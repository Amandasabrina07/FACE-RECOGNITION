from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_DIR = PROJECT_ROOT / "data" / "dataset"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "trainer.yml"
DEFAULT_PEOPLE_PATH = PROJECT_ROOT / "config" / "people.json"


def get_camera_url(cli_value: str | None) -> str:
    """Resolve the ESP32-CAM JPEG capture URL from CLI or environment."""
    value = cli_value or os.getenv("ESP32CAM_CAPTURE_URL")
    if not value:
        raise ValueError(
            "Camera URL is required. Pass --camera-url or set "
            "ESP32CAM_CAPTURE_URL, for example "
            "http://192.168.1.120/capture"
        )
    return value.rstrip("/")


def load_people(path: Path) -> Dict[int, str]:
    """Load a JSON mapping such as {\"1\": \"Person One\"}."""
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)

    people: Dict[int, str] = {}
    for key, value in raw.items():
        try:
            person_id = int(key)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid person ID in {path}: {key!r}") from exc
        people[person_id] = str(value)
    return people


def require_lbph(cv2_module):
    """Return an LBPH recognizer or raise a clear dependency error."""
    if not hasattr(cv2_module, "face"):
        raise RuntimeError(
            "cv2.face is unavailable. Install opencv-contrib-python and remove "
            "conflicting opencv-python installations if necessary."
        )
    return cv2_module.face.LBPHFaceRecognizer_create()
