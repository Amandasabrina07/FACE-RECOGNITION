from __future__ import annotations

import argparse
import urllib.error
import urllib.request
from pathlib import Path

import cv2
import numpy as np

from common import (
    DEFAULT_MODEL_PATH,
    DEFAULT_PEOPLE_PATH,
    get_camera_url,
    load_people,
    require_lbph,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recognize faces from an ESP32-CAM JPEG endpoint using LBPH."
    )
    parser.add_argument("--camera-url", help="Example: http://192.168.1.120/capture")
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--people", type=Path, default=DEFAULT_PEOPLE_PATH)
    parser.add_argument(
        "--threshold",
        type=float,
        default=60.0,
        help="Maximum LBPH prediction distance accepted as a known identity",
    )
    parser.add_argument("--timeout", type=float, default=5.0)
    return parser.parse_args()


def fetch_frame(url: str, timeout: float) -> np.ndarray:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        payload = response.read()
    frame = cv2.imdecode(np.frombuffer(payload, dtype=np.uint8), cv2.IMREAD_COLOR)
    if frame is None:
        raise RuntimeError("ESP32-CAM returned an unreadable JPEG frame")
    return frame


def main() -> int:
    args = parse_args()
    camera_url = get_camera_url(args.camera_url)
    model_path = args.model_path.resolve()
    people_path = args.people.resolve()

    if not model_path.exists():
        raise SystemExit(f"Model not found: {model_path}. Run train_model.py first.")

    recognizer = require_lbph(cv2)
    recognizer.read(str(model_path))
    people = load_people(people_path)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    if detector.empty():
        raise RuntimeError("Failed to load OpenCV frontal-face Haar cascade")

    print(f"[INFO] Camera: {camera_url}")
    print(f"[INFO] Model: {model_path}")
    print(f"[INFO] Known labels loaded: {len(people)}")
    print("[INFO] Press Esc or q to exit.")

    try:
        while True:
            try:
                frame = fetch_frame(camera_url, args.timeout)
            except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
                print(f"[WARN] Frame request failed: {exc}")
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(60, 60),
            )

            for x, y, w, h in faces:
                predicted_id, distance = recognizer.predict(gray[y : y + h, x : x + w])
                known = distance <= args.threshold
                label = people.get(predicted_id, f"ID {predicted_id}") if known else "Unknown"

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(
                    frame,
                    label,
                    (x, max(20, y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                )
                cv2.putText(
                    frame,
                    f"LBPH distance: {distance:.1f}",
                    (x, y + h + 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    1,
                )

            cv2.imshow("ESP32-CAM Face Recognition", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q")):
                break
    finally:
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
