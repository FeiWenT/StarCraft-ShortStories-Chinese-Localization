# -*- coding: utf-8 -*-
r"""
story_self_check.py - 12 篇短篇专用的 pitfall 自检.

每篇有不同的写作风险:
  - 蒙眼行动: zergling 第一人称段误插"我"
  - Waking Dreams: 双关结尾 / Defenders of Man / UnQueen 术语
  - 万众一心: 4 方 POV 区分
  - 混合体: SC1 早期术语漂移
  - 启示录: Valerian 助手 Therun 译法
  - 7 篇 WoL: 殖民地 (Chau Sara) + 幽灵计划 + Heaven's Devils

用法:
  python tools/story_self_check.py --story 10th_anniversary__operation_blind_devil --file drafts/.../full_v1.md
  python tools/story_self_check.py --all      # 扫所有 drafts/*/llm_drafts/full_v1.md
"""
import argparse
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "drafts"


def read_text(p: Path) -> str:
    t = p.read_text(encoding="utf-8")
    if t.startswith("---"):
        t = t.split("---", 2)[2]
    return t


# --- 各篇 pitfall ----------------------------------------------------

def check_operation_blind_devil(zh):
    """蒙眼行动: zergling 第一人称段误插'我'

    判定启发式: zergling 段特征 = 含 "我" + 跳虫专属动作 (想/看/听/闻/嗅/感觉到)
                非 zergling 段 (Kerrigan 视角/人类对话) 即使含"我"/"我们"也 OK
    """
    issues = []
    paras = zh.split("\n\n")
    zergling_action = r"(想|看|听|闻|嗅|感[受到觉]|嘶[吼叫]|低吼|哀[号鸣]|扑|抓|踢|咬|伸出|伸展|踱步|踉跄|爬过|扑倒|翻身|抬头|低头|怒视|瞥)"
    for i, p in enumerate(paras):
        # 排除对话 (引号内)
        if re.search(r"[\"「『].*?[\"」』]", p):
            continue
        # 排除通讯体 (机密/通讯编号/收件人/发件人)
        if re.search(r"(机密|通讯编号|收件人|发件人|传输)", p):
            continue
        # zergling 段 = 含"我"作主语 + 跳虫动作
        if re.search(r"^我[们]?[\s,。]", p) and re.search(zergling_action, p):
            issues.append(f"[蒙眼-zergling POV 误插'我'] 段 {i}: {p[:80]}")
    # 抚摸渐进 4 次
    stroke_count = len(re.findall(r"(抚摸|摸|触碰|碰触|抚过|拂过|轻触)", zh))
    if stroke_count < 3:
        issues.append(f"[蒙眼-抚摸 4 次] 只检测到 {stroke_count} 次, 应有 3-4 次递进")
    return issues


def check_waking_dreams(zh):
    """Waking Dreams: Defenders of Man / UnQueen 译法, 双关结尾"""
    issues = []
    # Defenders 译法统一 (人类捍卫者)
    if "Defenders" in zh or "人类的捍卫者" not in zh and "捍卫者" not in zh:
        issues.append("[Waking-Defenders] 'Defenders of Man' 应译'人类捍卫者', 出现英文或漏译")
    # UnQueen
    if "UnQueen" in zh and "幽后" not in zh:
        issues.append("[Waking-UnQueen] 'UnQueen' 应译'幽后', 需保留英文或翻译")
    # 双关结尾: "Wake" (醒来/清醒)
    if re.search(r"(清醒|唤醒|醒来)", zh) and re.search(r"清醒梦境", zh) is None:
        issues.append("[Waking-标题] 'Waking Dreams' 标题'清醒梦境' 应出现")
    return issues


def check_one_people_one_purpose(zh):
    """万众一心: 4 方 POV (卡莱 / 塔达力姆 / 净化者 / 达西瑞斯)"""
    issues = []
    povs = ["卡莱", "塔达力姆", "净化者", "达西瑞斯", "兰萨瑞斯", "莫汉达尔", "内拉斯"]
    found_povs = [p for p in povs if p in zh]
    if len(found_povs) < 4:
        issues.append(f"[万众一心-POV 缺失] 仅 {len(found_povs)}/{len(povs)} 个 POV 标签: {found_povs}")
    return issues


def check_hybrid(zh):
    """混合体: SC1 早期术语 (Madrid / Pandora 太空站)"""
    issues = []
    if "马德里" in zh and "潘多拉" in zh:
        pass  # ok
    elif "Madrid" in zh or "Pandora" in zh:
        issues.append("[混合体-术语] 'Madrid'/'Pandora' 应译'马德里'/'潘多拉'")
    # 混合体 (Hybrid) 本身
    if "Hybrid" in zh and "混合体" not in zh:
        issues.append("[混合体-核心] 'Hybrid' 应译'混合体'")
    return issues


