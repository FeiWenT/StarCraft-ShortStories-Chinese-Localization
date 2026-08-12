# -*- coding: utf-8 -*-
r"""
mt_story.py - 短篇 LLM 翻译 (Ollama + Qwen2.5-14B-Instruct), 篇级.

继承自 StarCraft_汉化/publish/tools/mt_chapter.py (Nova/Spectres 验证范式),
改造点: 去掉 book/ch_num/prologue/epilogue 逻辑, 输入为单 .txt 文件, 改 slug 命名.
"""
import datetime
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:14b-instruct-q4_K_M"

SOURCES = ROOT / "sources"
DRAFTS = ROOT / "drafts"
LLM_DIR = DRAFTS / "__slug__" / "llm_drafts"
FINAL_DIR = DRAFTS / "__slug__" / "final"
CACHE_FILE = DRAFTS / "__slug__" / "_mt_cache.json"
GLOSS_FILE = ROOT / "terminology" / "glossary.json"
CALL_LOG = ROOT / "audits" / "llm_call_log"
ANCHOR_FILE = ROOT.parent / "StarCraft_汉化" / "publish" / "out" / "StarCraft_Ghost_Nova_zh.md"

CHUNK_SIZE = 1800
DEFAULT_TOP_K = 50

# 12 篇 slug + 中文标题
SLUG_TITLE = {
    "10th_anniversary__operation_blind_devil": "蒙眼行动",
    "10th_anniversary__waking_dreams": "清醒梦境",
    "10th_anniversary__one_people_one_purpose": "万众一心",
    "sc_brood_war__hybrid": "混合体",
    "sc_brood_war__revelations": "启示录",
    "wings_of_liberty__collateral_damage": "附带损伤",
    "wings_of_liberty__heavens_devils_lost_transmissions": "天堂魔鬼遗失的电讯",
    "wings_of_liberty__broken_wide": "宽宽出逃",
    "wings_of_liberty__colossus": "巨像",
    "wings_of_liberty__stealing_thunder": "夺雷",
    "wings_of_liberty__mothership": "母舰",
    "wings_of_liberty__changeling": "变形虫",
}


def _w(word, rep):
    return (r"(?i)(?<![a-zA-Z])" + word + r"(?![a-zA-Z])", rep)


RESIDUE_MAP = [
    _w("yeah", "是啊"), _w("yup", "是啊"),
    _w("huh", "嗯"), _w("kinda", "有点"),
    _w("maybe", "也许"), _w("anything", "任何"),
    _w("oh no", "不好"), _w("damn", "该死"),
    _w("roger", "收到"), _w("affirmative", "同意"),
    _w("okay", "好的"), _w("ok", "好"),
    _w("shit", "该死"),
    _w("sir", "长官"),
    _w("captain", "上尉"), _w("commander", "指挥官"),
    _w("god", "老天"), _w("lord", "老天"),
    _w("nope", "不"), _w("hey", "嘿"),
    _w("hmm+", "唔"), _w("tsk", "啧"),
    _w("bingo", "中了"), _w("sure", "好"),
    _w("oi", "喂"), _w("sniff", "抽泣"),
]


STORY_SYSTEM_PROMPT = """\
你是中文科幻/军事小说翻译, 目标读者是熟悉《星际争霸》(StarCraft) 世界观的玩家.

【12 篇短篇通用翻译守则】
- 文气保留 > 通顺: 不要为了"中文通顺"而改写原文语气
  (zergling 第一人称段不要补"我", 军报体保留被动语态, 对话保留人物个性)
- 专有名词首次出现: 中文 (English) 注音, 后续只用中文
- 保留英文: 书名号/舰船型号/品牌缩写 (UNN, AAI, Tychus 等) 按原文
- 拟声词/语气词 (huh/yeah/maybe/damn) 按中文习惯译 (嗯/是啊/也许/该死)
- 省略号统一用 "……"
- 只输出译文, 不要任何解释、引号包裹、前后缀

【本篇特殊守则 (来自 style_notes.md)】
{style_notes}

【术语表 (本篇相关 {n} 条)】
{glossary}

【风格样例 (模仿这种句式与语域, 来自 Nova 终稿)】
{style_anchor}
"""


def load_glossary():
    return json.load(open(GLOSS_FILE, encoding="utf-8"))["entries"]


def filter_story_terms(entries, story_text, k=DEFAULT_TOP_K):
    """按出现频率 + priority 排序选 top k"""
    hits = []
    for e in entries:
        en = e["en"]
        if not en or len(en) < 3:
            continue
        if re.search(r"\b" + re.escape(en) + r"\b", story_text):
            hits.append(e)
    # 优先级: keep_english (致敬语) > zhTW > wiki; risk high 优先
    hits.sort(key=lambda e: (
        0 if e.get("keep_english") else 1,
        0 if e.get("priority") == "zhTW" else 1,
        0 if e.get("risk") == "high" else 1,
        e.get("category", ""),
    ))
    return hits[:k]


