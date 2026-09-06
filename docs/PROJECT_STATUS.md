# Project Status

Updated: 2026-09-06

## Resuming after power interruption

The user has returned after another computer restart. The saved pre-restart state had `podman-machine-default` Running and the existing LabelGuard container Exited with code `0`; the last known route was `192.168.70.113`. Refresh the container state and route before continuing. Earlier health, listener PID, and IP findings below are historical evidence. The displayed exit age of `292 years ago` is unreliable and must not be interpreted as an actual elapsed time.

## Milestones

- P0 implementation committed locally as `d9dd867` (`feat: implement local single-label verification`).
- P1 implementation committed locally as `37c66f9` (`feat: add image robustness and evidence`).
- P0/P1 deterministic gates and live Windows Tesseract acceptance pass. OCI build, startup, internal health, and direct Podman-machine health pass; remaining acceptance is end-to-end container behavior.
- Podman built `labelguard-ai:local` successfully. The restarted container is healthy internally and reachable at `192.168.70.113:8000`; Windows `127.0.0.1:8000` remains refused because the WSL relay exposes only IPv6 loopback.
- The `::1:8000` listener is `wslrelay.exe`. WSL is `2.7.12.0`; the first machine-address lookup was inconclusive because the minimal Podman machine has no `hostname` executable.
- After the latest restart, the Podman-machine routing table again identifies `192.168.70.113` on `eth0`. Direct machine-address access is now the supported local container test URL.
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

Run the documented container end-to-end verification block in `USER_REQUIREMENTS.md` and return all output.

### Codex next

After receiving that output, inspect the running container, verify bundled Tesseract and application behavior through it, rerun live timings, and update repository readiness evidence.

## Remaining delivery path

1. User runs the documented container end-to-end verification block and returns all output.
2. Codex verifies browser behavior through the direct machine address, benchmarks live OCR, runs all automated gates, and updates README evidence.
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
