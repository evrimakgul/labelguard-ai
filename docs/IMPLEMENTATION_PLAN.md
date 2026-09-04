# LabelGuard AI Implementation Plan

## P0/P1 implementation — committed

- P0 single-label verification is committed as `d9dd867`.
- P1 preprocessing, evidence, timing, demo loading, and regression fixtures are committed as `37c66f9`.
- Local Tesseract is the default OCR provider; fixture-only demo OCR remains for deterministic tests.
- The OCI image includes Tesseract and English data, but the image has not yet been built locally.
- `TREASURY_ASSIGNMENT.md` remains unchanged historical/source material.

The deterministic and browser/demo gates are green in commits `d9dd867` and `37c66f9`. A 2026-09-04 live Tesseract smoke test reopened acceptance because the pass fixture's brand was not detected.

Current priority returns to P0 OCR correctness. Retain existing P1 work, but do not add P1 or P2 scope until live P0 acceptance passes.

## Immediate remediation — Codex

- Fix Tesseract segmentation/preprocessing so the pass fixture detects its brand.
- Make field fallback behavior express Missing or Needs Review instead of a misleading high-confidence mismatch when no plausible brand candidate exists.
- Make genuinely unreadable OCR produce Needs Review rather than Mismatch.
- Add live-regression coverage and rerun local OCR acceptance before benchmarking.

## Container acceptance — User then Codex

- After Codex clears live OCR, the user runs the exact Podman block in `USER_REQUIREMENTS.md` and leaves the container running.
- Codex verifies health, bundled Tesseract, pass/mismatch/review/error browser flows, logs, mobile layout, and live timings through the container.

## Deferred

P2 batch upload, CSV import/export, filtering, and expanded beverage rules remain deferred. They are not required to resolve the live OCR gate or submit the core Treasury prototype.

## Delivery constraints

- No paid OCR, cloud subscription, billing information, payment method, or prepaid credits.
- Do not select a public host until it satisfies the no-cost criteria in `USER_REQUIREMENTS.md`.
- Temporary gate: do not push, deploy, or provision external resources until live OCR and container acceptance pass.
- Final delivery: after those gates pass and the user authorizes it, push the reviewed commits, verify CI, select only a qualifying no-cost host, deploy, and verify the public HTTPS URL.
