# User Requirements

This file separates completed setup from the next manual gate. None of these tools requires an API key, credit card, billing profile, prepaid credits, or paid subscription.

## Completed: Tesseract

Tesseract `5.5.3.20260724` is installed and callable from PowerShell. Language data includes `eng` and `osd`. No `TESSERACT_CMD` override is currently required.

Verified commands:

```powershell
tesseract --version
tesseract --list-langs
```

The second command includes `eng`.

For a future machine where Tesseract is not on `PATH`, set only the local executable path in ignored `.env`:

```dotenv
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

`.env` is ignored by Git. This value is a local path, not a secret. Do not add it to README, source code, or a committed configuration file.

Python uses the free `pytesseract` adapter to launch this executable.

## Completed: Podman

Podman Desktop and Podman `6.0.2` are installed. `podman-machine-default` is running under WSL2, `podman info` succeeds, and the engine is rootless. No image or container has been built for this project yet.

Verified commands:

```powershell
podman --version
podman machine list
podman info
```

The repository's OCI-compatible `Dockerfile` can be built without Docker Desktop or a paid Docker Desktop license.

## Completed: GitHub CLI authentication

GitHub CLI authentication is active for `evrimakgul` through the operating-system keyring. No token was added to `.env` or Git. Reauthentication is only needed if `gh auth status` later fails:

```powershell
gh auth login --web
```

Do not send a personal access token in chat and do not place one in `.env`. The CLI should store authentication in the operating-system credential manager. No GitHub secret is required by the current CI workflow.

## Current Codex gate

Live Tesseract acceptance exposed a brand-detection defect. Do not build the final container, push, or deploy while `PROJECT_STATUS.md` lists this gate as open. Codex must repair and revalidate OCR first.

## Single next action now

No PowerShell command is required now. Send Codex this instruction:

```text
Fix and verify the live Tesseract acceptance blockers documented in PROJECT_STATUS.md.
```

Expected result: Codex corrects brand detection and unreadable-image status behavior, adds regression coverage, reruns the real local Tesseract fixtures, and updates `PROJECT_STATUS.md` to open the container gate.

## Next PowerShell action after Codex clears live OCR

Run this block from a new PowerShell window at the repository root:

```powershell
Set-Location C:\Users\Evrim\Documents\PROJECTS\labelguard-ai
podman build --tag labelguard-ai:local .
podman run --detach --name labelguard-ai-local --publish 8000:8000 labelguard-ai:local
Invoke-RestMethod http://localhost:8000/api/health
podman exec labelguard-ai-local tesseract --version
podman exec labelguard-ai-local tesseract --list-langs
(Invoke-WebRequest http://localhost:8000).StatusCode
podman ps --filter name=labelguard-ai-local
```

Expected success:

- `podman build` exits successfully and creates `labelguard-ai:local`.
- `podman run` prints a container ID.
- Health output contains `status` equal to `ok`.
- Container Tesseract reports version 5.x and lists `eng`.
- The application root returns HTTP status `200`.
- `podman ps` shows `labelguard-ai-local` running and publishing port 8000.

Return the complete PowerShell output to Codex and leave the container running. Codex will then inspect logs, exercise the browser/API through the container, run live OCR fixtures and benchmarks, and tell you when it is safe to stop the container.

## Public hosting is intentionally deferred

Do not create a cloud account or resource yet. A future host is acceptable only if it provides all of the following without exceptions:

- a public HTTPS URL;
- no billing information or payment method;
- no prepaid credits;
- no paid subscription;
- enough CPU and memory to run the supplied container and local Tesseract.

Until such a host is selected, local execution and the portable container are the supported deployment targets.

## Secrets summary

LabelGuard AI currently needs no secret token, API key, service credential, or paid external API. If a future deployment introduces a secret, store it only in the host's secret manager or an ignored local `.env`, never in Git.
