# Codex continuation checkpoint

## Current objective

Source publication and all CI succeeded; delegation hierarchy is committed in a9a29fa. Bounded hosting research is complete. Next: the Codex-owned local constrained-container feasibility test in HOSTING_RESEARCH.md, before requesting hosting approval.

## Current project gate

Local/container acceptance, authorized source publication and remote CI complete. Main was pushed through readiness fix 3369a0c; CI run 34085317594 passed all three jobs. Public deployment still requires separate approval; P2 deferred.

## Important decisions

Treasury > SPEC > AGENTS > judgment with explicit user no-cost override. Tesseract behind OCRProvider; fixture-only unit-test OCR. Root executes accessible work and requests sandbox approval before handing commands to the user. USER_REQUIREMENTS contains genuine human decisions only.

## Recently completed work

Recovered base HEAD 25e09e9 and preserved dirty work. Reduced AGENTS from 223 to 33 lines; migrated inventory to SPEC and engineering/copy rules to architecture. Created CODEX_ORCHESTRATION and this checkpoint. One read-only audit agent used gpt-5.6-luna/low to check migration. Fixed favicon and caption contrast, added reusable real-HTTP container verifier/JSON fixture and CI smoke acceptance.

## Files changed

AGENTS; CODEX_ORCHESTRATION/STATE; SPEC/architecture/assumptions; README/status/plan/user/deployment/test-case docs; web CSS/layout/favicon; Git/Docker ignore lists; CI workflow; scripts/verify_container.py; tests/fixtures/demo-application.json; desktop/mobile screenshots. See Git for the exact set.

## Verification completed

42 backend tests (35 deterministic + 7 native OCR), Ruff lint/format and dependency consistency pass; frontend lint/types/6 tests/build pass. Final container production build passes. All seven live label cases and 400/422 errors pass. Final 20-request container wall median/p95 648.9/694.6 ms; API 645.0/691 ms; OCR 528.0/557 ms. Final desktop/mobile pass/mismatch/review, invalid-image recovery, evidence click/keyboard, timings, caption colors, no overflow and fresh-page console pass. Screenshots refreshed. CI YAML parses; remote backend/frontend/container checks passed in run 34085317594. Treasury file hash unchanged; targeted secret/paid-platform scan clean outside Treasury history.

## Runtime/environment state

Verified at 2026-09-06 23:11 UTC. WSL IP 192.168.70.113 (refresh after reboot). Original labelguard-ai-local on 8000 preserved. Final labelguard-ai-verified, container ca50e49c8bad, port 8001->8000, image 4c2d0173a860192822bf39fe348225ad40265773a1c272a6905a3e5acaa603ae. Linux Tesseract 5.5.0 eng/osd; UID 1001. Review URL http://192.168.70.113:8001. Sandbox Podman identity/WSL/keyring access denied; approved host execution succeeds. Native Tesseract and repository work directly. GitHub auth verified through keyring.

## Current unfinished step

CI is green on published HEAD 30efee5 (run 34085764694). No outstanding CI failure or implementation defect is recorded. Current official documentation disqualifies new Hugging Face Docker Spaces (paid plan required). Render Free is a conditional candidate, not a selected host: 0.1 CPU/512 MB feasibility and account-specific no-billing onboarding are unverified. No runtime/code changes were made during research. Checkpoint before local resource testing; full procedure and conditional deployment settings are in HOSTING_RESEARCH.md.

## Exact next actions

1. Inspect git status --short and git log -3 --oneline to confirm this checkpoint, preserving any newer changes.
2. Read USER_REQUIREMENTS for publication boundary; no manual terminal request is needed.
3. If resuming after restart: inspect podman ps --all, refresh WSL route as documented in deployment.md, and start the existing verification container only if stopped.
4. Check actual remaining usage before new work. When capacity permits, run the isolated resource-limit feasibility stage in HOSTING_RESEARCH.md. Preserve existing containers; do not create an account or deploy. Latest published CI is already confirmed green in run 34085764694; do not repeat it absent a new push.
5. Do not rerun completed local gates unless code/runtime evidence changed.

## Errors/blockers

invalid_application is resolved operationally through JSON-file/structured requests; exact historical malformed payload unavailable. Windows localhost forwarding remains unavailable; direct-IP access works. CI startup reset is resolved by bounded retry-all-errors (3369a0c). No cloud/public URL exists. Qualifying host selection and deployment approval remain.

## Git checkpoint

Published origin/main is 30efee5; its CI passed. The user-requested CODEX_ORCHESTRATION hierarchy and this status update are saved in a following local checkpoint; use git log for its hash. No hosting/deployment performed. No push of this preservation checkpoint is needed before resuming local research.

## Usage checkpoint

2026-09-07, latest runtime query during hosting research: 57% remaining in the 5-hour window, 5% weekly. The user explicitly authorized limited further work despite the earlier preservation threshold; the bounded research stage is now checkpointed. Limits are shared account capacity, not convertible into guaranteed work hours or exact task tokens. No reset credit consumed; user authorization is required to redeem one.
