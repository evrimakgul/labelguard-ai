from __future__ import annotations

import io

from PIL import Image

from app.models import BoundingBox, OCRLine, OCRResult, OCRWord, Point

DEMO_LINES = (
    "OLD TOM DISTILLERY",
    "KENTUCKY STRAIGHT BOURBON WHISKEY",
    "45% ALC./VOL. (90 PROOF)",
    "750 mL",
    "GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink",
    "alcoholic beverages during pregnancy because of the risk of birth defects. (2) Consumption",
    "of alcoholic beverages impairs your ability to drive a car or operate machinery, "
    "and may cause health problems.",
)
DEMO_METADATA_KEY = "labelguard_ocr"


class DemoOCRProvider:
    """Reads embedded fixture text; never pretends to OCR arbitrary uploads."""

    async def extract(self, image: bytes, content_type: str) -> OCRResult:
        with Image.open(io.BytesIO(image)) as fixture:
            embedded_text = str(fixture.info.get(DEMO_METADATA_KEY, ""))
            width, height = fixture.size
        source_lines = tuple(line for line in embedded_text.splitlines() if line.strip())
        lines: list[OCRLine] = []
        for index, text in enumerate(source_lines):
            top = 100 + index * 105
            box = BoundingBox(
                points=[
                    Point(x=120, y=top),
                    Point(x=1080, y=top),
                    Point(x=1080, y=top + 64),
                    Point(x=120, y=top + 64),
                ]
            )
            words = [OCRWord(text=word, confidence=0.99, bounding_box=box) for word in text.split()]
            lines.append(OCRLine(text=text, confidence=0.99, bounding_box=box, words=words))
        return OCRResult(
            full_text="\n".join(source_lines),
            lines=lines,
            width=width,
            height=height,
            provider="demo-fixture",
        )
