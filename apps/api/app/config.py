from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    ocr_provider: str
    tesseract_cmd: str | None
    ocr_timeout_seconds: float
    max_upload_bytes: int
    max_image_pixels: int
    cors_origins: tuple[str, ...]


@lru_cache
def get_settings() -> Settings:
    origins = tuple(
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    )
    return Settings(
        ocr_provider=os.getenv("OCR_PROVIDER", "tesseract").strip().lower(),
        tesseract_cmd=os.getenv("TESSERACT_CMD") or None,
        ocr_timeout_seconds=float(os.getenv("OCR_TIMEOUT_SECONDS", "8")),
        max_upload_bytes=int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024))),
        max_image_pixels=int(os.getenv("MAX_IMAGE_PIXELS", "40000000")),
        cors_origins=origins,
    )
