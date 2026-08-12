# -*- coding: utf-8 -*-
r"""
split_story.py - 把 sources/{slug}.txt 按 1800 字符切块写到 drafts/{slug}/split/chunk_NN.md.

独立工具: 通常 mt_story.py 内置 chunking, 但有时需要先切块看结构 (人工预览, 估算 chunk 数).
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
DRAFTS = ROOT / "drafts"
SIZE = 1800


def split_story(slug: str, size: int = SIZE):
    src = SOURCES / f"{slug}.txt"
    if not src.exists():
        sys.exit(f"!!! 故事源不存在: {src}")
    text = src.read_text(encoding="utf-8").strip()
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    out = DRAFTS / slug / "split"
    out.mkdir(parents=True, exist_ok=True)
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
    for i, c in enumerate(chunks, 1):
        f = out / f"chunk_{i:02d}.md"
        f.write_text(f"---\nslug: {slug}\nchunk: {i:02d}\nchars: {len(c)}\n---\n\n{c}\n", encoding="utf-8")
    print(f"  {slug}: {len(text):,} chars -> {len(chunks)} 块, 写到 {out.relative_to(ROOT)}/")
    return chunks


def main():
    args = sys.argv[1:]
    if not args or "--all" in args:
        for f in sorted(SOURCES.glob("*.txt")):
            split_story(f.stem)
        return
    split_story(args[0])


if __name__ == "__main__":
    main()
