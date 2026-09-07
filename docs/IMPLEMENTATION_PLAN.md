# LabelGuard AI implementation plan

## Completed implementation

P0 core and P1 work are committed as d9dd867 and 37c66f9. Local Tesseract correction followed in b5bfb61. Preserve that implementation. Detailed requirements live in SPEC; acceptance evidence lives in PROJECT_STATUS.

## Current stage

Local container/browser acceptance and repository review pass; the lightweight instruction/orchestration refactor is integrated. Source publication and remote CI completed on 2026-09-07. The current gate is qualifying host research and separately approved public deployment. CODEX_STATE records the exact continuation.

## Remaining delivery sequence

1. Local/container evidence, README/run instructions and source/secrets review are complete; retain that evidence unless changes require revalidation.
2. Source publication is authorized and completed; retain that authorization for this workflow.
3. Remote CI passed for 3369a0c. Its container job builds and exercises live OCR without secrets; retain the verified evidence.
4. Complete the local constrained-container feasibility test in HOSTING_RESEARCH.md for the conditional Render Free candidate. If feasible, obtain separate account/deployment approval and verify no-billing onboarding; otherwise continue qualifying-host research. No host has been selected.
5. Deploy, verify public HTTPS with no login, fresh-browser pass/error/mobile flows, and production timings.
6. Add source/public URLs and final limitations to README; confirm both Treasury deliverables are accessible.

Local and container gates do not themselves authorize publication. Public delivery remains unfinished until an evaluator can access the source and working application.

## Deferred scope

P2 batch, CSV, filtering, advanced corrections, and expanded beverage rules remain deferred. Do not start optional work to fill time while awaiting delivery approval.

## Constraints

No paid OCR/cloud service, billing, payment method, credits, or paid subscription. No secrets in Git. No cloud provisioning, account creation, push or deployment without the appropriate stage and explicit authorization. Treasury source remains unchanged.
