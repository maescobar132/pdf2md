# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pymupdf==1.28.2",
#   "markitdown[docx,pptx,xlsx]==0.1.7",
# ]
# ///
"""Convert documents to Markdown; optionally strip images.

PDFs go through PyMuPDF (clean spacing on dense academic layouts, which the
pdfminer engine inside markitdown mangles). Text is NFKC-normalized so
ligatures like 'fi'/'fl' become plain ASCII while accented letters are kept.
Everything else (docx, pptx, xlsx, html, epub, csv) goes through markitdown.

Usage (via wrapper):
  pdf2md paper.pdf                 -> paper.md next to it
  pdf2md --no-images slides.pptx   -> slides.md, images removed (non-PDF only)
  pdf2md --no-images *.pdf docs/   -> batch; directories are recursed
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

MARKITDOWN = {".docx", ".pptx", ".xlsx", ".html", ".htm", ".epub", ".csv"}
SUPPORTED = MARKITDOWN | {".pdf"}

RE_DATA_IMG = re.compile(r"!\[[^\]]*\]\(data:[^)]*\)", re.DOTALL)
RE_IMG = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
RE_HTML_IMG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)


def strip_images(md: str) -> str:
    md = RE_DATA_IMG.sub("", md)
    md = RE_IMG.sub(lambda m: f"[imagen omitida: {m.group(1)}]" if m.group(1) else "", md)
    md = RE_HTML_IMG.sub("", md)
    return re.sub(r"\n{4,}", "\n\n\n", md)


def pdf_to_text(path: Path) -> str:
    """Page-ordered text via PyMuPDF, NFKC-normalized."""
    import pymupdf

    doc = pymupdf.open(path)
    pages = [doc[i].get_text() for i in range(doc.page_count)]
    doc.close()
    return unicodedata.normalize("NFKC", "\n".join(pages))


def convert_one(path: Path, no_images: bool) -> str:
    if path.suffix.lower() == ".pdf":
        return pdf_to_text(path)
    from markitdown import MarkItDown

    text = MarkItDown(enable_plugins=False).convert(str(path)).text_content
    return strip_images(text) if no_images else text


def targets(args: list[str]) -> list[Path]:
    out: list[Path] = []
    for a in args:
        p = Path(a)
        if p.is_dir():
            out += [q for q in sorted(p.rglob("*")) if q.suffix.lower() in SUPPORTED]
        elif p.exists():
            out.append(p)
        else:
            print(f"  !! no existe: {a}", file=sys.stderr)
    return out


def main() -> int:
    args = sys.argv[1:]
    no_images = "--no-images" in args
    files = targets([a for a in args if a != "--no-images"])
    if not files:
        print(__doc__)
        return 1

    failed = 0
    for f in files:
        out = f.with_suffix(".md")
        try:
            text = convert_one(f, no_images)
            out.write_text(text, encoding="utf-8")
            kb_in, kb_out = f.stat().st_size // 1024, out.stat().st_size // 1024
            print(f"  {f}  ->  {out.name}   ({kb_in} KB -> {kb_out} KB)")
            if not text.strip():
                print("     ADVERTENCIA: salida vacia. PDF escaneado? No hay OCR aqui.")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  FALLO {f}: {e}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
