# User requirements

Only genuine human dependencies belong here. Codex owns routine terminal, container, OCR, test, browser, benchmark, Git, and documentation work.

## Current user action

None for local verification. Podman, WSL2, Tesseract, GitHub CLI, and the repository are accessible to Codex. The sandbox cannot access Podman's identity file, the WSL service, or the GitHub credential store; approved execution outside it succeeds. Any future sandbox approval is requested through the app, not by asking the user to copy commands.

## Source publication authorized

On 2026-09-07, the user authorized pushing the reviewed main branch to `https://github.com/evrimakgul/labelguard-ai.git` and verifying GitHub Actions. Source publication and CI verification succeeded, including the container startup-probe correction. No additional manual terminal action or repeat source-publication approval is required for this workflow. This does not authorize creating a host account, deploying, provisioning, or accepting costs.

Public deployment additionally requires approval of an identified host that provides a public HTTPS URL without billing information, a payment method, prepaid credits, or a paid subscription, and can run local Tesseract. No host has been selected. [HOSTING_RESEARCH.md](HOSTING_RESEARCH.md) records Render Free as a conditional candidate and rejects paid-plan Docker Spaces. Local resource testing found an OCR timeout; Codex must resolve feasibility before requesting separate account/deployment approval. No new account, manual command, or hosting decision is needed now. Any required billing/card step disqualifies the candidate.

Single-thread tuning now passes correctness at 0.1 CPU, but still misses the speed target. The rebuilt image meets the fixture target at 0.25 CPU/512 MB. Codex owns further qualifying-host research; do not create a Render account or run additional commands for these results. Koyeb/Northflank are rejected because they require a payment method.

Account authorization or physical/admin interaction is requested only if Codex attempts it and cannot proceed. Record the exact inaccessible resource, attempted command, error, and single required action here if that happens.

## Credentials

The app requires no API key, OCR credential, or application secret. GitHub CLI uses the existing OS keyring; never copy its token into chat, .env, or Git. Any future necessary secret belongs in an approved secret store or ignored local configuration.

## Ownership

Runtime instructions and reproducible commands are in [deployment.md](deployment.md). Current evidence is in [PROJECT_STATUS.md](PROJECT_STATUS.md); exact continuation is in [CODEX_STATE.md](CODEX_STATE.md). A restart can invalidate runtime state; Codex refreshes it directly.
