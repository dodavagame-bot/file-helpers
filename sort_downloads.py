#!/usr/bin/env python3
"""
Purpose: Sort a Downloads directory into folders by file type.
Example: python sort_downloads.py ~/Downloads
Warning: This moves files; inspect the preview and confirm before continuing.
"""

import argparse
import shutil
from pathlib import Path


CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"},
    "videos": {".mp4", ".mov", ".mkv", ".avi", ".webm"},
    "audio": {".mp3", ".wav", ".flac", ".m4a", ".ogg"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"},
    "spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "archives": {".zip", ".tar", ".gz", ".bz2", ".7z", ".rar"},
    "installers": {".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"},
}


def category_for(path: Path) -> str:
    for category, extensions in CATEGORIES.items():
        if path.suffix.lower() in extensions:
            return category
    return "other"


def available_target(target: Path) -> Path:
    if not target.exists():
        return target
    for number in range(1, 10000):
        candidate = target.with_name(f"{target.stem} ({number}){target.suffix}")
        if not candidate.exists():
            return candidate
    raise OSError(f"could not find an unused name for {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sort downloaded files by type.")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Show moves without moving files")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error(f"directory does not exist: {args.directory}")
    files = sorted(path for path in args.directory.iterdir() if path.is_file())
    if not files:
        print("No files found.")
        return 0

    plan = [(path, args.directory / category_for(path) / path.name) for path in files]
    print("Planned moves:")
    for source, target in plan:
        print(f"  {source.name} -> {target.parent.name}\\{target.name}")
    if args.dry_run:
        return 0
    if input("Move these files? [y/N] ").strip().lower() not in {"y", "yes"}:
        print("Cancelled.")
        return 0

    moved = 0
    for source, target in plan:
        try:
            target.parent.mkdir(exist_ok=True)
            shutil.move(str(source), str(available_target(target)))
            moved += 1
        except OSError as error:
            print(f"Failed to move {source}: {error}")
    print(f"Moved {moved} of {len(plan)} file(s).")
    return 0 if moved == len(plan) else 1


if __name__ == "__main__":
    raise SystemExit(main())