def load_style_anchor():
    if not ANCHOR_FILE.exists():
        return "(无 Nova 终稿, 直接翻译)"
    text = ANCHOR_FILE.read_text(encoding="utf-8")
    paras = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    # 跳过 frontmatter
    if paras and paras[0].startswith("---"):
        paras = paras[1:]
    if not paras:
        return "(Nova 终稿为空)"
    para = paras[0]
    if len(para) > 400:
        para = para[:400] + "..."
    return para


def load_style_notes(slug):
    p = DRAFTS / slug / "style_notes.md"
    if not p.exists():
        return "(无 style_notes.md, 按通用守则翻译)"
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return "(style_notes.md 为空)"
    return text


def chunk_story(text, size=CHUNK_SIZE):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []
    cur = []
    cur_len = 0
    for p in paras:
        if cur_len + len(p) > size and cur:
            chunks.append("\n\n".join(cur))
            cur = [p]
            cur_len = len(p)
        else:
            cur.append(p)
            cur_len += len(p)
    if cur:
        chunks.append("\n\n".join(cur))
    return chunks


def chunk_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:10]


def make_story_system(story_text, entries, style_notes):
    terms = filter_story_terms(entries, story_text)
    gloss_lines = []
    for e in terms:
        if e.get("keep_english"):
            ann = e.get("zh_annotation", "")
            if ann:
                gloss_lines.append(f"  {e['en']} = {e['en']} (首次出现注音: {ann})")
            else:
                gloss_lines.append(f"  {e['en']} = {e['en']} (保留英文)")
        else:
            gloss_lines.append(f"  {e['en']} = {e['zh']}")
    gloss = "\n".join(gloss_lines) or "  (无特别术语, 按通用理解)"
    style = load_style_anchor()
    return STORY_SYSTEM_PROMPT.format(
        style_notes=style_notes, n=len(terms), glossary=gloss, style_anchor=style
    )


def make_user_v0(chunk_text, chunk_idx, total):
    return (
        f"请翻译下面这段英文 (第 {chunk_idx+1}/{total} 段), 直接给出中文:\n\n"
        f"{chunk_text}\n"
    )


def make_user_v1(orig_en, v0_zh):
    return (
        "下面是你之前翻译的一段, 请检查并修正:\n"
        "1. 所有英文专名是否已用术语表里的中文?\n"
        "2. 是否有未翻译的英文残留?\n"
        "3. 句式是否流畅?\n"
        "4. 是否漏译了原文内容?\n\n"
        "只输出修正后的中文 (不要解释).\n\n"
        f"[英文原文]\n{orig_en}\n\n"
        f"[你的初翻]\n{v0_zh}\n"
    )


