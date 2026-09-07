# LabelGuard AI

LabelGuard AI is a standalone decision-support prototype that compares U.S. alcohol label artwork with application data and explains every automated check.

## Live Demo

The application runs locally without a paid service. The OCI image, container process, internal health endpoint, and direct machine-address health pass; Windows IPv4 loopback forwarding remains unavailable under Podman 6/WSL. A public host has intentionally not been selected; any future host must provide public HTTPS without billing information, a payment method, credits, or a paid subscription.

## Current Status

P0/P1 core implementation, local/container acceptance, and [GitHub Actions](https://github.com/evrimakgul/labelguard-ai/actions/runs/34085317594) pass. [Source code](https://github.com/evrimakgul/labelguard-ai) is published following user authorization. The verified local application was at `http://192.168.70.113:8001` (refresh after restart). Public hosting and deployment still require a qualifying host and separate approval. See [project status](docs/PROJECT_STATUS.md), [deployment procedures](docs/deployment.md), and [user decisions](docs/USER_REQUIREMENTS.md).

## Problem

Compliance agents repeatedly compare brand, class/type, alcohol content, net contents, and the mandatory Government Health Warning by eye. Slow or opaque automation would add work instead of reducing it.

## Solution

The application provides one obvious workflow: enter expected values, upload a JPEG or PNG, select **Verify Label**, and review Pass, Mismatch, Missing, or Needs Review results with detected evidence and confidence.

LabelGuard AI does not approve or reject a COLA application. It preserves human judgment for uncertain and image-dependent requirements.

![LabelGuard AI real container verification](docs/screenshots/container-desktop.png)

## Features

- Single-label application form and drag-and-drop image upload
- MIME, encoding, size, and pixel-count validation
- Local Tesseract OCR behind a provider protocol
- Deterministic brand, class/type, ABV, proof, net-content, and warning rules
- Exact Government Health Warning heading, wording, and punctuation checks
- Confidence-aware results that never auto-pass low-confidence OCR
- Clickable image evidence, explanations, stage timings, structured logs, and safe errors
- EXIF orientation correction, resize safeguards, adaptive contrast, and bounded deskew
- One-click demo application loader
- Deterministic demo provider and downloadable test labels
- Responsive, keyboard-accessible UI with status words in addition to color
- Portable Docker packaging and GitHub Actions CI

## Architecture

```mermaid
flowchart LR
    B[Next.js browser UI] -->|multipart request| A[FastAPI]
    A --> I[Image validation]
    I --> O[OCR provider protocol]
    O --> T[Local Tesseract process]
    O --> D[Fixture-only demo provider]
    O --> E[Field extraction]
    E --> V[Deterministic verification]
    V --> R[Explainable result]
    R --> B
```

The Next.js application is statically built and served by FastAPI in production, giving evaluators one endpoint. OCR runs inside the same machine or container, with no API key or paid cloud dependency. See [architecture](docs/architecture.md).

## Verification Logic

- Text is Unicode-, case-, whitespace-, punctuation-, and apostrophe-normalized before comparison.
- Exact normalized matches pass. Text similarity of 95% or higher passes, 85–94% needs review, and lower similarity mismatches.
- ABV is parsed from alcohol-by-volume statements; proof is converted with `proof / 2`, but proof-only or `ABV`-only formatting needs review.
- Net contents are converted to milliliters (`L`, `mL`, and `fl oz`) before numeric comparison.
- OCR confidence below 80% needs review and never automatically passes.
- A mismatch or missing required field makes the overall result Mismatch; otherwise any review makes it Needs Review.

## Government Warning Validation

The canonical statement is maintained once in the backend. Heading capitalization, required words, and punctuation are reported separately. Bold styling and physical type size are explicitly not evaluated because OCR output and an unscaled photograph cannot prove them reliably.

The implementation follows the [TTB Health Warning guidance](https://www.ttb.gov/regulated-commodities/beverage-alcohol/distilled-spirits/ds-labeling-home/ds-health-warning).

## Technology Choices

- Next.js 16, React 19, and TypeScript for a compact accessible interface
- FastAPI, Pydantic, Pillow, OpenCV, Tesseract, and pytesseract for typed requests, preprocessing, and local OCR
- Pytest, Ruff, Vitest, Testing Library, ESLint, and TypeScript for quality gates
- One multi-stage container for portable deployment on any qualifying host

The OCR provider protocol keeps image reading separate from regulatory verification and allows future local engines without changing the rules.

## Local Setup

Prerequisites: Node.js 22+, npm 10+, Python 3.12+, and Tesseract 5 with English language data. Docker is optional and already includes Tesseract.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e '.\apps\api[dev]'
Set-Location apps\web
npm ci
```

On macOS/Linux, activate `.venv/bin/python` and use forward-slash paths.

Install Tesseract locally using the [official installation guidance](https://tesseract-ocr.github.io/tessdoc/Installation.html). On Windows, add the installation directory to `PATH` or set `TESSERACT_CMD` to the full executable path.

## Environment Variables

Copy `.env.example` to `.env` and set:

- `OCR_PROVIDER=tesseract` for normal operation or `demo` for bundled fixtures only
- `TESSERACT_CMD` only when the executable is not on `PATH`
- `OCR_TIMEOUT_SECONDS` (defaults to 8)
- `NEXT_PUBLIC_API_URL=http://localhost:8000` for split local development

No OCR credentials are needed. Do not commit local machine-specific configuration. The backend does not automatically load `.env`; the commands below set environment variables explicitly. To load the repository-root `.env` instead, add `--env-file .env` to the root-level uvicorn command. Next.js reads configuration in its own application directory.

## Run Locally

Start the API:

```powershell
$env:OCR_PROVIDER='tesseract'
.\.venv\Scripts\uvicorn app.main:app --app-dir apps\api --reload --port 8000
```

Start the UI in a second terminal:

```powershell
Set-Location apps\web
$env:NEXT_PUBLIC_API_URL='http://localhost:8000'
npm run dev
```

Open `http://localhost:3000`. If Tesseract is not installed, use `OCR_PROVIDER=demo` with repository fixtures; demo OCR only reads their embedded text, and an arbitrary upload returns Needs Review instead of invented text.

## Run Tests

```powershell
.\.venv\Scripts\ruff check apps\api\app apps\api\tests scripts
.\.venv\Scripts\ruff format --check apps\api\app apps\api\tests scripts
.\.venv\Scripts\pytest apps\api
$env:RUN_LIVE_OCR='1'
.\.venv\Scripts\pytest apps\api\tests\test_live_tesseract.py
Remove-Item Env:RUN_LIVE_OCR

Set-Location apps\web
npm run lint
npm run typecheck
npm test
npm run build
```

## OCI Container

```powershell
podman build --tag labelguard-ai:local .
podman run --rm --publish 8000:8000 labelguard-ai:local
```

The image installs Tesseract and English language data. No host OCR installation, credentials, or paid service is required. Final image build, real OCR API cases, desktop/mobile browser flows and error recovery pass. Reproduce acceptance with `.venv/Scripts/python scripts/verify_container.py --base-url <running-container-url>`; see [deployment procedures](docs/deployment.md) for current container names, ports, and Windows networking.

## Deployment

The project deliberately does not select a final host yet. Its single Linux container can run on any platform that meets all of these constraints:

- public HTTPS URL
- no billing information or payment method
- no prepaid credits
- no paid subscription
- enough CPU and memory for local Tesseract

See [portable deployment guidance](docs/deployment.md). No external resources are created by this repository.

## Performance

The response reports image-preparation, OCR, extraction, verification, and total timings. On this Windows development host, 20 fixture-mode requests measured a 136.2 ms wall median and 169.0 ms p95 (131.5 ms/164.0 ms API-reported). Run `.venv/Scripts/python scripts/benchmark_demo.py` to reproduce it.

After live OCR correction, 20 production-mode requests on the same host measured a 682.8 ms wall median and 737.6 ms p95 (679.0 ms/734.0 ms API-reported; 546.5 ms/565.0 ms OCR stage). Run `.venv/Scripts/python scripts/benchmark_live_ocr.py` to reproduce it. These host-specific fixture measurements are evidence for the warm target, not a guarantee for arbitrary artwork or deployment hardware.

Final Linux container benchmark (2026-09-06): 20 sequential pass-fixture requests after warmup, wall median **648.9 ms**, nearest-rank p95 **694.6 ms**; API median/p95 645.0/691 ms and OCR 528.0/557 ms. This measures the local WSL container, not public-host latency or varied real-world artwork. The container verifier reports every expected case and rejects unexpected results.

## Test Data

Download or upload the fixtures under [`tests/fixtures/labels`](tests/fixtures/labels):

- `demo-pass.png`
- `demo-brand-mismatch.png`
- `demo-abv-mismatch.png`
- `demo-warning-error.png`
- `demo-rotated.png`
- `demo-low-contrast.png`
- `demo-unreadable.png`

Regenerate them with `.venv/Scripts/python scripts/generate_demo_labels.py`.

For the fastest evaluation, select **Load demo application**, download the demo label from the upload panel, upload it, and select **Verify Label**.

## Assumptions

See [docs/assumptions.md](docs/assumptions.md).

## Known Limitations

See [docs/limitations.md](docs/limitations.md).

## Security and Privacy

Uploads are size- and format-validated, processed in memory, and not retained. The service does not log image bytes, complete OCR text, application values, or secrets. Production OCR calls occur server-side and use timeouts. No database is included.

## Future Improvements

- Evaluate additional free, local OCR engines behind the existing provider protocol
- Validate style and physical type size when reliable scale/font evidence is available
- Add beverage-specific and same-field-of-vision rules
- Add bounded-concurrency batch workflows only after the single-label system remains stable
