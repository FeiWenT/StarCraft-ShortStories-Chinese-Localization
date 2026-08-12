# -*- coding: utf-8 -*-
r"""
build_glossary_v2.py - 从 glossary.json v1 (680) + zhTW_terminology_pairs.md 构建 v2 (720-730)
"""
import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
AUDITS = ROOT / "audits"
TERM = ROOT / "terminology"

V1_PATH = ROOT.parent / "StarCraft_汉化" / "publish" / "terminology" / "glossary.json"
V2_PATH = TERM / "glossary.json"
PAIRS_MD = AUDITS / "zhTW_terminology_pairs.md"

v1 = json.load(open(V1_PATH, encoding="utf-8"))
print(f"v1 entries: {len(v1['entries'])}")

for e in v1["entries"]:
    if "priority" not in e:
        e["priority"] = "wiki"

md = PAIRS_MD.read_text(encoding="utf-8")
new_entries = []

def parse_table(md_text, section_name):
    lines = md_text.split('\n')
    in_section = False
    rows = []
    for line in lines:
        if section_name in line and line.startswith('##'):
            in_section = True
            continue
        if in_section and line.startswith('## ') and section_name not in line:
            in_section = False
            continue
        if in_section and line.startswith('|') and '|' in line[1:] and '---' not in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if not parts or parts[0] in ('', '英文'):
                continue
            en = parts[0]
            # 列偏移: T1/T2/T3/T4 是 5 列表 (英文/zhTW/wiki/采纳/备注), zh 在 parts[1]
            # T5 (12 篇新译专有) 是 5 列表 (英文/出现次数/出现篇/建议译法/备注), zh 在 parts[3]
            if section_name == "12 篇新译专有专名":
                zh = parts[3] if len(parts) > 3 else ''
                prio_raw = ''  # 第五节无 priority 列
            else:
                zh = parts[1] if len(parts) > 1 else ''
                prio_raw = parts[3] if len(parts) > 3 else ''
            if '**zhTW**' in prio_raw:
                priority = 'zhTW'
            elif '**' in prio_raw:
                m = re.search(r'\*\*(\S+?)\*\*', prio_raw)
                priority = m.group(1) if m else 'wiki'
            else:
                priority = 'wiki'
            if en and zh and zh != en and len(en) < 100:
                rows.append((en, zh, priority))
    return rows

table1 = parse_table(md, "角色类")
table2 = parse_table(md, "地点/组织/概念类")
table3 = parse_table(md, "致敬语/祝福语类")
table4 = parse_table(md, "单位/战术类")
table5 = parse_table(md, "12 篇新译专有专名")

print(f"Parsed: T1={len(table1)} T2={len(table2)} T3={len(table3)} T4={len(table4)} T5={len(table5)}")

existing_ens = {e["en"].lower() for e in v1["entries"]}
added = 0
for en, zh, priority in table1 + table2 + table4 + table5:
    if en.lower() in existing_ens:
        for e in v1["entries"]:
            if e["en"].lower() == en.lower():
                if priority == "zhTW":
                    e["priority"] = "zhTW"
                break
        continue
    cat = "新译专用" if any(en == t[0] for t in table5) else "zhTW 官方"
    e = {
        "en": en,
        "zh": zh,
        "category": cat,
        "subcategory": "",
        "risk": "low",
        "priority": priority,
    }
    v1["entries"].append(e)
    existing_ens.add(en.lower())
    added += 1

for en, zh, priority in table3:
    if en.lower() in existing_ens:
        for e in v1["entries"]:
            if e["en"].lower() == en.lower():
                e["keep_english"] = True
                e["zh_annotation"] = zh
                e["priority"] = "wiki"
                break
        continue
    e = {
        "en": en,
        "zh": en,
        "zh_annotation": zh,
        "category": "致敬语",
        "subcategory": "Protoss",
        "risk": "low",
        "priority": "wiki",
        "keep_english": True,
    }
    v1["entries"].append(e)
    existing_ens.add(en.lower())
    added += 1

v1["version"] = "v2"
v1["source"] = "Nova/Spectres 680 + zhTW 23 篇官方 + 12 篇新译 (Stage 1-2, 2026-08-12)"
v1["zhTW_pairs_doc"] = "audits/zhTW_terminology_pairs.md"
v1["entries"].sort(key=lambda e: (e.get("priority", "wiki"), e.get("category", ""), e["en"]))

TERM.mkdir(parents=True, exist_ok=True)
V2_PATH.write_text(json.dumps(v1, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nv2 written: {V2_PATH}")
print(f"Total entries: {len(v1['entries'])} (added {added})")
pc = Counter(e.get("priority", "wiki") for e in v1["entries"])
print(f"Priority: {dict(pc)}")
print(f"keep_english: {sum(1 for e in v1['entries'] if e.get('keep_english'))}")
