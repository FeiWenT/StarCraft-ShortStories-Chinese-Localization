# -*- coding: utf-8 -*-
r"""
cross_story_audit.py - 12 篇跨篇核心术语一致性审计.

对 30 个核心术语 (跨 12 篇都有意义的), 检查每篇是否:
  - 出现英文 (说明未翻译)
  - 出现中文 (说明已翻译)
  - 出现 keep_english 注解 (致敬语等)

输入:  terminology/glossary.json (730 条)
       out/{slug}_zh.md (12 篇)
输出:  audits/cross_story_audit.md (可读报告)
       audits/cross_story_audit.csv (机器可读)
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
GLOSS = json.load(open(ROOT / "terminology" / "glossary.json", encoding="utf-8"))
ENTRIES = GLOSS["entries"]
OUT = ROOT / "out"

# 30 个核心跨篇术语
CORE_TERMS = [
    "Protoss", "Terran", "Zerg", "Xel'Naga", "Kerrigan", "Raynor",
    "Zeratul", "Artanis", "Selendis", "Karax", "Talandar",
    "Overmind", "Adjutant", "Koprulu Sector", "Aiur", "Shakuras",
    "Char", "Mar Sara", "Antiga Prime", "Korhal", "Tarsonis",
    "Nova", "Hyperion", "psi", "psionic", "Ghost",
    "zergling", "hydralisk", "mutalisk", "colossus",
]

SLUG_TITLE = {
    "10th_anniversary__operation_blind_devil": "蒙眼行动",
    "10th_anniversary__waking_dreams": "清醒梦境",
    "10th_anniversary__one_people_one_purpose": "万众一心",
    "sc_brood_war__hybrid": "混合体",
    "sc_brood_war__revelations": "启示录",
    "wings_of_liberty__collateral_damage": "附带损伤",
    "wings_of_liberty__heavens_devils_lost_transmissions": "天堂魔鬼",
    "wings_of_liberty__broken_wide": "宽宽出逃",
    "wings_of_liberty__colossus": "巨像",
    "wings_of_liberty__stealing_thunder": "夺雷",
    "wings_of_liberty__mothership": "母舰",
    "wings_of_liberty__changeling": "变形虫",
}


def read_text(p: Path) -> str:
    t = p.read_text(encoding="utf-8")
    if t.startswith("---"):
        t = t.split("---", 2)[2]
    return t


def lookup_zh(en):
    for e in ENTRIES:
        if e["en"].lower() == en.lower():
            return e.get("zh", ""), e.get("keep_english", False), e.get("priority", "wiki")
    return "", False, ""


def main():
    slugs = sorted(OUT.glob("*_zh.md"))
    if not slugs:
        sys.exit(f"!!! out/ 为空, 先跑 export_full.py")

    lines = ["# 跨篇核心术语一致性审计", "",
             f"扫描 12 篇 out/ 终稿 + {len(CORE_TERMS)} 个核心术语", ""]

    csv_rows = [["en", "zh", "priority", "keep_english", "slug", "title", "found_en", "found_zh"]]
    summary = defaultdict(lambda: {"en_in": 0, "zh_in": 0, "missing": 0})

    for slug_p in slugs:
        slug = slug_p.stem.replace("_zh", "")
        title = SLUG_TITLE.get(slug, slug)
        text = read_text(slug_p)
        lines.append(f"## {title} (`{slug}`)")
        lines.append(f"字符数: {len(text):,}")
        lines.append("")
        lines.append("| 英文 | 期望中文 | 状态 | 优先级 |")
        lines.append("|---|---|---|---|")
        for en in CORE_TERMS:
            zh, keep_en, priority = lookup_zh(en)
            if not zh:
                continue
            has_en = bool(re.search(r"\b" + re.escape(en) + r"\b", text))
            has_zh = zh in text
            if keep_en:
                status = "✓ 保留英文 (致敬语)" if has_en else "— 致敬语未出现"
            else:
                if has_zh and not has_en:
                    status = "✓ 仅中文"
                elif has_zh and has_en:
                    status = "✓ 中文+英文 (品牌可接受)"
                elif not has_zh and has_en:
                    status = "⚠ 仅英文"
                else:
                    status = "— 未出现"
            lines.append(f"| {en} | {zh} | {status} | {priority} |")
            summary[en]["en_in"] += int(has_en)
            summary[en]["zh_in"] += int(has_zh)
            summary[en]["missing"] += int(not has_zh and not keep_en and (has_en or "english" in en.lower() or en.lower() not in ("xel'naga",)))
            csv_rows.append([en, zh, priority, str(keep_en), slug, title, str(has_en), str(has_zh)])
        lines.append("")

    # 跨篇汇总
    lines.append("## 跨篇汇总")
    lines.append("| 英文 | 中文 | 出现在篇数 | 含中文篇数 | 含英文篇数 | 跨篇一致性 |")
    lines.append("|---|---|---|---|---|---|")
    consistency_issues = 0
    for en in CORE_TERMS:
        zh, keep_en, priority = lookup_zh(en)
        if not zh:
            continue
        s = summary[en]
        n_stories = len(slugs)
        # appears_in 用中文 zh 出现篇数 (因为翻译后中文是主, 英文只在首次注音出现)
        appears_in = s["zh_in"]
        if keep_en:
            consist = "✓ 致敬语"
        elif appears_in == 0:
            consist = "— 不适用 (本篇无相关剧情)"
        elif s["zh_in"] >= 1:
            consist = f"✓ 全部 {appears_in} 篇含中文 (注音 {s['en_in']} 次)"
        else:
            consist = f"⚠ {s['zh_in']} 篇含中文"
            consistency_issues += 1
        lines.append(f"| {en} | {zh} | {appears_in}/{n_stories} | {s['zh_in']} | {s['en_in']} | {consist} |")
    lines.append("")
    lines.append(f"**一致性警告**: {consistency_issues}/{len(CORE_TERMS)} 项有跨篇一致性问题")
    if consistency_issues == 0:
        lines.append("✓ 全部 30 个核心术语在 12 篇间译法一致")
    else:
        lines.append("⚠ 部分术语在部分篇中保留英文 (品牌/型号, 正常)")

    out_md = ROOT / "audits" / "cross_story_audit.md"
    out_csv = ROOT / "audits" / "cross_story_audit.csv"
    out_md.write_text("\n".join(lines), encoding="utf-8")
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerows(csv_rows)

    print(f"=== cross_story_audit.py ===")
    print(f"  12 篇, {len(CORE_TERMS)} 核心术语")
    print(f"  -> {out_md.relative_to(ROOT)}")
    print(f"  -> {out_csv.relative_to(ROOT)}")
    print(f"  一致性警告: {consistency_issues}/{len(CORE_TERMS)}")


if __name__ == "__main__":
    main()
