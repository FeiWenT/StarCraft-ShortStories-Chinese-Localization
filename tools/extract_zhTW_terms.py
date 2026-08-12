# -*- coding: utf-8 -*-
r"""
extract_zhTW_terms.py - 12 篇新英文 -> 抽取未在 glossary 的专名
"""
import json
import re
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
AUDITS = ROOT / "audits"

GLOSS = json.load(open(ROOT.parent / "StarCraft_汉化" / "publish" / "terminology" / "glossary.json", encoding="utf-8"))
EXISTING_ENS = {e["en"].lower() for e in GLOSS["entries"]}
print(f"Loaded {len(EXISTING_ENS)} existing EN terms from glossary.json")

all_new_en = ""
for f in sorted(SOURCES.glob("*.txt")):
    all_new_en += "\n" + f.read_text(encoding="utf-8")
print(f"Loaded 12 new English files, total {len(all_new_en)} chars")

PROPER_NOUN = re.compile(r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,2})\b")
new_proper_nouns = []
for m in PROPER_NOUN.finditer(all_new_en):
    n = m.group(1).strip()
    nl = n.lower()
    if nl in EXISTING_ENS:
        continue
    if n in ("I", "A", "An", "The", "And", "Or", "But", "So", "This", "That", "It", "If", "Oh", "No", "Yes", "All", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "How", "Why", "What", "When", "Where", "Who", "He", "She", "They", "We", "You", "My", "Your", "His", "Her", "Its", "Our", "Their", "Then", "Now", "Just", "Even", "Still", "Only", "Very", "Really", "Much", "Many", "Some", "Any", "Each", "Every", "Most", "More", "Less", "Such", "Same", "Other", "Another", "First", "Last", "Next", "New", "Old", "Good", "Bad", "Big", "Small", "Long", "Short", "High", "Low", "Right", "Left", "Up", "Down", "In", "Out", "On", "Off", "Over", "Under", "Above", "Below", "Before", "After", "During", "Between", "Without", "Within", "Through", "Across", "Around", "Along", "Against", "Among", "Behind", "Beyond", "Despite", "Except", "Inside", "Outside", "Throughout", "Until", "Upon", "With", "About", "Around", "Before"):
        continue
    new_proper_nouns.append(n)

freq = Counter(new_proper_nouns)
print(f"\nTop 100 proper nouns NOT in existing 680 glossary:")
print(f"{'Count':>6}  Term")
for n, c in freq.most_common(100):
    print(f"{c:>6}  {n}")
