from __future__ import annotations

from app.extraction import CANONICAL_WARNING, extract_label
from app.models import LabelApplication, OCRLine, OCRResult, VerificationStatus
from app.verification import overall_status, verify_label, volume_to_ml


def make_application(brand: str = "Old Tom Distillery") -> LabelApplication:
    return LabelApplication.model_validate(
        {
            "brandName": brand,
            "classType": "Kentucky Straight Bourbon Whiskey",
            "alcoholByVolume": 45,
            "netContents": {"value": 750, "unit": "mL"},
        }
    )


def make_ocr(*lines: str, confidence: float = 0.99) -> OCRResult:
    return OCRResult(
        fullText="\n".join(lines),
        lines=[OCRLine(text=line, confidence=confidence) for line in lines],
        provider="test",
    )


def run_checks(*lines: str, confidence: float = 0.99):
    app = make_application()
    extracted = extract_label(make_ocr(*lines, confidence=confidence), app)
    return verify_label(app, extracted)


def status_for(checks, field: str) -> VerificationStatus:
    return next(check.status for check in checks if check.field == field)


def test_perfect_label_passes() -> None:
    checks = run_checks(
        "OLD TOM DISTILLERY",
        "Kentucky Straight Bourbon Whiskey",
        "45% Alc./Vol. (90 Proof)",
        "750 mL",
        CANONICAL_WARNING,
    )
    assert overall_status(checks) == VerificationStatus.PASS


def test_case_only_brand_difference_passes() -> None:
    checks = run_checks(
        "old tom distillery",
        "Kentucky Straight Bourbon Whiskey",
        "45% Alc./Vol.",
        "750 mL",
        CANONICAL_WARNING,
    )
    assert status_for(checks, "brandName") == VerificationStatus.PASS


def test_wrong_abv_and_missing_warning_produce_mismatch() -> None:
    checks = run_checks(
        "OLD TOM DISTILLERY",
        "Kentucky Straight Bourbon Whiskey",
        "40% Alc./Vol.",
        "750 mL",
    )
    assert status_for(checks, "alcoholByVolume") == VerificationStatus.MISMATCH
    assert status_for(checks, "healthWarning") == VerificationStatus.MISSING
    assert overall_status(checks) == VerificationStatus.MISMATCH


def test_low_confidence_never_auto_passes() -> None:
    checks = run_checks(
        "OLD TOM DISTILLERY",
        "Kentucky Straight Bourbon Whiskey",
        "45% Alc./Vol.",
        "750 mL",
        CANONICAL_WARNING,
        confidence=0.70,
    )
    assert overall_status(checks) == VerificationStatus.REVIEW
    assert all(
        check.status != VerificationStatus.PASS
        for check in checks
        if check.status != VerificationStatus.NOT_APPLICABLE
    )


def test_empty_ocr_requires_review_instead_of_false_pass() -> None:
    app = make_application()
    extracted = extract_label(make_ocr(), app)
    checks = verify_label(app, extracted)
    assert overall_status(checks) == VerificationStatus.REVIEW
    assert {check.status for check in checks} == {VerificationStatus.REVIEW}


def test_volume_conversions() -> None:
    assert volume_to_ml(0.75, "L") == 750
    assert round(volume_to_ml(12, "fl_oz"), 2) == 354.88
