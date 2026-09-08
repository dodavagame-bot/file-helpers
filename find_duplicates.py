#!/usr/bin/env python3
"""
Purpose: Find files with identical content using SHA-256 hashes.
Example: python find_duplicates.py ~/Downloads
Warning: This tool only reports duplicates; it never deletes files.
"""

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path


def file_hash(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Find duplicate files by content.")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--recursive", action="store_true", help="Search subdirectories")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error(f"directory does not exist: {args.directory}")

    paths = args.directory.rglob("*") if args.recursive else args.directory.iterdir()
    by_size = defaultdict(list)
    for path in paths:
        if path.is_file():
            try:
                by_size[path.stat().st_size].append(path)
            except OSError as error:
                print(f"Skipping {path}: {error}")

    duplicate_groups = 0
    for same_size in by_size.values():
        if len(same_size) < 2:
            continue
        by_hash = defaultdict(list)
        for path in same_size:
            try:
                by_hash[file_hash(path)].append(path)
            except OSError as error:
                print(f"Skipping {path}: {error}")
        for paths_with_same_content in by_hash.values():
            if len(paths_with_same_content) > 1:
                duplicate_groups += 1
                print("Duplicate group:")
                for path in sorted(paths_with_same_content):
                    print(f"  {path}")
    if duplicate_groups == 0:
        print("No duplicate files found.")
    else:
        print(f"Found {duplicate_groups} duplicate group(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
