# Project Status

Updated: 2026-09-04

## Milestones

- P0 implementation committed locally as `d9dd867` (`feat: implement local single-label verification`).
- P1 implementation committed locally as `37c66f9` (`feat: add image robustness and evidence`).
- P0/P1 deterministic gates and live Windows Tesseract acceptance pass. The OCI image build passed; remaining acceptance is container startup and health.
- Podman built `labelguard-ai:local` successfully. The container remains running, and its internal health endpoint returns `{"status":"ok"}`. Windows IPv4 port 8000 is refused while only `::1:8000` is listening, isolating the active gate to Podman/WSL host forwarding.
- The `::1:8000` listener is `wslrelay.exe`. WSL is `2.7.12.0`; the first machine-address lookup was inconclusive because the minimal Podman machine has no `hostname` executable.
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

- Backend: Ruff lint and format checks; 35 deterministic pytest tests
- Live OCR: 7 opt-in Tesseract acceptance cases covering pass, mismatch, rotation, contrast, warning, and unreadable behavior
- Frontend: ESLint, TypeScript, 6 Vitest tests, and production build
- Browser: pass, mismatch, unreadable, invalid-image, evidence selection, processing detail, and 390 px mobile checks
- Browser console: no warnings, errors, framework overlay, or horizontal mobile overflow
- Fixture pipeline benchmark: 20 requests, 136.2 ms wall median and 169.0 ms p95; excludes live Tesseract
- Live Tesseract benchmark: 20 requests, 682.8 ms wall median and 737.6 ms p95; 546.5 ms OCR median and 565.0 ms p95
- Active-source paid-platform scan: clean outside the unchanged Treasury assignment

## Completed external setup

- Tesseract `5.5.3.20260724` is installed and available from PowerShell.
- Tesseract language data includes `eng` and `osd`.
- Podman `6.0.2` is installed. `podman-machine-default` runs under WSL2 in rootless mode, and `podman info` succeeds. The image build, process startup, and internal application health pass; Windows host access is unresolved.
- GitHub CLI authentication is active through the operating-system keyring. No token is stored in `.env` or Git.

## Live Tesseract evidence

On 2026-09-04, Codex corrected the Tesseract segmentation mode and unreadable-text policy, then reran the real provider against all seven label fixtures.

- Pass, rotated, and low-contrast fixtures return Pass.
- Brand, ABV, and warning-error fixtures return Mismatch.
- The unreadable fixture returns Needs Review rather than turning sparse OCR noise into missing-field failures.
- The adapter uses Tesseract sparse-text segmentation for independently positioned label regions, and producer statements are excluded from brand fallback.
- A 20-request production-mode benchmark passed every request and remained below the approximately five-second warm target.

## Current gate and ownership

### User next

Run the single documented Podman-machine route lookup in `USER_REQUIREMENTS.md`, return its complete output, and leave the container running.

### Codex next

After receiving that output, inspect the running container, verify bundled Tesseract and application behavior through it, rerun live timings, and update repository readiness evidence.

## Remaining delivery path

1. User runs the documented Podman-machine route lookup and returns the requested output.
2. Codex resolves host forwarding, then verifies Tesseract and application behavior inside the running container, benchmarks live OCR, runs all automated gates, and updates README evidence.
3. Codex performs repository/secrets/CI readiness review.
4. The temporary no-push gate is lifted only after container acceptance passes.
5. A qualifying no-cost public host is selected, explicitly authorized, deployed, and verified over HTTPS.
6. README receives the source URL, public URL, final timings, and final limitations before Treasury submission.

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
