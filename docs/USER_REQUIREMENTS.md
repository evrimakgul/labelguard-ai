# User Requirements

These actions are needed only for live local OCR, local container verification, or later GitHub inspection. None requires an API key, credit card, billing profile, prepaid credits, or paid subscription.

## 1. Install Tesseract for live Windows OCR

Install a free Tesseract 5.x Windows build with the English language data (`eng`). Use the installation guidance linked from the [Tesseract documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html).

After installation, open a new PowerShell window and run:

```powershell
tesseract --version
tesseract --list-langs
```

The second command must include `eng`.

If `tesseract` is not on `PATH`, copy `.env.example` to `.env` and set the executable path there:

```dotenv
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

`.env` is ignored by Git. This value is a local path, not a secret. Do not add it to README, source code, or a committed configuration file.

Why it is needed: Python uses the free `pytesseract` adapter to launch the local Tesseract executable. Tests and fixture-demo mode continue to work without the executable.

## 2. Install Podman for local container verification

Install the free, open-source [Podman Desktop](https://podman-desktop.io/) and its Podman engine. It does not require a hosted account or payment information.

Verify it in PowerShell:

```powershell
podman --version
podman machine init
podman machine start
```

If a Podman machine already exists, skip `podman machine init`.

Why it is needed: the repository ships an OCI-compatible `Dockerfile`. Podman can build and run it without Docker Desktop or a paid Docker Desktop license. The container itself includes Tesseract.

## 3. Optional GitHub CLI repair

The configured GitHub CLI credential is currently invalid. This is not needed for local implementation or commits. If later CI inspection is desired, use the browser/device flow:

```powershell
gh auth login --web
```

Do not send a personal access token in chat and do not place one in `.env`. The CLI should store authentication in the operating-system credential manager. No GitHub secret is required by the current CI workflow.

## 4. Public hosting is intentionally deferred

Do not create a cloud account or resource yet. A future host is acceptable only if it provides all of the following without exceptions:

- a public HTTPS URL;
- no billing information or payment method;
- no prepaid credits;
- no paid subscription;
- enough CPU and memory to run the supplied container and local Tesseract.

Until such a host is selected, local execution and the portable container are the supported deployment targets.

## Secrets summary

LabelGuard AI currently needs no secret token, API key, service credential, or paid external API. If a future deployment introduces a secret, store it only in the host's secret manager or an ignored local `.env`, never in Git.

