from __future__ import annotations

import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from PIL.PngImagePlugin import PngInfo

from app.main import app
from app.ocr.demo import DEMO_LINES, DEMO_METADATA_KEY


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def png_bytes() -> bytes:
    buffer = io.BytesIO()
    metadata = PngInfo()
    metadata.add_text(DEMO_METADATA_KEY, "\n".join(DEMO_LINES))
    Image.new("RGB", (200, 200), "white").save(buffer, format="PNG", pnginfo=metadata)
    return buffer.getvalue()


@pytest.fixture
def application_payload() -> dict:
    return {
        "applicationId": "COLA-001",
        "beverageType": "distilled_spirits",
        "brandName": "Old Tom Distillery",
        "classType": "Kentucky Straight Bourbon Whiskey",
        "alcoholByVolume": 45,
        "netContents": {"value": 750, "unit": "mL"},
    }
