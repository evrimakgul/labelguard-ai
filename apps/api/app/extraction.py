from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher

from app.models import (
    ExtractedField,
    ExtractedLabel,
    ExtractedWarning,
    LabelApplication,
    OCRLine,
    OCRResult,
)

CANONICAL_WARNING = (
    "GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink "
    "alcoholic beverages during pregnancy because of the risk of birth defects. "
    "(2) Consumption of alcoholic beverages impairs your ability to drive a car or operate "
    "machinery, and may cause health problems."
)

CLASS_KEYWORDS = re.compile(
    r"\b(bourbon|whisk(?:e)?y|vodka|gin|rum|brandy|liqueur|tequila|mezcal|spirits?|wine|"
    r"beer|ale|lager|stout|porter|vermouth|champagne)\b",
    re.IGNORECASE,
)
ABV_PATTERN = re.compile(
    r"(?P<value>\d{1,3}(?:\.\d+)?)\s*(?:%|percent)\s*"
    r"(?P<format>alc(?:ohol)?\.?\s*/?\s*vol(?:ume)?\.?|alcohol\s+by\s+volume|abv)?",
    re.IGNORECASE,
)
PROOF_PATTERN = re.compile(r"(?P<value>\d{1,3}(?:\.\d+)?)\s*proof\b", re.IGNORECASE)
VOLUME_PATTERN = re.compile(
    r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>m\s*l|lit(?:er|re)s?|l\b|fl\.?\s*oz\.?)",
    re.IGNORECASE,
)


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).replace("’", "'").replace("‘", "'")
    return " ".join(value.casefold().split())


def normalize_comparison_text(value: str) -> str:
    value = normalize_text(value)
    value = re.sub(r"[^\w\s']", " ", value)
    return " ".join(value.split())


def similarity(left: str, right: str) -> float:
    return SequenceMatcher(
        None, normalize_comparison_text(left), normalize_comparison_text(right)
    ).ratio()


def _line_confidence(line: OCRLine) -> float:
    return line.confidence if line.text.strip() else 0.0


def _best_line(
    expected: str,
    lines: list[OCRLine],
    *,
    class_field: bool,
) -> OCRLine | None:
    candidates = []
    for index, line in enumerate(lines):
        text = line.text.strip()
        lowered = text.casefold()
        if not text or "government warning" in lowered or "surgeon general" in lowered:
            continue
        if ABV_PATTERN.search(text) or PROOF_PATTERN.search(text) or VOLUME_PATTERN.search(text):
            continue
        has_class_keyword = bool(CLASS_KEYWORDS.search(text))
        if class_field and not has_class_keyword:
            continue
        if not class_field and has_class_keyword:
            continue
        score = similarity(expected, text)
        position_bonus = max(0.0, 0.08 - index * 0.01)
        candidates.append((score + position_bonus, line))
    if not candidates and class_field:
        candidates = [
            (similarity(expected, line.text), line)
            for line in lines
            if line.text.strip()
            and not ABV_PATTERN.search(line.text)
            and not VOLUME_PATTERN.search(line.text)
        ]
    return max(candidates, key=lambda item: item[0])[1] if candidates else None


def _extract_abv(lines: list[OCRLine]) -> ExtractedField:
    for line in lines:
        match = ABV_PATTERN.search(line.text)
        if not match:
            continue
        raw_format = (match.group("format") or "").casefold()
        if "abv" in raw_format:
            source = "abv_abbreviation"
        elif raw_format:
            source = "alc_vol"
        else:
            source = "percent_only"
        return ExtractedField(
            value=float(match.group("value")),
            raw_text=match.group(0),
            confidence=_line_confidence(line),
            bounding_box=line.bounding_box,
            source=source,
        )
    for line in lines:
        match = PROOF_PATTERN.search(line.text)
        if match:
            return ExtractedField(
                value=float(match.group("value")) / 2,
                raw_text=match.group(0),
                confidence=_line_confidence(line),
                bounding_box=line.bounding_box,
                source="proof_only",
            )
    return ExtractedField(value=None, raw_text=None, confidence=0, source=None)


def _extract_volume(lines: list[OCRLine]) -> ExtractedField:
    for line in lines:
        for match in VOLUME_PATTERN.finditer(line.text):
            value = float(match.group("value"))
            unit = re.sub(r"[\s.]", "", match.group("unit").casefold())
            if unit in {"l", "liter", "litre", "liters", "litres"}:
                milliliters = value * 1000
            elif unit == "floz":
                milliliters = value * 29.5735
            else:
                milliliters = value
            return ExtractedField(
                value=milliliters,
                raw_text=match.group(0),
                confidence=_line_confidence(line),
                bounding_box=line.bounding_box,
                source="volume",
            )
    return ExtractedField(value=None, raw_text=None, confidence=0, source=None)


def _warning_words(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.casefold())


def _extract_warning(ocr: OCRResult) -> ExtractedWarning:
    collapsed = " ".join(ocr.full_text.split())
    start_match = re.search(
        r"government\s+warning|according\s+to\s+the\s+surgeon\s+general", collapsed, re.I
    )
    if not start_match:
        return ExtractedWarning(
            found=False,
            text=None,
            confidence=0,
            heading_correct=None,
            wording_correct=None,
            punctuation_correct=None,
        )

    segment = collapsed[start_match.start() :]
    end_match = re.search(r"health\s+problems\s*[.!]?", segment, re.I)
    if end_match:
        segment = segment[: end_match.end()]
    heading_correct = bool(re.match(r"GOVERNMENT\s+WARNING\s*:", segment))
    wording_correct = _warning_words(segment) == _warning_words(CANONICAL_WARNING)
    punctuation_correct = normalize_text(segment) == normalize_text(CANONICAL_WARNING)
    relevant_lines = [
        line
        for line in ocr.lines
        if any(
            token in line.text.casefold()
            for token in ("government", "surgeon", "alcoholic", "health problems")
        )
    ]
    confidence = (
        sum(line.confidence for line in relevant_lines) / len(relevant_lines)
        if relevant_lines
        else 0.0
    )
    return ExtractedWarning(
        found=True,
        text=segment,
        confidence=confidence,
        heading_correct=heading_correct,
        wording_correct=wording_correct,
        punctuation_correct=punctuation_correct,
    )


def extract_label(ocr: OCRResult, application: LabelApplication) -> ExtractedLabel:
    brand_line = _best_line(application.brand_name, ocr.lines, class_field=False)
    class_line = _best_line(application.class_type, ocr.lines, class_field=True)
    brand = ExtractedField(
        value=brand_line.text if brand_line else None,
        raw_text=brand_line.text if brand_line else None,
        confidence=_line_confidence(brand_line) if brand_line else 0,
        bounding_box=brand_line.bounding_box if brand_line else None,
        source="ocr_line" if brand_line else None,
    )
    class_type = ExtractedField(
        value=class_line.text if class_line else None,
        raw_text=class_line.text if class_line else None,
        confidence=_line_confidence(class_line) if class_line else 0,
        bounding_box=class_line.bounding_box if class_line else None,
        source="ocr_line" if class_line else None,
    )
    return ExtractedLabel(
        full_text=ocr.full_text,
        brand_name=brand,
        class_type=class_type,
        alcohol_by_volume=_extract_abv(ocr.lines),
        net_contents=_extract_volume(ocr.lines),
        health_warning=_extract_warning(ocr),
    )
