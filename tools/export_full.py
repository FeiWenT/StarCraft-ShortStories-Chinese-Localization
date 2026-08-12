# -*- coding: utf-8 -*-
r"""
export_full.py - 把 12 篇 llm_drafts/full_v1.md 部署到 out/{slug}_zh.md.

12 篇短篇, 每篇一个 .md 文件 (mt_story.py 已经把全文拼好), 不需要按章拼装.
本工具职责: 从 drafts/{slug}/llm_drafts/full_v1.md 拷贝 + 重命名 + 去掉 frontmatter 到 out/.

如果 drafts/{slug}/final/full.md 存在 (人工 v2 校对后), 优先用 final.

输出排序 (按 Tier):
  Tier 1 (4 篇): 蒙眼行动, 清醒梦境, 万众一心, 启示录
  Tier 2 (5 篇): 混合体, 巨像, 母舰, 变形虫, 夺雷
  Tier 3 (3 篇): 附带损伤, 天堂魔鬼, 宽宽出逃

用法:
  python tools/export_full.py                  # 处理所有 12 篇
  python tools/export_full.py 10th_anniversary__operation_blind_devil
  python tools/export_full.py --tier 1
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
DRAFTS = ROOT / "drafts"

# Tier 排序 (从易到难, 12 篇)
TIER_ORDER = {
    "10th_anniversary__operation_blind_devil": 1,   # 5 星 (MVP, 最难)
    "10th_anniversary__waking_dreams": 1,           # 4 星
    "10th_anniversary__one_people_one_purpose": 1,  # 4 星 (4 方 POV)
    "sc_brood_war__revelations": 1,                 # 4 星
    "sc_brood_war__hybrid": 2,                      # 3 星
    "wings_of_liberty__colossus": 2,                # 3 星
    "wings_of_liberty__mothership": 2,              # 3 星
    "wings_of_liberty__changeling": 2,              # 3 星
    "wings_of_liberty__stealing_thunder": 2,        # 3 星
    "wings_of_liberty__collateral_damage": 3,       # 2 星
    "wings_of_liberty__heavens_devils_lost_transmissions": 3,  # 2 星
    "wings_of_liberty__broken_wide": 3,             # 2 星
}

# 12 篇 slug + 中文标题 (与 mt_story.py 一致)
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


def read_md(p: Path):
    if not p.exists():
        return None
    t = p.read_text(encoding="utf-8")
    if t.startswith("---"):
        t = t.split("---", 2)[2].lstrip()
    return t


def export_story(slug: str) -> dict:
    """返回 {'ok': bool, 'src': str, 'dst': str, 'chars': int, 'tier': int, 'title': str}"""
    title = SLUG_TITLE.get(slug, slug)
    tier = TIER_ORDER.get(slug, 9)
    # 优先 final (人工 v2), 否则 llm_drafts v1
    final_p = DRAFTS / slug / "final" / "full.md"
    v1_p = DRAFTS / slug / "llm_drafts" / "full_v1.md"
    v0_p = DRAFTS / slug / "llm_drafts" / "full_v0.md"
    if final_p.exists():
        src, src_kind = final_p, "final"
    elif v1_p.exists():
        src, src_kind = v1_p, "v1"
    elif v0_p.exists():
        src, src_kind = v0_p, "v0"
    else:
        return {"ok": False, "slug": slug, "reason": "no source (final/v1/v0 都没有)"}

    body = read_md(src)
    if not body:
        return {"ok": False, "slug": slug, "reason": "empty"}

    OUT.mkdir(parents=True, exist_ok=True)
    out_path = OUT / f"{slug}_zh.md"
    fm = (
        f"---\n"
        f"title: {title}\n"
        f"slug: {slug}\n"
        f"tier: {tier}\n"
        f"source: sources/{slug}.txt\n"
        f"exported: {datetime.datetime.now().isoformat()}\n"
        f"---\n\n"
    )
    out_path.write_text(fm + body, encoding="utf-8")
    return {"ok": True, "slug": slug, "title": title, "tier": tier,
            "src": str(src.relative_to(ROOT)), "src_kind": src_kind,
            "dst": str(out_path.relative_to(ROOT)), "chars": len(body)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?", help="单篇 slug")
    ap.add_argument("--tier", type=int, choices=[1, 2, 3], help="按 Tier 导出")
    ap.add_argument("--all", action="store_true", help="全部 12 篇")
    args = ap.parse_args()

    if args.tier:
        targets = [s for s, t in TIER_ORDER.items() if t == args.tier]
    elif args.slug:
        targets = [args.slug]
    elif args.all or True:
        targets = sorted(TIER_ORDER.keys(), key=lambda s: (TIER_ORDER[s], s))
    else:
        targets = []

    print(f"=== export_full.py ({len(targets)} 篇) ===")
    ok, fail = 0, 0
    for slug in targets:
        r = export_story(slug)
        if r["ok"]:
            ok += 1
            print(f"  ✓ T{r['tier']} {slug:55s} <- {r['src']:60s}  ({r['chars']:,} chars)")
        else:
            fail += 1
            print(f"  ✗ {slug:55s} {r.get('reason', '?')}")
    print(f"\n  成功 {ok}, 失败 {fail}")
    print(f"  输出目录: {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
