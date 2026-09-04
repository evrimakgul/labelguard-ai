"""Measure the complete local API pipeline with the installed Tesseract runtime."""

from __future__ import annotations

import json
import logging
import statistics
import time
from pathlib import Path

from app.main import app
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "labels" / "demo-pass.png"
APPLICATION = {
    "brandName": "OLD TOM DISTILLERY",
    "classType": "Kentucky Straight Bourbon Whiskey",
    "alcoholByVolume": 45,
    "netContents": {"value": 750, "unit": "mL"},
}


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * fraction)))
    return ordered[index]


def main() -> None:
    logging.disable(logging.CRITICAL)
    wall_times: list[float] = []
    api_times: list[float] = []
    ocr_times: list[float] = []
    try:
        with TestClient(app) as client:
            for _ in range(20):
                started = time.perf_counter()
                with FIXTURE.open("rb") as image:
                    response = client.post(
                        "/api/v1/verify",
                        data={"application": json.dumps(APPLICATION)},
                        files={"image": (FIXTURE.name, image, "image/png")},
                    )
                response.raise_for_status()
                result = response.json()
                if result["overallStatus"] != "pass":
                    raise RuntimeError(
                        "Live benchmark fixture did not pass verification."
                    )
                if result["ocrProvider"] != "local-tesseract":
                    raise RuntimeError("Live benchmark did not use local Tesseract.")
                wall_times.append((time.perf_counter() - started) * 1000)
                api_times.append(float(result["processingTimeMs"]))
                ocr_times.append(float(result["stageTimingsMs"]["ocrMs"]))
    finally:
        logging.disable(logging.NOTSET)

    print(
        json.dumps(
            {
                "mode": "local-tesseract",
                "requests": len(wall_times),
                "wallMedianMs": round(statistics.median(wall_times), 1),
                "wallP95Ms": round(percentile(wall_times, 0.95), 1),
                "apiMedianMs": round(statistics.median(api_times), 1),
                "apiP95Ms": round(percentile(api_times, 0.95), 1),
                "ocrMedianMs": round(statistics.median(ocr_times), 1),
                "ocrP95Ms": round(percentile(ocr_times, 0.95), 1),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
