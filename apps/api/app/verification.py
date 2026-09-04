from __future__ import annotations

from app.extraction import CANONICAL_WARNING, normalize_comparison_text, similarity
from app.models import (
    ExtractedField,
    ExtractedLabel,
    LabelApplication,
    VerificationCheck,
    VerificationStatus,
    VolumeUnit,
)

AUTO_CONFIDENCE = 0.80


def volume_to_ml(value: float, unit: VolumeUnit) -> float:
    if unit == VolumeUnit.LITERS:
        return value * 1000
    if unit == VolumeUnit.FLUID_OUNCES:
        return value * 29.5735
    return value


def _text_check(
    *,
    field: str,
    label: str,
    expected: str,
    extracted: ExtractedField,
) -> VerificationCheck:
    detected = str(extracted.value) if extracted.value is not None else None
    if detected is None:
        return VerificationCheck(
            field=field,
            label=label,
            group="Application checks",
            status=VerificationStatus.MISSING,
            expected=expected,
            explanation=f"{label} was not detected on the label.",
        )
    score = similarity(expected, detected)
    if extracted.confidence < AUTO_CONFIDENCE:
        return VerificationCheck(
            field=field,
            label=label,
            group="Application checks",
            status=VerificationStatus.REVIEW,
            expected=expected,
            detected=detected,
            confidence=extracted.confidence,
            explanation="OCR confidence is too low for an automatic decision.",
            bounding_box=extracted.bounding_box,
        )
    if normalize_comparison_text(expected) == normalize_comparison_text(detected):
        status = VerificationStatus.PASS
        explanation = f"{label} matches after case, spacing, and punctuation normalization."
    elif score >= 0.95:
        status = VerificationStatus.PASS
        explanation = f"{label} is equivalent after normalization ({score:.0%} similarity)."
    elif score >= 0.85:
        status = VerificationStatus.REVIEW
        explanation = f"{label} is close but not exact ({score:.0%} similarity). Review the image."
    else:
        status = VerificationStatus.MISMATCH
        explanation = (
            f"Detected {label.lower()} does not match the application ({score:.0%} similarity)."
        )
    return VerificationCheck(
        field=field,
        label=label,
        group="Application checks",
        status=status,
        expected=expected,
        detected=detected,
        confidence=extracted.confidence,
        explanation=explanation,
        bounding_box=extracted.bounding_box,
    )


def _numeric_check(
    *,
    field: str,
    label: str,
    expected: float,
    expected_display: str,
    extracted: ExtractedField,
    tolerance: float,
) -> VerificationCheck:
    if extracted.value is None:
        return VerificationCheck(
            field=field,
            label=label,
            group="Application checks",
            status=VerificationStatus.MISSING,
            expected=expected_display,
            explanation=f"{label} was not detected on the label.",
        )
    detected_value = float(extracted.value)
    if extracted.confidence < AUTO_CONFIDENCE:
        status = VerificationStatus.REVIEW
        explanation = "OCR confidence is too low for an automatic decision."
    elif abs(expected - detected_value) <= tolerance:
        status = VerificationStatus.PASS
        explanation = f"{label} matches the application value."
    else:
        status = VerificationStatus.MISMATCH
        explanation = f"Detected {label.lower()} differs from the application value."
    return VerificationCheck(
        field=field,
        label=label,
        group="Application checks",
        status=status,
        expected=expected_display,
        detected=extracted.raw_text,
        confidence=extracted.confidence,
        explanation=explanation,
        bounding_box=extracted.bounding_box,
    )


