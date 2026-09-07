# User requirements

Only genuine human dependencies belong here. Codex owns routine terminal, container, OCR, test, browser, benchmark, Git, and documentation work.

## Current user action

None for local verification. Podman, WSL2, Tesseract, GitHub CLI, and the repository are accessible to Codex. The sandbox cannot access Podman's identity file, the WSL service, or the GitHub credential store; approved execution outside it succeeds. Any future sandbox approval is requested through the app, not by asking the user to copy commands.

## Next external decision: source publication

Local/container acceptance and repository review pass. The single next user decision is whether Codex may push the reviewed local main branch to the existing remote `https://github.com/evrimakgul/labelguard-ai.git` and inspect its GitHub Actions checks. No push is authorized yet; the user need not run any terminal command. This authorization would not include creating a host account, deploying, provisioning, or accepting costs.

Public deployment additionally requires approval of an identified host that provides a public HTTPS URL without billing information, a payment method, prepaid credits, or a paid subscription, and can run local Tesseract. No host has been selected. Codex will research and present a concrete candidate before requesting a hosting decision; no new account is needed now.

Account authorization or physical/admin interaction is requested only if Codex attempts it and cannot proceed. Record the exact inaccessible resource, attempted command, error, and single required action here if that happens.

## Credentials

The app requires no API key, OCR credential, or application secret. GitHub CLI uses the existing OS keyring; never copy its token into chat, .env, or Git. Any future necessary secret belongs in an approved secret store or ignored local configuration.

## Ownership

Runtime instructions and reproducible commands are in [deployment.md](deployment.md). Current evidence is in [PROJECT_STATUS.md](PROJECT_STATUS.md); exact continuation is in [CODEX_STATE.md](CODEX_STATE.md). A restart can invalidate runtime state; Codex refreshes it directly.
