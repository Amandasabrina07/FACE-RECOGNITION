from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

import cv2
import numpy as np

from common import DEFAULT_DATASET_DIR, DEFAULT_MODEL_PATH, require_lbph

FILENAME_PATTERN = re.compile(r"^User\.(\d+)\.(\d+)\.(?:jpg|jpeg|png)$", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train an OpenCV LBPH face recognizer.")
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR)
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument(
        "--detect-again",
        action="store_true",
        help="Run Haar detection on stored crops before training",
    )
    return parser.parse_args()


def load_training_samples(dataset_dir: Path, detect_again: bool):
    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    samples: list[np.ndarray] = []
    labels: list[int] = []
    skipped: list[str] = []

    for path in sorted(dataset_dir.iterdir()):
        if not path.is_file():
            continue
        match = FILENAME_PATTERN.match(path.name)
        if not match:
            skipped.append(path.name)
            continue

        image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if image is None or image.size == 0:
            skipped.append(path.name)
            continue

        person_id = int(match.group(1))

        if detect_again:
            faces = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=4)
            if len(faces) == 0:
                skipped.append(path.name)
                continue
            x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
            image = image[y : y + h, x : x + w]

        samples.append(image)
        labels.append(person_id)

    return samples, labels, skipped


def main() -> int:
    args = parse_args()
    dataset_dir = args.dataset_dir.resolve()
    model_path = args.model_path.resolve()

    if not dataset_dir.exists():
        raise SystemExit(f"Dataset directory does not exist: {dataset_dir}")

    samples, labels, skipped = load_training_samples(dataset_dir, args.detect_again)
    if not samples:
        raise SystemExit("No valid training images were found")

    recognizer = require_lbph(cv2)
    recognizer.train(samples, np.asarray(labels, dtype=np.int32))

    model_path.parent.mkdir(parents=True, exist_ok=True)
    recognizer.write(str(model_path))

    counts = Counter(labels)
    print(f"[INFO] Model written to: {model_path}")
    print(f"[INFO] Identities trained: {len(counts)}")
    for person_id, count in sorted(counts.items()):
        print(f"  ID {person_id}: {count} sample(s)")
    if skipped:
        print(f"[WARN] Skipped {len(skipped)} invalid or unmatched file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
