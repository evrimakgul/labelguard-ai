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

## Podman setup and current acceptance state

Podman Desktop and Podman `6.0.2` are installed. `podman-machine-default` is running under WSL2, `podman info` succeeds, and the engine is rootless. The LabelGuard image build completed and the named container was created, but the first health request closed unexpectedly before the remaining checks ran.

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

## Completed: live Windows OCR acceptance

The production Tesseract provider passes all seven repository label cases, including corrected brand detection and Needs Review handling for unreadable OCR. A 20-request live benchmark also passes.

## Completed: Podman process diagnosis

The container remained running for at least 15 minutes with exit code `0`. Its logs show application startup completed and Uvicorn listening on `0.0.0.0:8000`; Podman reports `0.0.0.0:8000->8000/tcp`. A delayed request to `localhost` still closed unexpectedly. The application process is therefore stable, and diagnosis now moves to the in-container endpoint and Windows IPv4 forwarding path.

## Completed: internal and Windows IPv4 health diagnosis

The in-container endpoint returns `{"status":"ok"}`, proving that the packaged application is healthy. Windows cannot connect to `127.0.0.1:8000`, and `curl.exe` receives connection refused. Windows reports only an IPv6 `::1:8000` listener owned by process `29440`, despite Podman reporting an IPv4 publication. The open defect is therefore Podman/WSL host forwarding, not LabelGuard startup.

Podman's Windows documentation says published ports should bind to `127.0.0.1`. The observed behavior instead matches [Microsoft WSL issue 41204](https://github.com/microsoft/WSL/issues/41204), which reports Podman 6 ports reachable inside WSL but refused from Windows.

## Completed: relay identity and WSL version

PID `29440` is `C:\Program Files\WSL\wslrelay.exe`, confirming that the IPv6 listener belongs to WSL forwarding. The host runs WSL `2.7.12.0` with kernel `6.18.33.2-2`. The first machine-address lookup was inconclusive because the minimal `podman-machine-default` image does not contain `hostname`; the resulting null-variable connection attempts did not test any Podman-machine address.

## Completed: Podman-machine IPv4 lookup

The routing table reports `192.168.70.113` as the current Podman-machine source address on `eth0`. This address is diagnostic and can change after restarting the Podman machine.

## Single next action now: test the Podman-machine IPv4

Run this exact read-only block from PowerShell. Do not substitute an address, restart anything, or remove the container:

```powershell
Set-Location C:\Users\Evrim\Documents\PROJECTS\labelguard-ai
Test-NetConnection -ComputerName 192.168.70.113 -Port 8000
curl.exe --verbose --noproxy "*" --max-time 10 http://192.168.70.113:8000/api/health
```

Expected evidence:

- `Test-NetConnection` reports whether Windows can reach port `8000` on the Podman-machine address.
- If reachable, `curl.exe` returns HTTP `200` with `{"status":"ok"}`.
- If refused or timed out, the output confirms that neither WSL localhost relay nor direct machine-address access works.

Return the complete output to Codex and leave the container running.

## OCI `HEALTHCHECK` warning

Podman builds default to OCI format and report that the Dockerfile `HEALTHCHECK` is ignored. This is a metadata limitation, not the cause of the connection failure: the application endpoint remains `GET /api/health`. Keep the Dockerfile health check for Docker-compatible runtimes, and use the endpoint as the portable host-level health probe. Do not switch the normal build to Docker format solely to silence this warning; an optional `podman build --format docker` is only needed when a Docker-specific health-check metadata test is required.

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