def _warning_checks(extracted: ExtractedLabel) -> list[VerificationCheck]:
    warning = extracted.health_warning
    if not warning.found:
        missing = VerificationCheck(
            field="healthWarning",
            label="Government health warning",
            group="Label requirements",
            status=VerificationStatus.MISSING,
            expected=CANONICAL_WARNING,
            explanation="The mandatory Government Health Warning was not detected.",
        )
        return [missing]
    low_confidence = warning.confidence < AUTO_CONFIDENCE
    heading_status = (
        VerificationStatus.REVIEW
        if low_confidence
        else VerificationStatus.PASS
        if warning.heading_correct
        else VerificationStatus.MISMATCH
    )
    wording_status = (
        VerificationStatus.REVIEW
        if low_confidence
        else VerificationStatus.PASS
        if warning.wording_correct
        else VerificationStatus.MISMATCH
    )
    punctuation_status = (
        VerificationStatus.REVIEW
        if low_confidence
        else VerificationStatus.PASS
        if warning.punctuation_correct
        else VerificationStatus.MISMATCH
    )
    return [
        VerificationCheck(
            field="healthWarningHeading",
            label="Warning heading",
            group="Label requirements",
            status=heading_status,
            expected="GOVERNMENT WARNING:",
            detected=(warning.text or "")[:24],
            confidence=warning.confidence,
            explanation=(
                "OCR confidence is too low to confirm the heading."
                if low_confidence
                else "The warning heading is uppercase and includes the required colon."
                if warning.heading_correct
                else "The warning heading must be uppercase and include the required colon."
            ),
        ),
        VerificationCheck(
            field="healthWarningWording",
            label="Warning wording",
            group="Label requirements",
            status=wording_status,
            expected=CANONICAL_WARNING,
            detected=warning.text,
            confidence=warning.confidence,
            explanation=(
                "OCR confidence is too low to confirm the required wording."
                if low_confidence
                else "All required warning words are present in the required order."
                if warning.wording_correct
                else "The warning wording differs from the mandatory statement."
            ),
        ),
        VerificationCheck(
            field="healthWarningPunctuation",
            label="Warning punctuation",
            group="Label requirements",
            status=punctuation_status,
            expected="Required colon, parentheses, comma, and periods",
            detected=warning.text,
            confidence=warning.confidence,
            explanation=(
                "OCR confidence is too low to confirm punctuation."
                if low_confidence
                else "Warning punctuation matches the mandatory statement."
                if warning.punctuation_correct
                else "One or more punctuation marks or spaces differ from the mandatory statement."
            ),
        ),
        VerificationCheck(
            field="warningTypography",
            label="Warning typography and type size",
            group="Label requirements",
            status=VerificationStatus.NOT_APPLICABLE,
            detected=None,
            explanation=(
                "Not automatically evaluated: OCR does not reliably prove bold styling "
                "or physical type size."
            ),
        ),
    ]


def verify_label(
    application: LabelApplication, extracted: ExtractedLabel
) -> list[VerificationCheck]:
    if not extracted.full_text.strip():
        return [
            VerificationCheck(
                field=field,
                label=label,
                group=group,
                status=VerificationStatus.REVIEW,
                explanation=(
                    "The image did not contain enough readable text. Manual review is recommended."
                ),
            )
            for field, label, group in (
                ("brandName", "Brand name", "Application checks"),
                ("classType", "Class / type", "Application checks"),
                ("alcoholByVolume", "Alcohol content", "Application checks"),
                ("netContents", "Net contents", "Application checks"),
                ("healthWarning", "Government health warning", "Label requirements"),
            )
        ]

    expected_ml = volume_to_ml(application.net_contents.value, application.net_contents.unit)
    checks = [
        _text_check(
            field="brandName",
            label="Brand name",
            expected=application.brand_name,
            extracted=extracted.brand_name,
        ),
        _text_check(
            field="classType",
            label="Class / type",
            expected=application.class_type,
            extracted=extracted.class_type,
        ),
        _numeric_check(
            field="alcoholByVolume",
            label="Alcohol content",
            expected=application.alcohol_by_volume,
            expected_display=f"{application.alcohol_by_volume:g}% Alc./Vol.",
            extracted=extracted.alcohol_by_volume,
            tolerance=0.05,
        ),
        _numeric_check(
            field="netContents",
            label="Net contents",
            expected=expected_ml,
            expected_display=(
                f"{application.net_contents.value:g} {application.net_contents.unit.value}"
            ),
            extracted=extracted.net_contents,
            tolerance=1.0,
        ),
    ]
    if (
        extracted.alcohol_by_volume.value is not None
        and extracted.alcohol_by_volume.confidence >= AUTO_CONFIDENCE
    ):
        format_ok = extracted.alcohol_by_volume.source == "alc_vol"
        checks.append(
            VerificationCheck(
                field="alcoholFormat",
                label="Alcohol statement format",
                group="Label requirements",
                status=VerificationStatus.PASS if format_ok else VerificationStatus.REVIEW,
                expected="Percent alcohol by volume statement",
                detected=extracted.alcohol_by_volume.raw_text,
                confidence=extracted.alcohol_by_volume.confidence,
                explanation=(
                    "The detected statement uses an alcohol-by-volume form."
                    if format_ok
                    else (
                        "The value was detected, but the mandatory statement format "
                        "needs manual review."
                    )
                ),
                bounding_box=extracted.alcohol_by_volume.bounding_box,
            )
        )
    checks.extend(_warning_checks(extracted))
    return checks


def overall_status(checks: list[VerificationCheck]) -> VerificationStatus:
    statuses = {check.status for check in checks}
    if VerificationStatus.MISMATCH in statuses or VerificationStatus.MISSING in statuses:
        return VerificationStatus.MISMATCH
    if VerificationStatus.REVIEW in statuses:
        return VerificationStatus.REVIEW
    return VerificationStatus.PASS
