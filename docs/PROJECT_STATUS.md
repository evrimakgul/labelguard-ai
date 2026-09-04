# Project Status

Updated: 2026-09-04

## Milestones

- P0 implementation committed locally as `d9dd867` (`feat: implement local single-label verification`).
- P1 implementation committed locally as `37c66f9` (`feat: add image robustness and evidence`).
- Deterministic P0/P1 gates pass, but live Tesseract acceptance found a P0 correctness defect. P0 acceptance is reopened; existing P1 work is retained but frozen until the defect is fixed.
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

## Completed external setup

- Tesseract `5.5.3.20260724` is installed and available from PowerShell.
- Tesseract language data includes `eng` and `osd`.
- Podman `6.0.2` is installed. `podman-machine-default` runs under WSL2 in rootless mode, and `podman info` succeeds.
- GitHub CLI authentication is active through the operating-system keyring. No token is stored in `.env` or Git.

## Live Tesseract evidence

On 2026-09-04, Codex ran the real Tesseract provider through the API against the pass, rotated, low-contrast, and unreadable fixtures.

- All requests completed with HTTP 200 in 457–823 ms.
- The pass, rotated, and low-contrast fixtures incorrectly returned Mismatch because Tesseract omitted `OLD TOM DISTILLERY`; field extraction then selected `DISTILLED AND BOTTLED IN THE USA` as the brand.
- The unreadable fixture returned Mismatch after sparse false OCR plus missing required fields; the intended product behavior is Needs Review for an unreadable image.
- A live benchmark is deferred until correctness is restored. The existing 20-request fixture benchmark is not live OCR evidence.

## Current gate and ownership

### Codex next

1. Diagnose and fix live Tesseract brand detection/segmentation.
2. Prevent an implausible fallback line from becoming a confident brand mismatch when the brand was not read.
3. Restore Needs Review behavior for genuinely unreadable images.
4. Add regression tests and rerun live local OCR acceptance.

### User next

Send Codex the instruction `Fix and verify the live Tesseract acceptance blockers documented in PROJECT_STATUS.md.` No PowerShell command is required before that remediation. After Codex marks live OCR acceptance green, run the documented Podman build/run block in `USER_REQUIREMENTS.md` and return its complete output.

## Remaining delivery path

1. Codex fixes and revalidates live local OCR.
2. User builds and starts the OCI container with Podman and returns the requested output.
3. Codex verifies Tesseract and application behavior inside the running container, benchmarks live OCR, runs all automated gates, and updates README evidence.
4. Codex performs repository/secrets/CI readiness review.
5. The temporary no-push gate is lifted only after local and container acceptance pass.
6. A qualifying no-cost public host is selected, explicitly authorized, deployed, and verified over HTTPS.
7. README receives the source URL, public URL, final timings, and final limitations before Treasury submission.

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
