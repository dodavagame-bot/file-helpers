# file-helpers

Small Python 3 command-line tools for everyday file jobs. Each command prints a
preview before it changes or moves files.

## Tools

### `batch_rename.py`
Renames matching files to a numbered sequence, preserving their extensions.
Use `--dry-run` to review the planned names without changing anything.

### `find_duplicates.py`
Finds files with identical SHA-256 content, optionally through subdirectories.
It only reports duplicate groups and never deletes files.

### `image_batch.py`
Resizes images, converts formats, or does both using Pillow.
Install Pillow with `python -m pip install Pillow` before using it.

### `strip_photo_metadata.py`
Writes photo copies without EXIF metadata such as GPS location and camera data.
Install Pillow with `python -m pip install Pillow`; originals are left untouched.

### `sort_downloads.py`
Moves files into folders such as `images`, `documents`, and `archives` based on
extension. Use `--dry-run` to review the move plan first.

### `search_pdfs.py`
Searches PDF text case-insensitively and reports matching page numbers.
Install pypdf with `python -m pip install pypdf`; scanned PDFs need OCR first.
