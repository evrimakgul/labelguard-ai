from __future__ import annotations

import asyncio
import io
import statistics
from collections import defaultdict

import pytesseract
from PIL import Image
from pytesseract import Output

from app.models import BoundingBox, OCRLine, OCRResult, OCRWord, Point
from app.ocr.base import OCRProviderError


class TesseractOCRProvider:
    """Local Tesseract OCR adapter with vendor-neutral output models."""

    def __init__(self, command: str | None = None, timeout_seconds: float = 8):
        if command:
            pytesseract.pytesseract.tesseract_cmd = command
        self.timeout_seconds = timeout_seconds

    async def extract(self, image: bytes, content_type: str) -> OCRResult:
        try:
            return await asyncio.to_thread(self._extract_sync, image)
        except pytesseract.TesseractNotFoundError as exc:
            raise OCRProviderError(
                "Tesseract is not installed or TESSERACT_CMD is incorrect."
            ) from exc
        except RuntimeError as exc:
            raise OCRProviderError("Local OCR timed out.") from exc
        except (pytesseract.TesseractError, OSError, ValueError) as exc:
            raise OCRProviderError("Local OCR could not process the image.") from exc

    def _extract_sync(self, image: bytes) -> OCRResult:
        with Image.open(io.BytesIO(image)) as source:
            prepared = source.convert("RGB")
            width, height = prepared.size
            data = pytesseract.image_to_data(
                prepared,
                lang="eng",
                config="--oem 3 --psm 6",
                output_type=Output.DICT,
                timeout=self.timeout_seconds,
            )

        grouped: dict[tuple[int, int, int, int], list[OCRWord]] = defaultdict(list)
        for index, raw_text in enumerate(data["text"]):
            text = str(raw_text).strip()
            raw_confidence = float(data["conf"][index])
            if not text or raw_confidence < 0:
                continue
            left = float(data["left"][index])
            top = float(data["top"][index])
            word_width = float(data["width"][index])
            word_height = float(data["height"][index])
            box = self._rectangle(left, top, word_width, word_height)
            key = (
                int(data["page_num"][index]),
                int(data["block_num"][index]),
                int(data["par_num"][index]),
                int(data["line_num"][index]),
            )
            grouped[key].append(
                OCRWord(
                    text=text,
                    confidence=min(raw_confidence / 100, 1),
                    bounding_box=box,
                )
            )

        lines = [self._make_line(words) for words in grouped.values()]
        return OCRResult(
            full_text="\n".join(line.text for line in lines),
            lines=lines,
            width=width,
            height=height,
            provider="local-tesseract",
        )

    @classmethod
    def _make_line(cls, words: list[OCRWord]) -> OCRLine:
        points = [
            point
            for word in words
            if word.bounding_box is not None
            for point in word.bounding_box.points
        ]
        left = min(point.x for point in points)
        top = min(point.y for point in points)
        right = max(point.x for point in points)
        bottom = max(point.y for point in points)
        return OCRLine(
            text=" ".join(word.text for word in words),
            confidence=statistics.fmean(word.confidence for word in words),
            bounding_box=cls._rectangle(left, top, right - left, bottom - top),
            words=words,
        )

    @staticmethod
    def _rectangle(left: float, top: float, width: float, height: float) -> BoundingBox:
        return BoundingBox(
            points=[
                Point(x=left, y=top),
                Point(x=left + width, y=top),
                Point(x=left + width, y=top + height),
                Point(x=left, y=top + height),
            ]
        )
