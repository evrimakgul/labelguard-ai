from __future__ import annotations

import io
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image, ImageOps

from app.image_validation import ValidatedImage

MAX_OCR_EDGE = 3000
CONTRAST_STD_THRESHOLD = 45.0
MAX_DESKEW_DEGREES = 8.0
MIN_DESKEW_DEGREES = 0.75


@dataclass(frozen=True)
class ProcessedImage:
    content: bytes
    content_type: str
    width: int
    height: int
    applied_steps: tuple[str, ...]


def _rotate(image: np.ndarray, angle: float, border_value: int) -> np.ndarray:
    height, width = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1.0)
    return cv2.warpAffine(
        image,
        matrix,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border_value,
    )


def estimate_deskew_angle(gray: np.ndarray) -> float:
    """Return a bounded corrective rotation using horizontal projection scoring."""
    height, width = gray.shape
    scale = min(1.0, 800 / max(height, width))
    sample = (
        cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        if scale < 1
        else gray
    )
    margin_y = max(1, round(sample.shape[0] * 0.05))
    margin_x = max(1, round(sample.shape[1] * 0.05))
    sample = sample[margin_y:-margin_y, margin_x:-margin_x]
    _, binary = cv2.threshold(sample, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    ink_ratio = float(np.count_nonzero(binary)) / binary.size
    if ink_ratio < 0.002 or ink_ratio > 0.55:
        return 0.0

    best_angle = 0.0
    best_score = -1.0
    for angle in np.arange(-MAX_DESKEW_DEGREES, MAX_DESKEW_DEGREES + 0.1, 0.5):
        rotated = _rotate(binary, float(angle), 0)
        projection = np.sum(rotated, axis=1, dtype=np.float64)
        score = float(np.sum(np.diff(projection) ** 2))
        if score > best_score:
            best_score = score
            best_angle = float(angle)
    return best_angle if abs(best_angle) >= MIN_DESKEW_DEGREES else 0.0


def preprocess_image(validated: ValidatedImage) -> ProcessedImage:
    steps = ["metadata_removed"]
    with Image.open(io.BytesIO(validated.content)) as source:
        orientation = source.getexif().get(274)
        image = ImageOps.exif_transpose(source)
        if orientation not in (None, 1):
            steps.append("orientation_corrected")
        image = image.convert("RGB")

    width, height = image.size
    longest_edge = max(width, height)
    if longest_edge > MAX_OCR_EDGE:
        scale = MAX_OCR_EDGE / longest_edge
        image = image.resize(
            (max(1, round(width * scale)), max(1, round(height * scale))),
            Image.Resampling.LANCZOS,
        )
        width, height = image.size
        steps.append("resized_for_ocr")

    rgb = np.asarray(image)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    if float(np.std(gray)) < CONTRAST_STD_THRESHOLD:
        gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
        steps.append("contrast_enhanced")

    angle = estimate_deskew_angle(gray)
    if angle:
        gray = _rotate(gray, angle, 255)
        steps.append(f"deskewed_{angle:+.1f}_degrees")

    encoded, output = cv2.imencode(".png", gray, [cv2.IMWRITE_PNG_COMPRESSION, 6])
    if not encoded:
        raise ValueError("Image preprocessing could not encode the result.")
    return ProcessedImage(
        content=output.tobytes(),
        content_type="image/png",
        width=width,
        height=height,
        applied_steps=tuple(steps),
    )
