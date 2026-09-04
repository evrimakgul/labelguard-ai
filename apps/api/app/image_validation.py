from __future__ import annotations

import io
from dataclasses import dataclass

from fastapi import HTTPException, status
from PIL import Image, UnidentifiedImageError

ALLOWED_CONTENT_TYPES = {"image/jpeg": "JPEG", "image/png": "PNG"}


@dataclass(frozen=True)
class ValidatedImage:
    content: bytes
    content_type: str
    width: int
    height: int
    format: str


def invalid_image(message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"code": "invalid_image", "message": message},
    )


def validate_image(
    content: bytes,
    declared_content_type: str | None,
    *,
    max_bytes: int,
    max_pixels: int,
) -> ValidatedImage:
    if not content:
        raise invalid_image("The selected file is empty. Choose a JPEG or PNG image.")
    if len(content) > max_bytes:
        raise invalid_image(
            f"The image is too large. The maximum size is {max_bytes // 1048576} MB."
        )
    if declared_content_type not in ALLOWED_CONTENT_TYPES:
        raise invalid_image("We could not read this file. Upload a JPEG or PNG image.")

    try:
        with Image.open(io.BytesIO(content)) as image:
            detected_format = image.format
            width, height = image.size
            image.verify()
    except (Image.DecompressionBombError, UnidentifiedImageError, OSError, ValueError):
        raise invalid_image(
            "We could not read this file. Upload a valid JPEG or PNG image."
        ) from None

    if detected_format not in {"JPEG", "PNG"}:
        raise invalid_image("We could not read this file. Upload a JPEG or PNG image.")
    if ALLOWED_CONTENT_TYPES[declared_content_type] != detected_format:
        raise invalid_image("The file type does not match the image contents.")
    if width < 50 or height < 50:
        raise invalid_image(
            "The image is too small to read. Use an image at least 50 by 50 pixels."
        )
    if width * height > max_pixels:
        raise invalid_image("The image dimensions are too large. Resize the image and try again.")

    return ValidatedImage(content, declared_content_type, width, height, detected_format)
