from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


def to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.title() for part in parts[1:])


class APIModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class BeverageType(StrEnum):
    DISTILLED_SPIRITS = "distilled_spirits"
    WINE = "wine"
    MALT_BEVERAGE = "malt_beverage"


class VolumeUnit(StrEnum):
    MILLILITERS = "mL"
    LITERS = "L"
    FLUID_OUNCES = "fl_oz"


class Volume(APIModel):
    value: float = Field(gt=0)
    unit: VolumeUnit


class LabelApplication(APIModel):
    application_id: str | None = Field(default=None, max_length=100)
    beverage_type: BeverageType = BeverageType.DISTILLED_SPIRITS
    brand_name: str = Field(min_length=1, max_length=200)
    class_type: str = Field(min_length=1, max_length=200)
    alcohol_by_volume: float = Field(gt=0, le=100)
    net_contents: Volume

    @field_validator("brand_name", "class_type")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value


class Point(APIModel):
    x: float
    y: float


class BoundingBox(APIModel):
    points: list[Point] = Field(min_length=4, max_length=4)


class OCRWord(APIModel):
    text: str
    confidence: float = Field(ge=0, le=1)
    bounding_box: BoundingBox | None = None


class OCRLine(APIModel):
    text: str
    confidence: float = Field(ge=0, le=1)
    bounding_box: BoundingBox | None = None
    words: list[OCRWord] = Field(default_factory=list)


class OCRResult(APIModel):
    full_text: str
    lines: list[OCRLine]
    width: int | None = None
    height: int | None = None
    provider: str


class ExtractedField(APIModel):
    value: str | float | None
    raw_text: str | None
    confidence: float = Field(ge=0, le=1)
    bounding_box: BoundingBox | None = None
    source: str | None = None


class ExtractedWarning(APIModel):
    found: bool
    text: str | None
    confidence: float = Field(ge=0, le=1)
    heading_correct: bool | None
    wording_correct: bool | None
    punctuation_correct: bool | None


class ExtractedLabel(APIModel):
    full_text: str
    brand_name: ExtractedField
    class_type: ExtractedField
    alcohol_by_volume: ExtractedField
    net_contents: ExtractedField
    health_warning: ExtractedWarning


class VerificationStatus(StrEnum):
    PASS = "pass"
    MISMATCH = "mismatch"
    MISSING = "missing"
    REVIEW = "review"
    NOT_APPLICABLE = "not_applicable"


class VerificationCheck(APIModel):
    field: str
    label: str
    group: str
    status: VerificationStatus
    expected: str | None = None
    detected: str | None = None
    confidence: float | None = None
    explanation: str
    bounding_box: BoundingBox | None = None


class StageTimings(APIModel):
    image_prepare_ms: int
    ocr_ms: int
    field_extract_ms: int
    verification_ms: int


class ImageMetadata(APIModel):
    width: int
    height: int
    format: str


class VerificationResponse(APIModel):
    request_id: str
    overall_status: VerificationStatus
    processing_time_ms: int
    checks: list[VerificationCheck]
    warnings: list[str]
    extracted_text: str
    ocr_provider: str
    image: ImageMetadata
    stage_timings_ms: StageTimings


class ErrorBody(APIModel):
    code: str
    message: str


class ErrorResponse(APIModel):
    error: ErrorBody
