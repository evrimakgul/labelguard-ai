# Codex continuation checkpoint

## Current objective

Single-thread Docker default and CI assertion are implemented and locally verified. Recovered 0.1 CPU experiment: all cases passed, wall p95 9599.8 ms (too slow). Rebuilt image at 0.25 CPU/512 MB passed all cases and 20-request benchmark, wall p95 3996.8 ms. Full evidence in HOSTING_RESEARCH. Next: qualifying host with adequate resources; no host selected or deployment approved.

Published source CI remains green; latest local Docker/CI changes are not pushed. Delegation hierarchy remains in CODEX_ORCHESTRATION. No P2 work or external resources introduced.

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

Rebuilt image labelguard-ai:single-thread is d653e81cfa2fac0899119b27bae06c35fcc8ae048fb8f33cd3be0089c175e538. Tesseract 5.5.0 eng/osd; OMP_THREAD_LIMIT=1 asserted. All temporary test containers were removed; original/verified containers remain running on the older image. Rechecked 42 backend tests, Ruff lint/format, frontend lint/types/6 tests, dependency consistency, CI YAML and Podman image build (frontend layers cached). Local resource-limited HTTP acceptance passed. No UI change or new browser run. Updated remote CI is pending a push; prior published run remains green. Hosting remains unresolved: Docker Spaces require a paid plan; Koyeb/Northflank require payment methods; Render's simulated free CPU misses the latency target.

## Exact next actions

1. Inspect git status --short and git log -3 --oneline to confirm this checkpoint, preserving any newer changes.
2. Read USER_REQUIREMENTS for publication boundary; no manual terminal request is needed.
3. If resuming after restart: inspect podman ps --all, refresh WSL route as documented in deployment.md, and start the existing verification container only if stopped.
4. Continue host research against the no-billing constraints and measured local sizing. Do not repeat the completed thread experiment. Preserve existing containers; no account creation/deployment without approval. If publishing the new runtime/CI checkpoint under existing source authorization, inspect the resulting CI; never claim prior CI covers this new change.
5. Do not rerun completed local gates unless code/runtime evidence changed.

## Errors/blockers

invalid_application is resolved operationally through JSON-file/structured requests; exact historical malformed payload unavailable. Windows localhost forwarding remains unavailable; direct-IP access works. CI startup reset is resolved by bounded retry-all-errors (3369a0c). No cloud/public URL exists. Qualifying host selection and deployment approval remain.

## Git checkpoint

Published origin/main is 30efee5; its CI passed. The user-requested CODEX_ORCHESTRATION hierarchy and this status update are saved in a following local checkpoint; use git log for its hash. No hosting/deployment performed. No push of this preservation checkpoint is needed before resuming local research.

## Usage checkpoint

On resumption after the user's 0% stop, the actual usage query reported 99% remaining in the five-hour window and 100% weekly. No reset credit was redeemed by Codex. Continue bounded stages with periodic checks; these are account limits, not guaranteed task hours.