def call_ollama(messages, temperature=0.3, num_predict=-1, timeout=600, retries=3):
    body = json.dumps({
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": num_predict},
    }).encode("utf-8")
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(OLLAMA_URL, body, {"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            return data["message"]["content"].strip()
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(2)
    raise RuntimeError(f"Ollama 调用失败 {retries} 次: {last_err}")


def clean_residue(cn):
    for pat, rep in RESIDUE_MAP:
        cn = re.sub(pat, rep, cn)
    return cn


def self_check(cn, story_en, entries):
    issues = []
    en_words = re.findall(r"\b[A-Za-z]{4,}\b", cn)
    en_freq = {}
    for w in en_words:
        en_freq[w] = en_freq.get(w, 0) + 1
    if en_words:
        issues.append(("英文残留", en_freq))
    terms = filter_story_terms(entries, story_en, k=200)
    for t in terms:
        if t["en"] in cn and t.get("zh") and t["zh"] not in cn and not t.get("keep_english"):
            issues.append(("术语未对齐", f"{t['en']} -> 期望 {t['zh']}"))
    return issues


def load_cache(slug):
    p = Path(str(CACHE_FILE).replace("__slug__", slug))
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return {}


def save_cache(slug, cache):
    p = Path(str(CACHE_FILE).replace("__slug__", slug))
    p.parent.mkdir(parents=True, exist_ok=True)
    json.dump(cache, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)


def log_call(slug, idx, system, user, response, duration):
    p = CALL_LOG / slug
    p.mkdir(parents=True, exist_ok=True)
    f = p / f"chunk{idx:02d}_call.jsonl"
    rec = {
        "ts": datetime.datetime.now().isoformat(),
        "idx": idx,
        "duration_s": round(duration, 1),
        "model": MODEL,
        "system_len": len(system),
        "user_len": len(user),
        "response_len": len(response),
        "system": system,
        "user": user,
        "response": response,
    }
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def translate_story(slug, deploy=False, n_chunks=None):
    print(f"=== mt_story.py [{slug}] {'(DEPLOY)' if deploy else '(DRY)'} ===")
    src_path = SOURCES / f"{slug}.txt"
    if not src_path.exists():
        sys.exit(f"!!! 故事源不存在: {src_path}")
    story_text = src_path.read_text(encoding="utf-8").strip()
    print(f"  源: {src_path.relative_to(ROOT)}  ({len(story_text):,} chars)")

    entries = load_glossary()
    print(f"  glossary: {len(entries)} 条")
    style_notes = load_style_notes(slug)
    system = make_story_system(story_text, entries, style_notes)
    print(f"  system prompt: {len(system):,} chars (含 style_notes + 风格锚)")

    chunks = chunk_story(story_text)
    if n_chunks:
        chunks = chunks[:n_chunks]
        print(f"  分块: {len(chunks)} 段 (限 n={n_chunks})")
    else:
        print(f"  分块: {len(chunks)} 段")

    out_dir = Path(str(LLM_DIR).replace("__slug__", slug))
    out_dir.mkdir(parents=True, exist_ok=True)
    cache = load_cache(slug)

    v0_parts = []
    v1_parts = []
    total_t = 0
    for i, chunk in enumerate(chunks):
        h = chunk_hash(chunk)
        cache_key = f"chunk{i:02d}_{h}_v0"
        cache_key_v1 = f"chunk{i:02d}_{h}_v1"

        if cache_key in cache:
            v0 = cache[cache_key]
            print(f"  [{i+1}/{len(chunks)}] v0 缓存命中 ({len(v0)} chars)")
        else:
            t0 = time.time()
            user_v0 = make_user_v0(chunk, i, len(chunks))
            v0 = call_ollama([
                {"role": "system", "content": system},
                {"role": "user", "content": user_v0},
            ], temperature=0.3)
            v0 = clean_residue(v0)
            cache[cache_key] = v0
            save_cache(slug, cache)
            d = time.time() - t0
            total_t += d
            log_call(slug, i*2, system, user_v0, v0, d)
            print(f"  [{i+1}/{len(chunks)}] v0 完成 ({len(v0)} chars, {d:.1f}s)")

        if cache_key_v1 in cache:
            v1 = cache[cache_key_v1]
            print(f"  [{i+1}/{len(chunks)}] v1 缓存命中 ({len(v1)} chars)")
        else:
            t0 = time.time()
            user_v1 = make_user_v1(chunk, v0)
            v1 = call_ollama([
                {"role": "system", "content": system},
                {"role": "user", "content": user_v1},
            ], temperature=0.1)
            v1 = clean_residue(v1)
            cache[cache_key_v1] = v1
            save_cache(slug, cache)
            d = time.time() - t0
            total_t += d
            log_call(slug, i*2+1, system, user_v1, v1, d)
            print(f"  [{i+1}/{len(chunks)}] v1 完成 ({len(v1)} chars, {d:.1f}s)")

        v0_parts.append(v0)
        v1_parts.append(v1)

    title = SLUG_TITLE.get(slug, slug)
    fm = f"---\ntitle: {title}\nslug: {slug}\nsource: sources/{slug}.txt\nmodel: {MODEL}\nchars_en: {len(story_text)}\n---\n\n"
    v0_path = out_dir / f"full_v0.md"
    v1_path = out_dir / f"full_v1.md"
    v0_path.write_text(fm + "\n\n".join(v0_parts), encoding="utf-8")
    v1_path.write_text(fm + "\n\n".join(v1_parts), encoding="utf-8")
    print(f"\n  -> {v0_path.relative_to(ROOT)}  ({sum(len(x) for x in v0_parts):,} chars)")
    print(f"  -> {v1_path.relative_to(ROOT)}  ({sum(len(x) for x in v1_parts):,} chars)")
    print(f"  总 LLM 耗时: {total_t:.1f}s")

    final_text = "\n\n".join(v1_parts)
    issues = self_check(final_text, story_text, entries)
    if issues:
        print(f"\n  自检: {len(issues)} 项问题")
        for kind, detail in issues[:10]:
            if isinstance(detail, dict):
                sample = list(detail.items())[:5]
                print(f"    [{kind}] {sample}")
            else:
                print(f"    [{kind}] {detail}")
    else:
        print(f"\n  自检: OK 无问题")

    if deploy:
        final = Path(str(FINAL_DIR).replace("__slug__", slug))
        final.mkdir(parents=True, exist_ok=True)
        final_path = final / f"full.md"
        final_path.write_text(fm + final_text, encoding="utf-8")
        print(f"  部署: {final_path.relative_to(ROOT)}")
    else:
        print(f"  (DRY) 未部署, 试翻后人工审核 v1 -> 手动部署")


def main():
    args = sys.argv[1:]
    if "--all" in args:
        # 遍历所有 .txt
        for f in sorted(SOURCES.glob("*.txt")):
            translate_story(f.stem, deploy="--go" in args)
        return
    if not args or "--help" in args or "-h" in args:
        print("用法: python mt_story.py <slug> [--go] [--n N]")
        print("      python mt_story.py --all [--go]")
        print("\n可用的 slug:")
        for slug, title in SLUG_TITLE.items():
            print(f"  {slug}  ({title})")
        return
    slug = args[0]
    deploy = "--go" in args
    n_chunks = None
    for i, a in enumerate(args):
        if a == "--n" and i + 1 < len(args):
            n_chunks = int(args[i + 1])
    translate_story(slug, deploy=deploy, n_chunks=n_chunks)


if __name__ == "__main__":
    main()
