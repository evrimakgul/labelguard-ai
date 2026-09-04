# LabelGuard AI Implementation Plan

## P0/P1 implementation — committed

- P0 single-label verification is committed as `d9dd867`.
- P1 preprocessing, evidence, timing, demo loading, and regression fixtures are committed as `37c66f9`.
- Local Tesseract is the default OCR provider; fixture-only demo OCR remains for deterministic tests.
- The OCI image includes Tesseract and English data, but the image has not yet been built locally.
- `TREASURY_ASSIGNMENT.md` remains unchanged historical/source material.

The deterministic and browser/demo gates are green in commits `d9dd867` and `37c66f9`. The 2026-09-04 live Tesseract defect has been corrected and all seven live OCR fixture cases pass.

P0 and P1 are stable locally. Do not add P2 scope while container and delivery acceptance remain.

## Live OCR remediation — complete

- Sparse-text segmentation preserves the isolated brand heading.
- Producer statements are excluded from brand fallback, while brand-keyword mismatches remain detectable.
- Sparse unreadable OCR produces Needs Review rather than Mismatch.
- Deterministic regressions, seven opt-in live cases, and a 20-request live benchmark pass.

## Current gate: container startup diagnosis — User then Codex

- The user runs the read-only Podman status/log/retry block in `USER_REQUIREMENTS.md` and returns its complete output.
- Codex verifies health, bundled Tesseract, pass/mismatch/review/error browser flows, logs, mobile layout, and live timings through the container.

## Deferred

P2 batch upload, CSV import/export, filtering, and expanded beverage rules remain deferred. They are not required to resolve the live OCR gate or submit the core Treasury prototype.

## Delivery constraints

- No paid OCR, cloud subscription, billing information, payment method, or prepaid credits.
- Do not select a public host until it satisfies the no-cost criteria in `USER_REQUIREMENTS.md`.
- Temporary gate: do not push, deploy, or provision external resources until live OCR and container acceptance pass.
- Final delivery: after those gates pass and the user authorizes it, push the reviewed commits, verify CI, select only a qualifying no-cost host, deploy, and verify the public HTTPS URL.
