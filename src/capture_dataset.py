from __future__ import annotations

import argparse
import time
import urllib.error
import urllib.request
from pathlib import Path

import cv2
import numpy as np

from common import DEFAULT_DATASET_DIR, get_camera_url


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture face crops from an ESP32-CAM JPEG endpoint."
    )
    parser.add_argument("--camera-url", help="Example: http://192.168.1.120/capture")
    parser.add_argument("--user-id", type=int, required=True, help="Positive numeric identity")
    parser.add_argument("--count", type=int, default=30, help="Number of face images to save")
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=DEFAULT_DATASET_DIR,
        help="Directory used to store face crops",
    )
    parser.add_argument("--delay", type=float, default=0.12, help="Delay between requests")
    parser.add_argument("--timeout", type=float, default=5.0, help="HTTP timeout in seconds")
    parser.add_argument("--no-display", action="store_true", help="Run without an OpenCV window")
    return parser.parse_args()


def fetch_frame(url: str, timeout: float) -> np.ndarray:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        payload = response.read()
    array = np.frombuffer(payload, dtype=np.uint8)
    frame = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if frame is None:
        raise RuntimeError("ESP32-CAM returned an unreadable JPEG frame")
    return frame


def main() -> int:
    args = parse_args()
    if args.user_id <= 0:
        raise SystemExit("--user-id must be a positive integer")
    if args.count <= 0:
        raise SystemExit("--count must be greater than zero")

    camera_url = get_camera_url(args.camera_url)
    dataset_dir = args.dataset_dir.resolve()
    dataset_dir.mkdir(parents=True, exist_ok=True)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    if detector.empty():
        raise RuntimeError("Failed to load OpenCV frontal-face Haar cascade")

    saved = 0
    print(f"[INFO] Camera: {camera_url}")
    print(f"[INFO] Dataset: {dataset_dir}")
    print(f"[INFO] Capturing user ID {args.user_id}. Press Esc or q to stop.")

    try:
        while saved < args.count:
            time.sleep(max(args.delay, 0.0))
            try:
                frame = fetch_frame(camera_url, args.timeout)
            except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
                print(f"[WARN] Frame request failed: {exc}")
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60, 60),
            )

            if len(faces):
                # Save one face per frame. Prefer the largest detection.
                x, y, w, h = max(faces, key=lambda box: box[2] * box[3])
                saved += 1
                output = dataset_dir / f"User.{args.user_id}.{saved}.jpg"
                cv2.imwrite(str(output), gray[y : y + h, x : x + w])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                print(f"[INFO] Saved {saved}/{args.count}: {output.name}")

            if not args.no_display:
                cv2.putText(
                    frame,
                    f"Saved: {saved}/{args.count}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                )
                cv2.imshow("ESP32-CAM Dataset Capture", frame)
                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q")):
                    break
    finally:
        cv2.destroyAllWindows()

    print(f"[INFO] Finished. Saved {saved} face image(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