def check_revelations(zh):
    """启示录: Valerian 助手 Therun"""
    issues = []
    if "Therun" in zh and "塞伦" not in zh:
        issues.append("[启示录-Therun] 应译'塞伦'")
    if "Valerian" in zh and "瓦莱里安" not in zh:
        issues.append("[启示录-Valerian] 应译'瓦莱里安'")
    # 外星遗迹
    if "Aldera" in zh and "奥尔德拉" not in zh:
        issues.append("[启示录-Aldera] 应译'奥尔德拉'")
    return issues


def check_collateral_damage(zh):
    """附带损伤: 殖民地 Chau Sara"""
    issues = []
    if "Chau Sara" in zh and "周·萨拉" not in zh and "周萨拉" not in zh:
        issues.append("[附带损伤-Chau Sara] 应译'周·萨拉'或'周萨拉'")
    return issues


def check_broken_wide(zh):
    """宽宽出逃: 幽灵计划 / 12 岁小孩 POV"""
    issues = []
    if "Ghost Program" in zh and "幽灵计划" not in zh:
        issues.append("[宽宽-Ghost Program] 应译'幽灵计划'")
    if re.search(r"\b(Proehl|Brody)\b", zh):
        issues.append("[宽宽-人名] Proehl/Brody 应有中文译名")
    return issues


def check_heavens_devils(zh):
    """天堂魔鬼遗失的电讯: Heaven's Devils (Raynor/Tychus 旧部队)"""
    issues = []
    if "Heaven" in zh and "魔鬼" in zh:
        pass  # ok
    if "天堂魔鬼" not in zh and "Heaven" in zh:
        issues.append("[天堂魔鬼-部队名] 'Heaven's Devils' 应译'天堂魔鬼'")
    return issues


def check_colossus(zh):
    """巨像: 巨像 (colossus 兵种)"""
    issues = []
    if "Colossus" in zh and "巨像" not in zh:
        issues.append("[巨像-兵种] 'Colossus' 应译'巨像'")
    return issues


def check_stealing_thunder(zh):
    """夺雷: 雷 (thunder) 词义双关"""
    issues = []
    if re.search(r"\b(Thunder|thunder)\b", zh) and "夺雷" not in zh and "雷" not in zh:
        issues.append("[夺雷-核心] 'thunder' 应出现'雷'")
    return issues


def check_mothership(zh):
    """母舰: 母舰 (Protoss 旗舰)"""
    issues = []
    if "Mothership" in zh and "母舰" not in zh:
        issues.append("[母舰-旗舰] 'Mothership' 应译'母舰'")
    return issues


def check_changeling(zh):
    """变形虫: changeling (Zerg 间谍单位)"""
    issues = []
    if "Changeling" in zh and "变形虫" not in zh:
        issues.append("[变形虫-兵种] 'Changeling' 应译'变形虫'")
    return issues


CHECKERS = {
    "10th_anniversary__operation_blind_devil": check_operation_blind_devil,
    "10th_anniversary__waking_dreams": check_waking_dreams,
    "10th_anniversary__one_people_one_purpose": check_one_people_one_purpose,
    "sc_brood_war__hybrid": check_hybrid,
    "sc_brood_war__revelations": check_revelations,
    "wings_of_liberty__collateral_damage": check_collateral_damage,
    "wings_of_liberty__heavens_devils_lost_transmissions": check_heavens_devils,
    "wings_of_liberty__broken_wide": check_broken_wide,
    "wings_of_liberty__colossus": check_colossus,
    "wings_of_liberty__stealing_thunder": check_stealing_thunder,
    "wings_of_liberty__mothership": check_mothership,
    "wings_of_liberty__changeling": check_changeling,
}


def run_check(slug: str, file: Path) -> list:
    if slug not in CHECKERS:
        return [f"[未知 slug] {slug} 没有对应 checker"]
    if not file.exists():
        return [f"[文件缺失] {file}"]
    zh = read_text(file)
    return CHECKERS[slug](zh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--story", help="slug, 如 10th_anniversary__operation_blind_devil")
    ap.add_argument("--file", help="单文件路径 (默认 drafts/{slug}/llm_drafts/full_v1.md)")
    ap.add_argument("--all", action="store_true", help="扫所有 draft")
    args = ap.parse_args()

    if args.all:
        any_issues = False
        for slug in CHECKERS:
            for sub in ("llm_drafts", "final"):
                f = DRAFTS / slug / sub / ("full_v1.md" if sub == "llm_drafts" else "full.md")
                if f.exists():
                    issues = run_check(slug, f)
                    if issues:
                        any_issues = True
                        print(f"=== {slug} ({sub}) ===")
                        for i in issues:
                            print(f"  {i}")
        if not any_issues:
            print("✓ 全部 OK, 无 pitfall")
        return

    if not args.story:
        ap.error("--story 或 --all 必填")
    fp = Path(args.file) if args.file else DRAFTS / args.story / "llm_drafts" / "full_v1.md"
    issues = run_check(args.story, fp)
    print(f"=== {args.story} ===")
    print(f"  文件: {fp.relative_to(ROOT)}")
    if not issues:
        print("  ✓ 无 pitfall")
        return
    for i in issues:
        print(f"  {i}")


if __name__ == "__main__":
    main()
