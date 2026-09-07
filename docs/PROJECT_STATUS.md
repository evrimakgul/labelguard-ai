# Project status

Updated: 2026-09-06

## Current gate

Local implementation and container acceptance are complete for the supported core scope. Public-source publication, remote CI, host selection and public deployment remain pending authorization. P2 remains deferred. CODEX_STATE holds exact continuation, not this document.

## Verified runtime

Codex directly accessed the repository, native Tesseract, Podman, WSL2 and GitHub CLI. Podman identity/WSL service/keyring access fail in the sandbox and succeed with approved host execution; no manual terminal handoff is needed.

- Host OCR: Tesseract 5.5.3.20260724.
- Container: Tesseract 5.5.0, eng/osd, non-root UID 1001.
- Original container labelguard-ai-local on port 8000 preserved.
- Final image labelguard-ai:verified, ID 4c2d0173a860192822bf39fe348225ad40265773a1c272a6905a3e5acaa603ae.
- Verification container labelguard-ai-verified, ID ca50e49c8bad, port 8001 -> 8000.
- Local review URL: http://192.168.70.113:8001 (refresh route after restart).
- Windows IPv4 localhost forwarding remains unavailable; direct VM access works. The precise WSL relay cause is unconfirmed and does not block direct-IP acceptance.

## Acceptance evidence

- Backend: 35 deterministic tests plus 7 opt-in native OCR tests, all 42 passed; Ruff lint/format and pip dependency consistency passed.
- Frontend: lint, TypeScript, all 6 tests and production build passed. Final CSS change additionally passed container production build and browser verification.
- Podman: final image built, started, and served root/favicon/health successfully. Container pip consistency passed.
- Real container API: all seven fixtures returned expected pass/mismatch/review; invalid image returned safe 400; malformed application returned safe 422.
- Browser: desktop pass/mismatch/review; invalid PNG error preserved application values; successful retry cleared the error. 390px mobile pass, evidence selection, timing details, and no horizontal overflow.
- Final fresh-page browser console: zero errors/warnings. The deliberate invalid-image test produces its expected HTTP 400 resource entry.
- Fixed favicon 404 and preview filename/caption contrast; screenshots in screenshots/container-desktop.png and screenshots/container-mobile.png.
- Final warm container benchmark: 20 sequential demo-pass requests after acceptance warmup; wall median 648.9 ms / nearest-rank p95 694.6 ms, API 645.0 / 691 ms, OCR 528.0 / 557 ms. Fixture/hardware-specific, not arbitrary-artwork or public-host guarantees.
- CI YAML parses; workflow now loads/runs its image and performs real OCR smoke acceptance. Hosted execution is pending a push.
- Treasury source SHA256 remains AB10D3076C1421514C9B3FDC1970ABE2A068F3582F195CDC62B60675FD007E6A.

## invalid_application resolution

The original failure occurred at application JSON/model validation, before OCR. Exact historical request bytes are unavailable. File-based JSON and structured HTTP submissions pass, and a fresh valid inline-JSON shell request also passed: shell quoting or transcript escaping is plausible, not a proven unique cause. The reproducible fix is tests/fixtures/demo-application.json and scripts/verify_container.py. Server validation was not weakened.

## Ownership and remaining delivery

Codex owns all accessible tests, runtime operations, browser checks, benchmarks, repository inspection and documentation. USER_REQUIREMENTS contains only genuine human dependencies.

1. Final review and local checkpoint of this verified work.
2. Obtain explicit permission to publish reviewed commits to the existing source remote.
3. Push only when authorized; inspect remote CI and resolve any failure.
4. Research a host with public HTTPS, no billing/payment/credits/subscription, sufficient local OCR resources; obtain deployment/account approval.
5. Deploy and verify public health, full workflow, errors, mobile layout and timings; update README URLs and limitations.
6. Confirm evaluator-accessible source and public application before Treasury submission.

No paid dependency or application secret is required. No push, deployment or external provisioning has been performed. Completing local acceptance does not authorize those actions.
