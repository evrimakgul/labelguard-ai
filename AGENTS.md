# LabelGuard AI — Codex Instructions

## Mission

Build, test, document, and prepare for deployment the LabelGuard AI application for the U.S. Department of the Treasury take-home assessment.

This repository is the source of truth.

Read these files before you make implementation decisions:

1. `docs/TREASURY_ASSIGNMENT.md`
2. `docs/SPEC.md`
3. This `AGENTS.md`

If requirements conflict, use this priority:

1. `docs/TREASURY_ASSIGNMENT.md`
2. `docs/SPEC.md`
3. `AGENTS.md`
4. Reasonable engineering judgment

## Operating Mode

Work autonomously.

Do not ask the user for clarification when you can make a reasonable engineering assumption.

When information is missing:

1. Make the safest reasonable assumption.
2. Record the assumption in `docs/assumptions.md`.
3. Continue the work.

Do not stop after:

- planning
- scaffolding
- creating placeholder files
- implementing only one layer
- finding a test failure
- finding a lint failure
- finding a type error
- finding a build failure

Diagnose and fix problems before you consider the task complete.

## Product Goal

Build a working standalone prototype that helps a TTB compliance agent compare alcohol label artwork with application data.

The application must:

- accept application data
- accept a label image
- extract text from the image
- identify relevant label fields
- compare detected values with expected values
- validate the Government Health Warning
- show clear verification results
- show uncertainty instead of false confidence
- provide useful error messages
- be easy to use
- be deployable
- be documented

The application is a decision-support tool.

Do not describe it as an official TTB approval system.

Do not use wording such as:

- `TTB Approved`
- `Application Approved`
- `Regulatory Approval Granted`

Use wording such as:

- `Verification complete`
- `All automated checks passed`
- `Mismatch detected`
- `Manual review required`
- `Needs review`

## Product Priorities

Use this priority order.

### P0 — Required

Complete all P0 items before optional work.

1. Application data form
2. Label image upload
3. Image validation
4. OCR integration
5. Brand name extraction and comparison
6. Alcohol content extraction and comparison
7. Government Health Warning detection
8. Government Health Warning wording validation
9. Class/type extraction and comparison
10. Net contents extraction and comparison
11. Pass / Mismatch / Missing / Needs Review statuses
12. Explainable results
13. User-friendly error handling
14. Automated tests
15. Docker support
16. Production build
17. Deployment configuration
18. README documentation
19. Assumptions and limitations documentation
20. Demo/test data

### P1 — Important

Start P1 only after P0 is stable.

- image orientation correction
- contrast improvement
- basic deskewing
- OCR confidence handling
- bounding boxes or detected-text evidence
- demo application loader
- performance instrumentation
- additional regression fixtures

### P2 — Optional

Start P2 only when P0 and P1 are complete and tested.

- batch upload
- CSV application import
- batch progress
- batch filtering
- CSV result export
- advanced image correction
- additional beverage-specific rules

A working core product is more important than incomplete optional features.

## Architecture

Use this default stack unless there is a strong technical reason to change it.

### Frontend

- Next.js
- TypeScript
- React

### Backend

- FastAPI
- Python

### OCR

- Tesseract OCR as the default local OCR engine
- OCR must run locally and must not require a paid cloud API
- Keep OCR behind the `OCRProvider` abstraction so another provider can be added later if needed

### Image Processing

Use only what is necessary.

Preferred:

- Pillow
- OpenCV when required

### Testing

Backend:

- pytest

Frontend:

- appropriate TypeScript test tools
- use Playwright only where end-to-end testing adds value

### Deployment

- Docker
- portable OCI-compatible hosting
- GitHub Actions

### Source Control

- GitHub
- `main` is the primary branch

Do not introduce:

- a database unless a real requirement needs it
- message queues for the basic prototype
- microservices that do not add clear value
- unnecessary infrastructure
- an LLM for simple deterministic comparisons

## Architecture Principles

Separate these concerns:

1. Image validation
2. Image preprocessing
3. OCR
4. Field extraction
5. Normalization
6. Verification
7. Result presentation

OCR must not contain regulatory business rules.

Verification rules must not depend directly on the OCR vendor.

Use an OCR provider abstraction.

Example:

```python
class OCRProvider(Protocol):
    async def extract(self, image: bytes) -> OCRResult:
        ...
