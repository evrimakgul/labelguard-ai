# Codex continuation checkpoint

## Current objective

Finish the instruction/orchestration refactor and local container acceptance milestone; then prepare authorized Treasury publication/deployment.

## Current project gate

Local/container acceptance complete. Remote publication and public deployment require explicit user authorization; P2 deferred.

## Important decisions

Treasury > SPEC > AGENTS > judgment with explicit user no-cost override. Tesseract behind OCRProvider; fixture-only unit-test OCR. Root executes accessible work and requests sandbox approval before handing commands to the user. USER_REQUIREMENTS contains genuine human decisions only.

## Recently completed work

Recovered base HEAD 25e09e9 and preserved dirty work. Reduced AGENTS from 223 to 33 lines; migrated inventory to SPEC and engineering/copy rules to architecture. Created CODEX_ORCHESTRATION and this checkpoint. One read-only audit agent used gpt-5.6-luna/low to check migration. Fixed favicon and caption contrast, added reusable real-HTTP container verifier/JSON fixture and CI smoke acceptance.

## Files changed

AGENTS; CODEX_ORCHESTRATION/STATE; SPEC/architecture/assumptions; README/status/plan/user/deployment/test-case docs; web CSS/layout/favicon; Git/Docker ignore lists; CI workflow; scripts/verify_container.py; tests/fixtures/demo-application.json; desktop/mobile screenshots. See Git for the exact set.

## Verification completed

42 backend tests (35 deterministic + 7 native OCR), Ruff lint/format and dependency consistency pass; frontend lint/types/6 tests/build pass. Final container production build passes. All seven live label cases and 400/422 errors pass. Final 20-request container wall median/p95 648.9/694.6 ms; API 645.0/691 ms; OCR 528.0/557 ms. Final desktop/mobile pass/mismatch/review, invalid-image recovery, evidence click/keyboard, timings, caption colors, no overflow and fresh-page console pass. Screenshots refreshed. CI YAML parses; remote CI not yet run. Treasury file hash unchanged; targeted secret/paid-platform scan clean outside Treasury history.

## Runtime/environment state

Verified at 2026-09-06 23:11 UTC. WSL IP 192.168.70.113 (refresh after reboot). Original labelguard-ai-local on 8000 preserved. Final labelguard-ai-verified, container ca50e49c8bad, port 8001->8000, image 4c2d0173a860192822bf39fe348225ad40265773a1c272a6905a3e5acaa603ae. Linux Tesseract 5.5.0 eng/osd; UID 1001. Review URL http://192.168.70.113:8001. Sandbox Podman identity/WSL/keyring access denied; approved host execution succeeds. Native Tesseract and repository work directly. GitHub auth verified through keyring.

## Current unfinished step

Complete local milestone commits. No remaining application acceptance failure. Next major work is authorized publication/remote CI and selection of a qualifying public host.

## Exact next actions

1. Inspect git status --short and git log -3 --oneline; finish any named pending checkpoint commit, preserving changes.
2. Read USER_REQUIREMENTS for publication boundary; no manual terminal request is needed.
3. If resuming after restart: inspect podman ps --all, refresh WSL route as documented in deployment.md, and start the existing verification container only if stopped.
4. After explicit push authorization, publish reviewed main to the existing remote and inspect CI. Research/approve a no-billing HTTPS host before deployment.
5. Do not rerun completed local gates unless code/runtime evidence changed.

## Errors/blockers

invalid_application is resolved operationally through JSON-file/structured requests; exact historical malformed payload unavailable. Valid inline JSON also succeeds. Windows localhost forwarding remains unavailable; direct-IP access works. No cloud/public URL exists. Publication/deployment approval is the next external dependency.

## Git checkpoint

Recovered base 25e09e9; remote main read-only check returned 54b86006f8e07f7cc3e59dc38c6cfdb654f09bf1. Instruction and acceptance commits are being created locally; this file's containing commit plus git log identify the final checkpoint without self-referential hashes. No push performed.

## Usage checkpoint

2026-09-06 ~23:12 UTC: 30% remaining in 5-hour window, 32% weekly. Bounded-stage mode; complete commits and stop at the finished gate, preserving reserve. Limits are shared account capacity, not exact task tokens. No reset credit consumed.
