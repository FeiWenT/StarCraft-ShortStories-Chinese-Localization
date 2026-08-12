# -*- coding: utf-8 -*-
r"""
ocr_zhTW_stories.py - 23 篇 zhTW 官方短篇 -> 中文文本 (前 3 页 OCR)

仅抽前 3 页 (角色/地点集中), 避免全本 OCR 太慢 (24 篇 * 30 页 = 720 页太重).
"""
import shutil
import subprocess
import sys
from pathlib import Path
import fitz  # pymupdf

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "extracted" / "zhTW_raw" / "StarCraft_II_Shorts-zhTW"
TXT_DIR = ROOT / "extracted" / "zhTW_raw"

# Tesseract: 动态查找 PATH 里的 tesseract.exe (Windows 默认装在 Program Files, 加入 PATH 后无需 hardcode)
TESSERACT = shutil.which("tesseract") or shutil.which("tesseract.exe")
# TESSDATA: 走环境变量, 默认空 (用户需先 export TESSDATA_PREFIX=<chi_sim 所在目录>)
TESSDATA = ""  # 由调用方通过环境变量 TESSDATA_PREFIX 提供
RENDER_SCALE = 3.0
N_PAGES = 3

SLUG_MAP = {
    "a-war-on_zhTW.pdf": "a_war_on",
    "acid-burns-zhTW.pdf": "acid_burns",
    "ascension-zhTW.pdf": "ascension",
    "carrier-zhTW.pdf": "carrier",
    "children-void-zhTW.pdf": "children_of_the_void",
    "cold-symmetry-zhTW.pdf": "cold_symmetry",
    "command-performance-zhTW.pdf": "command_performance",
    "end-in-fire-zhTW.pdf": "end_in_fire",
    "frenzy-zhTW.pdf": "frenzy",
    "great-one-zhTW.pdf": "the_great_one",
    "icehouse-zhTW.pdf": "icehouse",
    "in-the-blood-zhTW.pdf": "in_the_blood",
    "in-the-dark-zhTW.pdf": "in_the_dark",
    "just-an-overlord-zhTW.pdf": "just_an_overlord",
    "lens-of-the-void-zhTW.pdf": "lens_of_the_void",
    "lost-vikings-zhTW.pdf": "lost_vikings",
    "momentum-zhTW.pdf": "momentum",
    "perditions-crossing-zhTW.pdf": "perdition_crossing",
    "sector-six-zhTW.pdf": "sector_six",
    "the-education-of-PFC-shane-zhTW.pdf": "education_of_pfc_shane",
    "the-exit-zhTW.pdf": "the_exit",
    "the-fightin-scee-vees-zhTW.pdf": "fightin_sceevees",
    "the-teacher-zhTW.pdf": "the_teacher",
}


def ocr_page(pdf_path, page_idx, tmp_png):
    doc = fitz.open(pdf_path)
    if page_idx >= len(doc):
        doc.close()
        return ""
    page = doc[page_idx]
    pix = page.get_pixmap(matrix=fitz.Matrix(RENDER_SCALE, RENDER_SCALE))
    pix.save(str(tmp_png))
    doc.close()
    env = {"TESSDATA_PREFIX": TESSDATA} if TESSDATA else None
    out = subprocess.run(
        [TESSERACT, str(tmp_png), "stdout", "-l", "chi_sim", "--psm", "6"],
        env=env, capture_output=True, encoding="utf-8", errors="replace", timeout=120
    )
    return out.stdout


def main():
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    print(f"Found {len(pdfs)} PDFs, starting OCR...")
    for i, pdf in enumerate(pdfs, 1):
        slug = SLUG_MAP.get(pdf.name)
        if not slug:
            print(f"  [{i}/{len(pdfs)}] {pdf.name} -> SKIP (no slug mapping)")
            continue
        out_txt = TXT_DIR / f"{slug}.txt"
        if out_txt.exists() and out_txt.stat().st_size > 100:
            print(f"  [{i}/{len(pdfs)}] {slug} -> exists, skip")
            continue
        tmp_png = TXT_DIR / f"_tmp_{slug}.png"
        try:
            text_parts = []
            for p in range(min(N_PAGES, 3)):
                t = ocr_page(pdf, p, tmp_png)
                text_parts.append(f"--- Page {p+1} ---\n{t}")
            out_txt.write_text("\n\n".join(text_parts), encoding="utf-8")
            print(f"  [{i}/{len(pdfs)}] {slug} -> {out_txt.name} ({out_txt.stat().st_size} bytes)")
        except Exception as e:
            print(f"  [{i}/{len(pdfs)}] {slug} -> ERROR: {e}")
        finally:
            if tmp_png.exists():
                tmp_png.unlink()
    print("done")


if __name__ == "__main__":
    main()
