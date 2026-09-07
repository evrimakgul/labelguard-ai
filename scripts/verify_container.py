"""Exercise a running production API without shell JSON quoting or fake OCR."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
CASES = {
    "demo-pass.png": "pass",
    "demo-brand-mismatch.png": "mismatch",
    "demo-abv-mismatch.png": "mismatch",
    "demo-warning-error.png": "mismatch",
    "demo-rotated.png": "pass",
    "demo-low-contrast.png": "pass",
    "demo-unreadable.png": "review",
}


def verify(base_url: str, benchmark_requests: int) -> dict:
    application = (FIXTURES / "demo-application.json").read_text(encoding="utf-8")
    json.loads(application)
    results: list[dict] = []
    with httpx.Client(base_url=base_url, timeout=20, trust_env=False) as client:
        health = client.get("/api/health")
        health.raise_for_status()
        assert health.json() == {"status": "ok"}
        root = client.get("/")
        root.raise_for_status()
        assert "LabelGuard" in root.text
        favicon = client.get("/favicon.svg")
        favicon.raise_for_status()

        def post(image: bytes, payload: str = application) -> httpx.Response:
            return client.post(
                "/api/v1/verify",
                data={"application": payload},
                files={"image": ("label.png", image, "image/png")},
            )

        for filename, expected in CASES.items():
            response = post((FIXTURES / "labels" / filename).read_bytes())
            response.raise_for_status()
            body = response.json()
            assert body["overallStatus"] == expected, (filename, body)
            assert body["ocrProvider"] == "local-tesseract", body
            assert not any("Demo OCR mode" in warning for warning in body["warnings"])
            if filename == "demo-brand-mismatch.png":
                brand = next(c for c in body["checks"] if c["field"] == "brandName")
                assert brand["status"] == "mismatch"
                assert brand["detected"] == "ACME SPIRITS"
            results.append(
                {"case": filename, "status": expected, "ms": body["processingTimeMs"]}
            )

        invalid_image = post(b"not an image")
        assert invalid_image.status_code == 400
        assert invalid_image.json()["error"]["code"] == "invalid_image"
        invalid_application = post(b"not an image", '{brandName:"unquoted key"}')
        assert invalid_application.status_code == 422
        assert invalid_application.json()["error"]["code"] == "invalid_application"
        for response in (invalid_image, invalid_application):
            assert "Traceback" not in response.text

        image = (FIXTURES / "labels" / "demo-pass.png").read_bytes()
        wall_times, api_times, ocr_times = [], [], []
        for _ in range(benchmark_requests):
            started = time.perf_counter()
            response = post(image)
            wall_times.append((time.perf_counter() - started) * 1000)
            response.raise_for_status()
            body = response.json()
            assert body["overallStatus"] == "pass"
            assert body["ocrProvider"] == "local-tesseract"
            api_times.append(body["processingTimeMs"])
            ocr_times.append(body["stageTimingsMs"]["ocrMs"])

    def stats(values: list[float]) -> dict:
        return {
            "medianMs": round(statistics.median(values), 1),
            "p95Ms": round(sorted(values)[math.ceil(len(values) * 0.95) - 1], 1),
        }

    return {
        "baseUrl": base_url,
        "provider": "local-tesseract",
        "cases": results,
        "errors": {"invalidImage": 400, "invalidApplication": 422},
        "benchmark": {
            "requests": benchmark_requests,
            "fixture": "demo-pass.png",
            "percentileMethod": "nearest-rank",
            "wall": stats(wall_times),
            "api": stats(api_times),
            "ocr": stats(ocr_times),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--requests", type=int, default=20)
    args = parser.parse_args()
    if args.requests < 1:
        parser.error("--requests must be positive")
    print(json.dumps(verify(args.base_url, args.requests), indent=2))


if __name__ == "__main__":
    main()
