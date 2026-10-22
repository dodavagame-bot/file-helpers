#!/usr/bin/env python3
"""
Purpose: Search text inside PDF files and report matching pages.
Example: python search_pdfs.py reports "invoice" --recursive
Warning: Scanned-image PDFs have no searchable text unless OCR was run first.
"""

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Search PDFs for a word or phrase.")
    parser.add_argument("directory", type=Path)
    parser.add_argument("term")
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error(f"directory does not exist: {args.directory}")
    if not args.term:
        parser.error("search term cannot be empty")
    try:
        from pypdf import PdfReader
        from pypdf.errors import PdfReadError
    except ImportError:
        print("This tool requires pypdf. Install it with: python -m pip install pypdf")
        return 1

    paths = args.directory.rglob("*.pdf") if args.recursive else args.directory.glob("*.pdf")
    pdfs = sorted(path for path in paths if path.is_file())
    matches = 0
    for path in pdfs:
        try:
            reader = PdfReader(str(path))
            pages = []
            for number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if args.term.casefold() in text.casefold():
                    pages.append(number)
            if pages:
                matches += 1
                print(f"{path}: pages {', '.join(map(str, pages))}")
        except (OSError, ValueError, PdfReadError) as error:
            print(f"Failed to read {path}: {error}")
    if matches == 0:
        print("No matches found.")
    else:
        print(f"Found matches in {matches} PDF(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
