#!/usr/bin/env python3
"""
Purpose: Save photo copies without EXIF location and camera metadata.
Example: python strip_photo_metadata.py photos clean-photos
Warning: Metadata is removed from output copies; keep originals as a backup.
"""

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Strip photo metadata into a new directory.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--recursive", action="store_true", help="Include subdirectories")
    args = parser.parse_args()
    if not args.source.is_dir():
        parser.error(f"source directory does not exist: {args.source}")
    try:
        from PIL import Image
    except ImportError:
        print("This tool requires Pillow. Install it with: python -m pip install Pillow")
        return 1

    extensions = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
    candidates = args.source.rglob("*") if args.recursive else args.source.iterdir()
    photos = sorted(path for path in candidates if path.is_file() and path.suffix.lower() in extensions)
    if not photos:
        print("No supported photos found.")
        return 0
    print(f"Found {len(photos)} photo(s); output will be written to {args.output}.")
    if input("Strip metadata from output copies? [y/N] ").strip().lower() not in {"y", "yes"}:
        print("Cancelled.")
        return 0

    completed = 0
    for source in photos:
        target = args.output / source.relative_to(args.source)
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(source) as image:
                image.save(target, exif=b"")
            completed += 1
        except (OSError, ValueError) as error:
            print(f"Failed to process {source}: {error}")
    print(f"Created {completed} of {len(photos)} cleaned photo(s).")
    return 0 if completed == len(photos) else 1


if __name__ == "__main__":
    raise SystemExit(main())
