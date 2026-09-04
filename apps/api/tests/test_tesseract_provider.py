from __future__ import annotations

import pytesseract
import pytest

from app.ocr.base import OCRProviderError
from app.ocr.tesseract import TesseractOCRProvider

OCR_DATA = {
    "text": ["OLD", "TOM", "45%"],
    "conf": ["98", "96", "94"],
    "left": [10, 55, 10],
    "top": [10, 10, 40],
    "width": [40, 35, 30],
    "height": [20, 20, 20],
    "page_num": [1, 1, 1],
    "block_num": [1, 1, 1],
    "par_num": [1, 1, 1],
    "line_num": [1, 1, 2],
}


@pytest.mark.asyncio
async def test_tesseract_maps_words_confidence_lines_and_boxes(
    monkeypatch: pytest.MonkeyPatch, png_bytes: bytes
) -> None:
    monkeypatch.setattr(pytesseract, "image_to_data", lambda *args, **kwargs: OCR_DATA)
    result = await TesseractOCRProvider().extract(png_bytes, "image/png")

    assert result.provider == "local-tesseract"
    assert result.full_text == "OLD TOM\n45%"
    assert result.lines[0].confidence == pytest.approx(0.97)
    assert result.lines[0].bounding_box is not None
    assert result.lines[0].bounding_box.points[2].x == 90
    assert result.width == 200


@pytest.mark.asyncio
async def test_missing_tesseract_becomes_provider_error(
    monkeypatch: pytest.MonkeyPatch, png_bytes: bytes
) -> None:
    def not_installed(*args, **kwargs):
        raise pytesseract.TesseractNotFoundError()

    monkeypatch.setattr(pytesseract, "image_to_data", not_installed)
    with pytest.raises(OCRProviderError, match="not installed"):
        await TesseractOCRProvider().extract(png_bytes, "image/png")
