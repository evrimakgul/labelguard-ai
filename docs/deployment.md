# Portable deployment

One Linux container contains the static Next.js interface, FastAPI, local Tesseract and English data. OCR requires no network service, account, or credential. Codex executes these procedures; they are reproducibility instructions, not manual user tasks.

## Current public deployment (2026-09-08)

The user deployed **https://labelguard-ai-4g5s.onrender.com** on Render Free from source **919e241**. User confirmation and the supplied Render screenshot establish the Free instance and live source; the user confirms no billing information/payment method, prepaid credits or paid subscription. The screenshot shows Docker startup using Render's assigned `PORT=10000` and one Uvicorn worker. Do not hard-code the old local port into the hosted start command.

Public root, `/api/health`, favicon, demo download, all seven real OCR cases, safe errors, desktop/mobile browser flows and timings are verified. See [submission review](SUBMISSION_READINESS.md) and [public evidence](verification/public-2026-09-08.json). Auto-Deploy is unconfirmed; do not enable it or create another service merely to finish submission.

Render Free sleeps after 15 idle minutes and may take roughly a minute to wake. Free allowances can suspend services or builds, and instances may restart. Cold-start timing was not measured here. Public warm wall median/p95 was 4857.8/5304.0 ms, distinct from historical local quota tests. [Render Free documentation](https://render.com/docs/free)

For reproduction, use the repository-root Dockerfile/context and its start command, local Tesseract, same-origin browser API, and the platform-provided PORT. No database, persistent disk, custom domain or app secrets are needed. `/api/health` is available for a platform HTTP health probe; the screenshot proves root HEAD health traffic, not that this probe path was configured. Do not assume access to SSH on Free or claim to have inspected hosted environment variables through HTTP.

### Verify the existing public service

Visit the URL once if it is asleep, then run from the repository root with backend development dependencies installed:

```powershell
.\.venv\Scripts\python.exe scripts/verify_container.py --base-url https://labelguard-ai-4g5s.onrender.com --requests 20
```

Expected: seven fixture statuses, safe 400/422 errors, `local-tesseract`, and timing statistics. The command reports performance rather than asserting a strict five-second ceiling. Never relabel local results as public measurements.

## Historical local review runtime

Original user container: labelguard-ai-local, port 8000 (preserved).
Verified replacement candidate: labelguard-ai-verified, image labelguard-ai:verified, port 8001 mapped to container 8000.
Last verified VM address: 192.168.70.113; refresh after restart. Windows 127.0.0.1 forwarding failed during local acceptance; direct VM address worked. This is a local networking limitation, not proof of any particular upstream bug. Local runtime was not rechecked during public verification.

The new candidate includes the favicon and caption-contrast fixes. Use http://192.168.70.113:8001 for final local review while it is running. Neither address is a public submission URL.

## Inspect and resume

```powershell
podman ps --all --filter name=labelguard-ai
wsl.exe --distribution podman-machine-default --exec ip -4 route get 1.1.1.1
podman logs --tail 30 labelguard-ai-verified
```

If the existing verification container is stopped, Codex can start it with `podman start labelguard-ai-verified`. Await readiness before sending uploads. Avoid creating a duplicate container with an existing name.

## Build and run on a clean machine

With Podman running and ports/names available:

```powershell
podman build --tag labelguard-ai:verified .
podman run --detach --name labelguard-ai-verified --publish 8001:8000 labelguard-ai:verified
```

Docker Engine can use the same Dockerfile. Docker Desktop is not required.

## Reproducible acceptance

Run from the repository root using the installed backend development dependencies:

```powershell
$machineRoute = wsl.exe --distribution podman-machine-default --exec ip -4 route get 1.1.1.1
if ($LASTEXITCODE -ne 0) { throw 'WSL route lookup failed' }
$machineIp = [regex]::Match(($machineRoute -join ' '), '\bsrc\s+(\d{1,3}(?:\.\d{1,3}){3})\b').Groups[1].Value
if (-not $machineIp) { throw 'No machine IPv4 found' }
$labelGuardUrl = 'http://{0}:8001' -f $machineIp
curl.exe --fail --retry 10 --retry-all-errors --retry-delay 2 --retry-max-time 60 --max-time 5 --noproxy "*" "$labelGuardUrl/api/health"
if ($LASTEXITCODE -ne 0) { throw 'Application not ready' }
podman exec labelguard-ai-verified tesseract --version
podman exec labelguard-ai-verified tesseract --list-langs
.\.venv\Scripts\python.exe scripts/verify_container.py --base-url $labelGuardUrl
```

The script uses structured HTTP multipart data: seven live fixtures, expected 400/422 errors, root/favicon/health and 20 measured pass requests. It fails on unexpected results. This avoids passing JSON through native shell arguments.

For an individual curl request, read the committed JSON as the text form field:

```powershell
curl.exe --silent --show-error --noproxy "*" --max-time 20 -F 'application=<tests/fixtures/demo-application.json' -F 'image=@tests/fixtures/labels/demo-pass.png;type=image/png' "$labelGuardUrl/api/v1/verify"
```

The earlier invalid_application response occurred during JSON/model validation before OCR. Its exact original payload is unavailable; corrected file-based requests, browser requests, and valid inline JSON in a fresh shell succeed. Do not claim a server parser bug or confirmed shell defect from the pasted transcript alone.

## Runtime contract and health

Linux container, PORT default 8000, no persistent storage or application secrets, non-root UID 1001. The single-thread image passed a local 0.25 CPU/512 MB/no-swap screen with warm p95 3996.8 ms across 20 demo-pass requests. Treat this as a measured starting point, not a proven minimum or concurrency/all-artwork guarantee. Public hardware still requires its own benchmark.

The Docker runtime defaults to `OMP_THREAD_LIMIT=1` to reduce Tesseract thread oversubscription. It can be explicitly overridden for separately benchmarked hardware. Keep `OCR_TIMEOUT_SECONDS=8`; thread tuning does not justify relaxing correctness or latency gates. At a strict 0.1 CPU/512 MB quota, single-thread OCR passed the fixtures but had a 9.6-second warm p95, so that sizing is not performance-approved. See [hosting evidence](HOSTING_RESEARCH.md). Native runs must export this variable explicitly; the application does not automatically load `.env`.

Podman OCI builds warn that Dockerfile HEALTHCHECK metadata is ignored. Keep the directive for runtimes that honor it and configure a host-level GET /api/health probe for portability. No format change is needed for application operation. The health endpoint proves HTTP liveness; live OCR acceptance separately verifies the OCR dependency. A host's PORT override must also be reflected in its health-probe port.

## Public delivery

The existing user-created Render deployment is the public submission target. Source publication and verification of this service are authorized. New services, billing changes, upgrades and unrelated deployment changes are not. CI for runtime 919e241 passed in run 34183695397; PROJECT_STATUS tracks final documentation publication. Document-only pushes may trigger a rebuild if Auto-Deploy is already enabled; verify availability afterward without forcing a redeploy. Readiness retries are bounded and do not replace live OCR checks.
