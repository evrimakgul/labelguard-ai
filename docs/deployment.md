# Portable deployment

One Linux container contains the static Next.js interface, FastAPI, local Tesseract and English data. OCR requires no network service, account, or credential. Codex executes these procedures; they are reproducibility instructions, not manual user tasks.

## Current local runtime

Original user container: labelguard-ai-local, port 8000 (preserved).
Verified replacement candidate: labelguard-ai-verified, image labelguard-ai:verified, port 8001 mapped to container 8000.
Current VM address: 192.168.70.113; refresh after restart. Windows 127.0.0.1 forwarding remains unavailable; direct VM address works. This is a local networking limitation, not proof of any particular upstream bug.

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

No hosting provider is selected or authorized. Require HTTPS without login, no billing/payment method, no credits/subscription, and sufficient resources for local OCR. After explicit approval, verify deployment from a fresh browser and record URLs, timings, cold-start behavior, and limitations. Source publication was authorized; remote CI passed for 3369a0c in run 34085317594, including the built container and real OCR checks. Readiness retries include transient connection resets with a bounded retry count/time limit.
