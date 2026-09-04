# Portable Deployment

LabelGuard AI ships as one OCI-compatible Linux container. It contains the exported Next.js interface, FastAPI service, Tesseract runtime, and English language data. Normal operation makes no paid OCR or cloud API call.

## Build and run

Podman is the preferred free local engine. The commands below are reference-only until `PROJECT_STATUS.md` says the live OCR gate is cleared:

Current status: Podman 6.0.2 and its rootless WSL2 machine are operational, but no LabelGuard image or container exists. Live OCR remediation must pass before the first final container build to avoid validating a known-defective revision.

```powershell
podman build -t labelguard-ai:local .
podman run --rm -p 8000:8000 labelguard-ai:local
```

Then check `http://localhost:8000/api/health` and the application at `http://localhost:8000`.

The authoritative staged command block, expected output, and handoff instructions are maintained in `USER_REQUIREMENTS.md`.

Docker Engine can use the same `Dockerfile` and `docker-compose.yml` when its local licensing is appropriate. Docker Desktop is not required.

## Runtime contract

- Linux OCI container support
- At least 0.5 CPU and 1 GB memory for the prototype
- Port supplied through `PORT`, defaulting to `8000`
- Persistent storage is not required
- No application secrets are required
- Health check: `GET /api/health`

## Public host acceptance gate

Do not select or create a hosted deployment until the provider offers:

- a public HTTPS URL;
- no billing profile, credit card, or payment method;
- no prepaid credits;
- no paid subscription;
- enough CPU and memory to run local Tesseract;
- support for the supplied OCI image without requiring an external OCR API.

After a qualifying host is selected, verify a fresh-browser pass case, mismatch case, invalid-image case, health check, warm processing time, and mobile layout. Record the exact public URL and measured median/p95 timing in README.
