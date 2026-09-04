# LabelGuard AI Implementation Plan

## P0 stabilization — complete

- Preserve the current Next.js, FastAPI, verification, image validation, fixtures, and test work.
- Make local Tesseract the default OCR provider and retain fixture-only demo OCR.
- Remove active paid-cloud requirements while leaving `TREASURY_ASSIGNMENT.md` unchanged.
- Keep one portable OCI container with Tesseract and English language data installed.
- Reconcile README, specification, deployment, assumptions, limitations, and tests.
- Run all P0 quality gates and create a local milestone commit before P1.

## P1 completion — implemented and verified

- Add EXIF orientation correction, resize safeguards, adaptive contrast, metadata removal, and bounded deskewing.
- Display clickable OCR bounding-box evidence and processing-stage timing.
- Add a demo application loader plus rotated, low-contrast, and unreadable fixtures.
- Run automated and browser acceptance checks and create a second local milestone commit.

## Deferred

P2 batch upload, CSV import/export, filtering, and expanded beverage rules remain deferred until the core and P1 workflow are stable.

## Delivery constraints

- No paid OCR, cloud subscription, billing information, payment method, or prepaid credits.
- Do not select a public host until it satisfies the no-cost criteria in `USER_REQUIREMENTS.md`.
- Do not push, deploy, or provision external resources.
