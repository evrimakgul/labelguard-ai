# Architecture

## Runtime shape

LabelGuard AI deploys as one container. A multi-stage build exports the Next.js client and copies it into the FastAPI image. FastAPI serves both the static UI and `/api/*`, while Tesseract OCR runs locally in the same container.

Local development runs Next.js on port 3000 and FastAPI on 8000. CORS is limited to configured origins.

## Request flow

1. The browser serializes typed application data and sends one JPEG or PNG as multipart form data.
2. FastAPI validates the JSON, declared MIME type, decoded image format, byte size, dimensions, and pixel count.
3. Preprocessing applies EXIF orientation, metadata removal, bounded resizing, adaptive contrast, and small-angle deskewing.
4. The configured local Tesseract provider returns vendor-neutral lines, words, confidences, and polygons.
5. Field extraction parses ABV, proof, and volume and selects brand/class candidates without regulatory decisions.
6. Verification applies deterministic normalization, thresholds, numeric comparisons, and the canonical warning rules.
7. The API returns explanations, confidence, evidence geometry, processing steps, and stage timings.

## Concern boundaries

| Concern | Module |
| --- | --- |
| Configuration | `apps/api/app/config.py` |
| Image validation | `apps/api/app/image_validation.py` |
| Image preprocessing | `apps/api/app/preprocessing.py` |
| OCR protocol/providers | `apps/api/app/ocr/` |
| Field extraction | `apps/api/app/extraction.py` |
| Normalization and verification | `apps/api/app/verification.py` |
| HTTP and structured logging | `apps/api/app/main.py` |
| Result presentation | `apps/web/src/components/` |

The verification layer imports no Tesseract code. Tests inject providers through FastAPI dependency overrides.

## Engineering constraints migrated from AGENTS

Default stack: Next.js/React/TypeScript, FastAPI/Python, Pillow and OpenCV only as needed, pytest and appropriate TypeScript tests. Use Playwright when end-to-end coverage adds value. Keep Docker/OCI packaging and GitHub Actions; GitHub source control uses `main` as the primary branch. Change the stack only for a strong documented technical reason.

Keep image validation, preprocessing, OCR, extraction, normalization, verification, and presentation separate. OCR contains no regulatory rules; verification has no provider dependency. The OCRProvider interface is specified in SPEC section 3.8; its implementation is in `apps/api/app/ocr/base.py`.

Do not introduce a database without a real requirement, queues for the basic prototype, unnecessary infrastructure, microservices without clear value, or an LLM for deterministic comparisons. A working core takes priority over optional complexity.

Product copy must never say `TTB Approved`, `Application Approved`, or `Regulatory Approval Granted`. Use `Verification complete`, `All automated checks passed`, `Mismatch detected`, `Manual review required`, or `Needs review`, consistent with SPEC and human decision support.

## Security boundaries

- No database or durable upload storage
- No OCR API keys or paid service credentials
- Strict image size and type checks
- Generic client errors; upstream details stay in structured server logs
- Provider-neutral container suitable for a qualifying HTTPS host
- Non-root container runtime
