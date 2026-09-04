from __future__ import annotations

from pathlib import Path

import pytest

from app.extraction import extract_label
from app.models import LabelApplication, VerificationStatus
from app.ocr.demo import DemoOCRProvider
from app.verification import overall_status, verify_label

FIXTURE_DIR = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "labels"


def application() -> LabelApplication:
    return LabelApplication.model_validate(
        {
            "brandName": "OLD TOM DISTILLERY",
            "classType": "Kentucky Straight Bourbon Whiskey",
            "alcoholByVolume": 45,
            "netContents": {"value": 750, "unit": "mL"},
        }
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
@pytest.mark.asyncio
async def test_fixture_regressions(filename: str, expected: VerificationStatus) -> None:
    image = (FIXTURE_DIR / filename).read_bytes()
    ocr = await DemoOCRProvider().extract(image, "image/png")
    extracted = extract_label(ocr, application())
    assert overall_status(verify_label(application(), extracted)) == expected


@pytest.mark.asyncio
async def test_demo_provider_does_not_invent_text_for_arbitrary_image(png_bytes: bytes) -> None:
    # Strip the fixture metadata by opening and re-saving through Pillow.
    import io

    from PIL import Image

    buffer = io.BytesIO()
    with Image.open(io.BytesIO(png_bytes)) as image:
        image.save(buffer, format="PNG")
    result = await DemoOCRProvider().extract(buffer.getvalue(), "image/png")
    assert result.full_text == ""
