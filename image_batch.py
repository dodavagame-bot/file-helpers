#!/usr/bin/env python3
"""
Purpose: Resize and/or convert a batch of images with Pillow.
Example: python image_batch.py photos resized --max-size 1600 --format jpg
Warning: The output directory may contain replaced files; review the preview first.
"""

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Resize or convert images.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--max-size", type=int, help="Fit inside this width and height")
    parser.add_argument("--format", choices=("jpg", "jpeg", "png", "webp", "bmp"), help="Output format")
    parser.add_argument("--recursive", action="store_true", help="Include images in subdirectories")
    args = parser.parse_args()
    if not args.source.is_dir():
        parser.error(f"source directory does not exist: {args.source}")
    if not args.max_size and not args.format:
        parser.error("provide --max-size, --format, or both")
    if args.max_size is not None and args.max_size < 1:
        parser.error("--max-size must be positive")
    try:
        from PIL import Image
    except ImportError:
        print("This tool requires Pillow. Install it with: python -m pip install Pillow")
        return 1

    extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
    candidates = args.source.rglob("*") if args.recursive else args.source.iterdir()
    images = sorted(path for path in candidates if path.is_file() and path.suffix.lower() in extensions)
    if not images:
        print("No supported images found.")
        return 0

    suffix = f".{args.format}" if args.format else None
    plan = []
    for source in images:
        relative = source.relative_to(args.source)
        target = args.output / relative
        if suffix:
            target = target.with_suffix(suffix)
        plan.append((source, target))
    print("Planned image operations:")
    for source, target in plan:
        print(f"  {source} -> {target}")
    if input("Process these images? [y/N] ").strip().lower() not in {"y", "yes"}:
        print("Cancelled.")
        return 0

    converted = 0
    for source, target in plan:
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(source) as image:
                if args.max_size:
                    image.thumbnail((args.max_size, args.max_size), Image.Resampling.LANCZOS)
                save_image = image.convert("RGB") if target.suffix.lower() in {".jpg", ".jpeg"} else image
                save_image.save(target)
            converted += 1
        except (OSError, ValueError) as error:
            print(f"Failed to process {source}: {error}")
    print(f"Processed {converted} of {len(plan)} image(s).")
    return 0 if converted == len(plan) else 1


if __name__ == "__main__":
    raise SystemExit(main())
