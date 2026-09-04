from __future__ import annotations

import io

import cv2
import numpy as np
import pytest
from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo

from app.image_validation import ValidatedImage
from app.preprocessing import estimate_deskew_angle, preprocess_image


def validated(content: bytes, width: int, height: int, image_format: str = "PNG"):
    content_type = "image/jpeg" if image_format == "JPEG" else "image/png"
    return ValidatedImage(content, content_type, width, height, image_format)


def test_exif_orientation_is_applied_and_metadata_removed() -> None:
    image = Image.new("RGB", (120, 80), "white")
    exif = image.getexif()
    exif[274] = 6
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", exif=exif)

    result = preprocess_image(validated(buffer.getvalue(), 120, 80, "JPEG"))

    assert (result.width, result.height) == (80, 120)
    assert "orientation_corrected" in result.applied_steps
    with Image.open(io.BytesIO(result.content)) as processed:
        assert processed.getexif().get(274) is None


def test_png_text_metadata_is_removed() -> None:
    metadata = PngInfo()
    metadata.add_text("private-note", "do not preserve")
    buffer = io.BytesIO()
    Image.new("RGB", (200, 100), "white").save(buffer, format="PNG", pnginfo=metadata)

    result = preprocess_image(validated(buffer.getvalue(), 200, 100))

    with Image.open(io.BytesIO(result.content)) as processed:
        assert "private-note" not in processed.info


def test_low_contrast_image_is_enhanced() -> None:
    image = Image.new("RGB", (300, 120), (125, 125, 125))
    ImageDraw.Draw(image).text((30, 45), "OLD TOM", fill=(138, 138, 138))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    result = preprocess_image(validated(buffer.getvalue(), 300, 120))

    assert "contrast_enhanced" in result.applied_steps


def test_estimate_deskew_angle_finds_small_corrective_rotation() -> None:
    canvas = np.full((260, 700), 255, dtype=np.uint8)
    for y in (70, 120, 170):
        cv2.line(canvas, (80, y), (620, y), 0, 8)
    matrix = cv2.getRotationMatrix2D((350, 130), 4.0, 1.0)
    skewed = cv2.warpAffine(canvas, matrix, (700, 260), borderValue=255)

    angle = estimate_deskew_angle(skewed)

    assert angle == pytest.approx(-4.0, abs=1.0)
