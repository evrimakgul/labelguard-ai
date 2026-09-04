from __future__ import annotations

import json

from app.main import app
from app.models import OCRResult
from app.ocr.base import OCRProviderError
from app.ocr.demo import DemoOCRProvider
from app.ocr.factory import get_ocr_provider


class EmptyProvider:
    async def extract(self, image: bytes, content_type: str) -> OCRResult:
        return OCRResult(fullText="", lines=[], provider="test-empty")


class FailingProvider:
    async def extract(self, image: bytes, content_type: str) -> OCRResult:
        raise OCRProviderError("secret upstream details")


def test_health(client) -> None:
    assert client.get("/api/health").json() == {"status": "ok"}


def test_verify_multipart_success(client, png_bytes, application_payload) -> None:
    app.dependency_overrides[get_ocr_provider] = DemoOCRProvider
    response = client.post(
        "/api/v1/verify",
        data={"application": json.dumps(application_payload)},
        files={"image": ("demo.png", png_bytes, "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["overallStatus"] == "pass"
    assert body["ocrProvider"] == "demo-fixture"
    assert body["requestId"].startswith("req_")
    assert "metadata_removed" in body["image"]["processingSteps"]
    assert any("Demo OCR mode" in warning for warning in body["warnings"])


def test_invalid_image_has_friendly_error(client, application_payload) -> None:
    app.dependency_overrides[get_ocr_provider] = DemoOCRProvider
    response = client.post(
        "/api/v1/verify",
        data={"application": json.dumps(application_payload)},
        files={"image": ("not-an-image.png", b"not an image", "image/png")},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_image"
    assert "Traceback" not in response.text


def test_ocr_failure_does_not_expose_provider_details(
    client, png_bytes, application_payload
) -> None:
    app.dependency_overrides[get_ocr_provider] = FailingProvider
    response = client.post(
        "/api/v1/verify",
        data={"application": json.dumps(application_payload)},
        files={"image": ("demo.png", png_bytes, "image/png")},
    )
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "ocr_unavailable"
    assert "secret upstream details" not in response.text


def test_unreadable_image_returns_review(client, png_bytes, application_payload) -> None:
    app.dependency_overrides[get_ocr_provider] = EmptyProvider
    response = client.post(
        "/api/v1/verify",
        data={"application": json.dumps(application_payload)},
        files={"image": ("blank.png", png_bytes, "image/png")},
    )
    assert response.status_code == 200
    assert response.json()["overallStatus"] == "review"
