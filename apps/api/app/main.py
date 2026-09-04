from __future__ import annotations

import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from app.config import get_settings
from app.extraction import extract_label
from app.image_validation import validate_image
from app.models import ImageMetadata, LabelApplication, StageTimings, VerificationResponse
from app.ocr.base import OCRProvider, OCRProviderError
from app.ocr.demo import DemoOCRProvider
from app.ocr.factory import get_ocr_provider
from app.preprocessing import preprocess_image
from app.verification import overall_status, verify_label

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(message)s")
logger = logging.getLogger("labelguard")
settings = get_settings()

app = FastAPI(
    title="LabelGuard AI API",
    version="0.1.0",
    description="Decision-support API for comparing alcohol labels with application data.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Request-ID"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    detail = (
        exc.detail
        if isinstance(exc.detail, dict)
        else {"code": "request_error", "message": str(exc.detail)}
    )
    return JSONResponse(status_code=exc.status_code, content={"error": detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, __: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "invalid_request",
                "message": "Check the application fields and try again.",
            }
        },
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("unexpected_error", exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "internal_error",
                "message": "The request could not be completed. Try again.",
            }
        },
    )


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/verify", response_model=VerificationResponse, response_model_by_alias=True)
async def verify_single_label(
    application: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
    provider: Annotated[OCRProvider, Depends(get_ocr_provider)],
) -> VerificationResponse:
    request_id = f"req_{uuid.uuid4().hex[:12]}"
    started = time.perf_counter()
    try:
        parsed_application = LabelApplication.model_validate_json(application)
    except (ValidationError, ValueError, json.JSONDecodeError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": "invalid_application",
                "message": "Check the application fields and try again.",
            },
        ) from None

    image_started = time.perf_counter()
    content = await image.read(settings.max_upload_bytes + 1)
    validated = validate_image(
        content,
        image.content_type,
        max_bytes=settings.max_upload_bytes,
        max_pixels=settings.max_image_pixels,
    )
    processed = preprocess_image(validated)
    image_ms = round((time.perf_counter() - image_started) * 1000)

    ocr_started = time.perf_counter()
    try:
        if isinstance(provider, DemoOCRProvider):
            ocr_result = await provider.extract(validated.content, validated.content_type)
        else:
            ocr_result = await provider.extract(processed.content, processed.content_type)
    except OCRProviderError as exc:
        logger.warning(
            json.dumps({"request_id": request_id, "event": "ocr_error", "reason": str(exc)})
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "code": "ocr_unavailable",
                "message": (
                    "The label could not be processed. Try again; "
                    "your application data was not lost."
                ),
            },
        ) from None
    ocr_ms = round((time.perf_counter() - ocr_started) * 1000)

    extraction_started = time.perf_counter()
    extracted = extract_label(ocr_result, parsed_application)
    extraction_ms = round((time.perf_counter() - extraction_started) * 1000)

    verification_started = time.perf_counter()
    checks = verify_label(parsed_application, extracted)
    result_status = overall_status(checks)
    verification_ms = round((time.perf_counter() - verification_started) * 1000)
    total_ms = round((time.perf_counter() - started) * 1000)
    warnings = [
        "This tool supports human review and does not issue a regulatory decision.",
        "Bold styling and physical type size are not automatically verified.",
    ]
    if ocr_result.provider == "demo-fixture":
        warnings.insert(
            0,
            "Demo OCR mode is active; the included fixture text is being used instead of live OCR.",
        )

    logger.info(
        json.dumps(
            {
                "request_id": request_id,
                "event": "verification_complete",
                "duration_ms": total_ms,
                "ocr_ms": ocr_ms,
                "result": result_status.value,
                "checks": len(checks),
            }
        )
    )
    return VerificationResponse(
        request_id=request_id,
        overall_status=result_status,
        processing_time_ms=total_ms,
        checks=checks,
        warnings=warnings,
        extracted_text=ocr_result.full_text,
        ocr_provider=ocr_result.provider,
        image=ImageMetadata(
            width=processed.width,
            height=processed.height,
            format=validated.format,
            processing_steps=list(processed.applied_steps),
        ),
        stage_timings_ms=StageTimings(
            image_prepare_ms=image_ms,
            ocr_ms=ocr_ms,
            field_extract_ms=extraction_ms,
            verification_ms=verification_ms,
        ),
    )


static_dir = Path(os.getenv("STATIC_DIR", Path(__file__).parent / "static"))
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="web")
