from __future__ import annotations

from fastapi import HTTPException, status

from app.config import get_settings
from app.ocr.base import OCRProvider
from app.ocr.demo import DemoOCRProvider
from app.ocr.tesseract import TesseractOCRProvider


def get_ocr_provider() -> OCRProvider:
    settings = get_settings()
    if settings.ocr_provider == "demo":
        return DemoOCRProvider()
    if settings.ocr_provider != "tesseract":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "ocr_configuration", "message": "The OCR provider is not configured."},
        )
    return TesseractOCRProvider(
        command=settings.tesseract_cmd,
        timeout_seconds=settings.ocr_timeout_seconds,
    )
