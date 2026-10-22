#!/usr/bin/env python3
"""
Purpose: Rename matching files to a numbered sequence.
Example: python batch_rename.py photos --pattern "*.jpg" --prefix trip-
Warning: Renaming changes filenames; review the preview before confirming.
"""

import argparse
import fnmatch
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rename files to a numbered sequence.")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--pattern", default="*", help="Filename pattern to match (default: *)")
    parser.add_argument("--prefix", default="file-", help="New filename prefix")
    parser.add_argument("--start", type=int, default=1, help="First number in the sequence")
    parser.add_argument("--digits", type=int, default=3, help="Minimum number width (default: 3)")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without renaming")
    return parser


def planned_renames(directory: Path, pattern: str, prefix: str, start: int, digits: int):
    files = sorted(
        (path for path in directory.iterdir() if path.is_file() and fnmatch.fnmatch(path.name, pattern)),
        key=lambda path: path.name.lower(),
    )
    return [
        (source, source.with_name(f"{prefix}{number:0{digits}d}{source.suffix}"))
        for number, source in enumerate(files, start=start)
    ]


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error(f"directory does not exist: {args.directory}")
    if args.start < 0 or args.digits < 1:
        parser.error("--start must be non-negative and --digits must be positive")

    renames = planned_renames(args.directory, args.pattern, args.prefix, args.start, args.digits)
    if not renames:
        print("No matching files found.")
        return 0

    print("Planned renames:")
    for source, target in renames:
        print(f"  {source.name} -> {target.name}")
    if args.dry_run:
        return 0

    targets = {target for _, target in renames}
    conflicts = [target for source, target in renames if target.exists() and target != source]
    if len(targets) != len(renames) or conflicts:
        print("Refusing to rename because one or more target names already exist.")
        return 1
    answer = input("Apply these renames? [y/N] ").strip().lower()
    if answer not in {"y", "yes"}:
        print("Cancelled.")
        return 0

    temporary = []
    try:
        for index, (source, target) in enumerate(renames):
            temporary_path = source.with_name(f".file_helpers_tmp_{index}_{source.name}")
            source.rename(temporary_path)
            temporary.append((temporary_path, target))
        for temporary_path, target in temporary:
            temporary_path.rename(target)
    except OSError as error:
        print(f"Rename failed: {error}")
        return 1
    print(f"Renamed {len(renames)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
