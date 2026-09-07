# LabelGuard AI implementation plan

## Completed implementation

P0 core and P1 work are committed as d9dd867 and 37c66f9. Local Tesseract correction followed in b5bfb61. Preserve that implementation. Detailed requirements live in SPEC; acceptance evidence lives in PROJECT_STATUS.

## Current stage

Local container/browser acceptance and repository review pass; the lightweight instruction/orchestration refactor is integrated. The current gate is explicit authorization to publish the reviewed source, followed by remote CI and qualifying public deployment. CODEX_STATE records the exact continuation.

## Remaining delivery sequence

1. Local/container evidence, README/run instructions and source/secrets review are complete; retain that evidence unless changes require revalidation.
2. Prepare reviewed source publication; obtain explicit user authorization before pushing.
3. Verify remote CI after the authorized push. Its container job builds and exercises live OCR without secrets.
4. Research a host meeting the no-cost/no-billing criteria; obtain approval for that specific deployment.
5. Deploy, verify public HTTPS with no login, fresh-browser pass/error/mobile flows, and production timings.
6. Add source/public URLs and final limitations to README; confirm both Treasury deliverables are accessible.

Local and container gates do not themselves authorize publication. Public delivery remains unfinished until an evaluator can access the source and working application.

## Deferred scope

P2 batch, CSV, filtering, advanced corrections, and expanded beverage rules remain deferred. Do not start optional work to fill time while awaiting delivery approval.

## Constraints

No paid OCR/cloud service, billing, payment method, credits, or paid subscription. No secrets in Git. No cloud provisioning, account creation, push or deployment without the appropriate stage and explicit authorization. Treasury source remains unchanged.
