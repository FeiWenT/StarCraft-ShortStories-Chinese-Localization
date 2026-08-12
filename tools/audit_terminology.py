# -*- coding: utf-8 -*-
r"""
audit_terminology.py - 扫单篇终稿, 标"未对齐"的英文写法 (与 glossary v2 比对).

输入:
  - drafts/{slug}/final/full.md  (或 llm_drafts/full_v1.md)
  - terminology/glossary.json (v2, 730 条)

输出:
  - audits/terminology_audit_{slug}.md  (可读报告)
  - audits/terminology_audit_{slug}.csv  (机器可读)

用法:
  python tools/audit_terminology.py 10th_anniversary__operation_blind_devil
  python tools/audit_terminology.py 10th_anniversary__operation_blind_devil --dir llm_drafts
  python tools/audit_terminology.py --all
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
GLOSS_FILE = ROOT / "terminology" / "glossary.json"


def load_glossary():
    return json.load(open(GLOSS_FILE, encoding="utf-8"))["entries"]


def collect_files(slug: str, dir_name: str) -> list:
    base = ROOT / "drafts" / slug / dir_name
    if not base.exists():
        return []
    files = []
    for p in sorted(base.glob("*.md")):
        if p.name.startswith("_"):
            continue
        if "_v0" in p.name:
            continue
        files.append(p)
    return files


def read_text(p: Path) -> str:
    t = p.read_text(encoding="utf-8")
    if t.startswith("---"):
        t = t.split("---", 2)[2]
    return t


def find_english_residue(text: str, entries) -> dict:
    """找英文 (3+ 字母), 跟 glossary 对比, 标出未对齐的"""
    en_re = re.compile(r"\b[A-Za-z][A-Za-z\-']{2,}\b")
    gloss_en = {e["en"].lower() for e in entries if e.get("en")}

    freq = defaultdict(int)
    examples = defaultdict(list)
    for m in en_re.finditer(text):
        w = m.group(0)
        freq[w] += 1
        if len(examples[w]) < 3:
            ctx_s = max(0, m.start() - 20)
            ctx_e = min(len(text), m.end() + 20)
            examples[w].append(text[ctx_s:ctx_e].replace("\n", " "))

    aligned = {}
    residue = {}
    for w, c in freq.items():
        if w.lower() in gloss_en:
            aligned[w] = (c, examples[w])
        else:
            residue[w] = (c, examples[w])
    return {"aligned_en_kept": aligned, "unknown_residue": residue}


def find_unaligned_terms(text: str, entries) -> list:
    issues = []
    for e in entries:
        en = e["en"]
        zh = e["zh"]
        if not en or len(en) < 3:
            continue
        if not re.search(r"\b" + re.escape(en) + r"\b", text):
            continue
        if e.get("keep_english"):
            continue
        if zh not in text:
            issues.append({
                "en": en,
                "zh_expected": zh,
                "risk": e.get("risk", ""),
                "category": e.get("category", ""),
                "priority": e.get("priority", "wiki"),
            })
    return issues


def md_escape(s: str) -> str:
    return s.replace("|", r"\|")


def write_report(slug: str, dir_name: str, files: list):
    if not files:
        print(f"!!! 无文件可扫: drafts/{slug}/{dir_name}/")
        return
    print(f"=== audit_terminology.py [{slug} {dir_name}] ===")
    print(f"  扫描 {len(files)} 个文件")

    entries = load_glossary()
    all_residue = defaultdict(int)
    all_aligned_kept = defaultdict(int)
    all_unaligned = []

    for f in files:
        text = read_text(f)
        r = find_english_residue(text, entries)
        for w, (c, _) in r["unknown_residue"].items():
            all_residue[w] += c
        for w, (c, _) in r["aligned_en_kept"].items():
            all_aligned_kept[w] += c
        ua = find_unaligned_terms(text, entries)
        for u in ua:
            u["file"] = f.name
            all_unaligned.append(u)

    out_md = ROOT / "audits" / f"terminology_audit_{slug}.md"
    out_csv = ROOT / "audits" / f"terminology_audit_{slug}.csv"
    out_md.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"# 术语审计报告 — {slug} ({dir_name})", ""]
    lines.append(f"扫描文件数: {len(files)}")
    lines.append(f"未对齐术语条目: {len(all_unaligned)}")
    lines.append(f"未知英文残留 (不在 glossary): {len(all_residue)}")
    lines.append(f"glossary 中的英文保留 (应已替换但未替换): {len(all_aligned_kept)}")
    lines.append("")

    if all_unaligned:
        lines.append("## 1. 未对齐术语 (glossary 有英文原文, 但缺中文)")
        lines.append("| 文件 | 英文 | 期望中文 | 优先级 | 风险 | 类别 |")
        lines.append("|---|---|---|---|---|---|")
        for u in sorted(all_unaligned, key=lambda x: (x["risk"] != "high", x["priority"] != "zhTW", x["en"])):
            lines.append(f"| {u['file']} | {md_escape(u['en'])} | {md_escape(u['zh_expected'])} | {u['priority']} | {u['risk']} | {u['category']} |")
        lines.append("")

    if all_residue:
        lines.append("## 2. 未知英文残留 (不在 glossary)")
        lines.append("可能是品牌/型号/语气词/专名, 需人工判断是否要加进 glossary")
        lines.append("")
        lines.append("| 英文 | 总次数 |")
        lines.append("|---|---|")
        for w, c in sorted(all_residue.items(), key=lambda x: -x[1])[:50]:
            lines.append(f"| {md_escape(w)} | {c} |")
        lines.append("")

    if all_aligned_kept:
        lines.append("## 3. glossary 中保留为英文的实体")
        lines.append("可能 LLM 没替换, 也可能是品牌/型号/致敬语 (注: keep_english 5 条是预期保留)")
        lines.append("")
        lines.append("| 英文 | 总次数 | 备注 |")
        lines.append("|---|---|---|")
        notable_brands = {"UNN", "UED", "SCV", "CMC", "Umojan", "Korhal", "Tarsonis", "Antiga",
                          "En Taro Adun", "En Taro Tassadar", "En Taro Artanis",
                          "En Aru'din Raszagal", "Adun Toridas"}
        for w, c in sorted(all_aligned_kept.items(), key=lambda x: -x[1])[:30]:
            if w in notable_brands:
                note = "保留 OK (品牌/致敬语)"
            elif w.lower() in ("en", "taro", "adun", "tassadar", "artanis", "raszagal", "toridas"):
                note = "保留 OK (致敬语片段)"
            else:
                note = ""
            lines.append(f"| {md_escape(w)} | {c} | {note} |")
        lines.append("")

    out_md.write_text("\n".join(lines), encoding="utf-8")

    with open(out_csv, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["type", "file", "en", "zh_expected", "priority", "risk", "count"])
        for u in all_unaligned:
            w.writerow(["unaligned", u["file"], u["en"], u["zh_expected"], u["priority"], u["risk"], ""])
        for k, c in all_residue.items():
            w.writerow(["residue", "", k, "", "", "", c])
        for k, c in all_aligned_kept.items():
            w.writerow(["aligned_kept", "", k, "", "", "", c])

    print(f"  -> {out_md.relative_to(ROOT)}")
    print(f"  -> {out_csv.relative_to(ROOT)}")
    print(f"  未对齐: {len(all_unaligned)}  残留: {len(all_residue)}  保留: {len(all_aligned_kept)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?", help="单篇 slug")
    ap.add_argument("--dir", default="llm_drafts", choices=["llm_drafts", "final"])
    ap.add_argument("--all", action="store_true", help="扫所有 draft")
    args = ap.parse_args()

    if args.all:
        for slug_dir in sorted((ROOT / "drafts").iterdir()):
            if not slug_dir.is_dir():
                continue
            slug = slug_dir.name
            files = collect_files(slug, args.dir)
            if files:
                write_report(slug, args.dir, files)
        return
    if not args.slug:
        ap.error("slug 或 --all 必填")
    files = collect_files(args.slug, args.dir)
    write_report(args.slug, args.dir, files)


if __name__ == "__main__":
    main()
