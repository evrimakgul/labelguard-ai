# Project Status

Updated: 2026-09-04

## Milestones

- P0 complete and committed locally as `d9dd867` (`feat: implement local single-label verification`).
- P1 implemented and verified: preprocessing, confidence, bounding-box evidence, demo loading, timing, and regression fixtures.
- P2 intentionally deferred.

## Current architecture

- Next.js/React/TypeScript interface exported as static assets
- FastAPI/Python API serving the interface and verification endpoint
- Local Tesseract as the default production OCR provider
- Fixture-only demo provider for deterministic tests and demonstrations
- Pillow/OpenCV preprocessing and deterministic verification rules
- One portable OCI container with Tesseract English data included
- No database, paid OCR API, cloud subscription, or application secret

## Verified quality gates

- Backend: Ruff lint and format checks; 30 pytest tests
- Frontend: ESLint, TypeScript, 6 Vitest tests, and production build
- Browser: pass, mismatch, unreadable, invalid-image, evidence selection, processing detail, and 390 px mobile checks
- Browser console: no warnings, errors, framework overlay, or horizontal mobile overflow
- Fixture pipeline benchmark: 20 requests, 136.2 ms wall median and 169.0 ms p95; excludes live Tesseract
- Active-source paid-platform scan: clean outside the unchanged Treasury assignment

## External validation still required

- Install Tesseract on Windows to run and benchmark live local OCR.
- Install Podman to build and run the OCI image locally; neither Podman nor Docker is currently installed.
- Select a public host only if it meets every no-cost/no-billing requirement in `USER_REQUIREMENTS.md`.
- GitHub CLI authentication is invalid, but this does not affect local work or commits.

## Standard commands

```powershell
.\.venv\Scripts\ruff check apps\api\app apps\api\tests scripts
.\.venv\Scripts\ruff format --check apps\api\app apps\api\tests scripts
.\.venv\Scripts\pytest apps\api
Set-Location apps\web
npm run lint
npm run typecheck
npm test
npm run build
```
