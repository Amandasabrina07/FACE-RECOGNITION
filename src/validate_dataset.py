from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

import cv2

from common import DEFAULT_DATASET_DIR

FILENAME_PATTERN = re.compile(r"^User\.(\d+)\.(\d+)\.(?:jpg|jpeg|png)$", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate face-dataset files.")
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dataset_dir = args.dataset_dir.resolve()
    if not dataset_dir.exists():
        raise SystemExit(f"Dataset directory does not exist: {dataset_dir}")

    counts: Counter[int] = Counter()
    invalid_names: list[str] = []
    unreadable: list[str] = []
    empty_files: list[str] = []

    files = [path for path in sorted(dataset_dir.iterdir()) if path.is_file() and path.name != ".gitkeep"]
    for path in files:
        match = FILENAME_PATTERN.match(path.name)
        if not match:
            invalid_names.append(path.name)
            continue
        if path.stat().st_size == 0:
            empty_files.append(path.name)
            continue
        image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if image is None or image.size == 0:
            unreadable.append(path.name)
            continue
        counts[int(match.group(1))] += 1

    print(f"[INFO] Dataset: {dataset_dir}")
    print(f"[INFO] Files checked: {len(files)}")
    print(f"[INFO] Valid identities: {len(counts)}")
    for person_id, count in sorted(counts.items()):
        print(f"  ID {person_id}: {count} valid image(s)")

    if invalid_names:
        print(f"[WARN] Invalid file names: {len(invalid_names)}")
    if empty_files:
        print(f"[WARN] Empty files: {len(empty_files)}")
    if unreadable:
        print(f"[WARN] Unreadable images: {len(unreadable)}")

    has_errors = bool(invalid_names or empty_files or unreadable)
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
