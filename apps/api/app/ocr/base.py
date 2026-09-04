from __future__ import annotations

from typing import Protocol

from app.models import OCRResult


class OCRProviderError(RuntimeError):
    """Raised when an OCR provider cannot return a usable result."""


class OCRProvider(Protocol):
    async def extract(self, image: bytes, content_type: str) -> OCRResult: ...
