# -*- coding: utf-8 -*-
r"""
spot_check.py - 12 篇抽检, 每篇随机抽 5 段, 写入 audits/spot_check_{ts}.md.

供人工 v2 校对时使用: 60 段翻译结果, 配原文逐段对照.
"""
import datetime
import random
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
OUT = ROOT / "out"
AUDITS = ROOT / "audits"
LOG_DIR = AUDITS / "run_log"


def read_text(p: Path) -> str:
    t = p.read_text(encoding="utf-8")
    if t.startswith("---"):
        t = t.split("---", 2)[2]
    return t


def split_paragraphs(text: str, min_len: int = 60):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if len(p.strip()) >= min_len]
    return paras


def main():
    random.seed(42)
    per_story = 5
    args = sys.argv[1:]
    for i, a in enumerate(args):
        if a == "--n" and i + 1 < len(args):
            per_story = int(args[i + 1])

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    out_files = sorted(OUT.glob("*_zh.md"))
    if not out_files:
        sys.exit(f"!!! out/ 为空, 先跑 export_full.py")

    print(f"=== spot_check.py ({len(out_files)} 篇 × {per_story} 段) ===")
    report = [
        f"# 12 篇抽检报告 (人工 v2 校对参考)",
        f"生成时间: {datetime.datetime.now().isoformat()}",
        f"每篇随机抽 {per_story} 段, 共 {len(out_files) * per_story} 段",
        f"使用方法: 逐段对照英文原文, 标注错译/漏译/术语漂移",
        "",
    ]

    for out_p in out_files:
        slug = out_p.stem.replace("_zh", "")
        src_p = SOURCES / f"{slug}.txt"
        if not src_p.exists():
            continue
        en_text = src_p.read_text(encoding="utf-8").strip()
        zh_text = read_text(out_p)
        en_paras = split_paragraphs(en_text)
        zh_paras = split_paragraphs(zh_text, min_len=30)
        if not en_paras or not zh_paras:
            continue
        n = min(per_story, len(en_paras), len(zh_paras))
        sample_en = random.sample(en_paras, n)
        sample_zh = random.sample(zh_paras, n)

        report.append(f"## {slug}")
        report.append(f"英文 {len(en_text):,} 字符 / {len(en_paras)} 段  →  中文 {len(zh_text):,} 字符 / {len(zh_paras)} 段")
        report.append("")
        for j, (en, zh) in enumerate(zip(sample_en, sample_zh), 1):
            report.append(f"### 段 {j}")
            report.append("**[英文原文]**")
            report.append(f"```")
            report.append(en[:500])
            report.append(f"```")
            report.append("**[中文译文]**")
            report.append(f"```")
            report.append(zh[:500])
            report.append(f"```")
            report.append("")
        report.append("---")
        report.append("")

    out_md = LOG_DIR / f"spot_check_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    out_md.write_text("\n".join(report), encoding="utf-8")
    print(f"  -> {out_md.relative_to(ROOT)}")
    print(f"  抽检段数: {len(out_files) * per_story}")


if __name__ == "__main__":
    main()
