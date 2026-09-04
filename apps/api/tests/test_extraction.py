from __future__ import annotations

from app.extraction import CANONICAL_WARNING, extract_label, normalize_text, similarity
from app.models import LabelApplication, OCRLine, OCRResult


def application() -> LabelApplication:
    return LabelApplication.model_validate(
        {
            "brandName": "Stone's Throw",
            "classType": "Kentucky Straight Bourbon Whiskey",
            "alcoholByVolume": 45,
            "netContents": {"value": 750, "unit": "mL"},
        }
    )


def ocr_from_lines(*values: str, confidence: float = 0.99) -> OCRResult:
    return OCRResult(
        fullText="\n".join(values),
        lines=[OCRLine(text=value, confidence=confidence) for value in values],
        provider="test",
    )


def test_normalize_text_handles_case_whitespace_and_typographic_apostrophe() -> None:
    assert normalize_text("  STONE’S   THROW ") == "stone's throw"
    assert similarity("Stone's Throw", "STONE’S THROW") == 1


def test_extracts_expected_fields_and_normalizes_liters() -> None:
    result = extract_label(
        ocr_from_lines(
            "STONE'S THROW",
            "KENTUCKY STRAIGHT BOURBON WHISKEY",
            "45% Alc./Vol. (90 Proof)",
            "0.75 L",
            CANONICAL_WARNING,
        ),
        application(),
    )

    assert result.brand_name.value == "STONE'S THROW"
    assert result.class_type.value == "KENTUCKY STRAIGHT BOURBON WHISKEY"
    assert result.alcohol_by_volume.value == 45
    assert result.alcohol_by_volume.source == "alc_vol"
    assert result.net_contents.value == 750
    assert result.health_warning.heading_correct is True
    assert result.health_warning.wording_correct is True
    assert result.health_warning.punctuation_correct is True


def test_proof_is_converted_to_abv_but_marked_as_proof_only() -> None:
    result = extract_label(
        ocr_from_lines("STONE'S THROW", "BOURBON WHISKEY", "90 Proof", "750 mL"),
        application(),
    )
    assert result.alcohol_by_volume.value == 45
    assert result.alcohol_by_volume.source == "proof_only"


def test_warning_heading_case_and_punctuation_are_independent() -> None:
    warning = CANONICAL_WARNING.replace("GOVERNMENT WARNING", "Government Warning").replace(
        "machinery,", "machinery"
    )
    result = extract_label(ocr_from_lines(warning), application())
    assert result.health_warning.found is True
    assert result.health_warning.heading_correct is False
    assert result.health_warning.wording_correct is True
    assert result.health_warning.punctuation_correct is False


def test_producer_statement_is_not_used_as_missing_brand() -> None:
    result = extract_label(
        ocr_from_lines(
            "KENTUCKY STRAIGHT BOURBON WHISKEY",
            "45% Alc./Vol.",
            "750 mL",
            "DISTILLED AND BOTTLED IN THE USA",
            CANONICAL_WARNING,
        ),
        application(),
    )

    assert result.brand_name.value is None


def test_brand_keyword_supports_confident_wrong_brand_detection() -> None:
    result = extract_label(
        ocr_from_lines(
            "ACME SPIRITS",
            "KENTUCKY STRAIGHT BOURBON WHISKEY",
            "45% Alc./Vol.",
            "750 mL",
            CANONICAL_WARNING,
        ),
        application(),
    )

    assert result.brand_name.value == "ACME SPIRITS"


def test_distilled_spirits_class_is_not_treated_as_a_producer_statement() -> None:
    app = application().model_copy(update={"class_type": "Distilled Spirits"})
    result = extract_label(
        ocr_from_lines("STONE'S THROW", "DISTILLED SPIRITS", "45% Alc./Vol.", "750 mL"),
        app,
    )

    assert result.class_type.value == "DISTILLED SPIRITS"
