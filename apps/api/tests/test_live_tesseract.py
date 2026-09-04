from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import VerificationStatus
from app.ocr.factory import get_ocr_provider
from app.ocr.tesseract import TesseractOCRProvider

FIXTURE_DIR = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "labels"
RUN_LIVE_OCR = os.getenv("RUN_LIVE_OCR") == "1"


APPLICATION = {
    "brandName": "OLD TOM DISTILLERY",
    "classType": "Kentucky Straight Bourbon Whiskey",
    "alcoholByVolume": 45,
    "netContents": {"value": 750, "unit": "mL"},
}


@pytest.mark.live_ocr
@pytest.mark.skipif(
    not RUN_LIVE_OCR or shutil.which("tesseract") is None,
    reason="set RUN_LIVE_OCR=1 on a machine with Tesseract to run live OCR acceptance",
)
@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        ("demo-pass.png", VerificationStatus.PASS),
        ("demo-brand-mismatch.png", VerificationStatus.MISMATCH),
        ("demo-abv-mismatch.png", VerificationStatus.MISMATCH),
        ("demo-warning-error.png", VerificationStatus.MISMATCH),
        ("demo-rotated.png", VerificationStatus.PASS),
        ("demo-low-contrast.png", VerificationStatus.PASS),
        ("demo-unreadable.png", VerificationStatus.REVIEW),
    ],
)
def test_live_tesseract_acceptance(
    client: TestClient, filename: str, expected: VerificationStatus
) -> None:
    content = (FIXTURE_DIR / filename).read_bytes()
    app.dependency_overrides[get_ocr_provider] = TesseractOCRProvider
    response = client.post(
        "/api/v1/verify",
        data={"application": json.dumps(APPLICATION)},
        files={"image": (filename, content, "image/png")},
    )

    assert response.status_code == 200
    assert response.json()["ocrProvider"] == "local-tesseract"
    assert response.json()["overallStatus"] == expected.value
