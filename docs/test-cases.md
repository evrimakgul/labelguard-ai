# Test Cases

## Automated coverage

| Case | Expected |
| --- | --- |
| Exact label | Overall Pass |
| Brand capitalization only | Brand Pass |
| Wrong brand | Brand Mismatch |
| Low-confidence exact OCR | Needs Review, never Pass |
| Wrong ABV | Alcohol Mismatch |
| Proof conversion | Correct numeric value; proof-only format Needs Review |
| Liter and fluid-ounce volume | Normalized to milliliters |
| Missing warning | Missing and overall Mismatch |
| Title-case warning heading | Heading Mismatch |
| Warning spelling error | Wording Mismatch |
| Warning punctuation error | Punctuation Mismatch |
| Empty OCR | Overall Needs Review |
| Sparse OCR noise | Overall Needs Review, not missing-field Mismatch |
| Invalid/corrupt upload | Friendly 400 error |
| OCR provider failure | Friendly 503 without upstream details |
| Tesseract adapter output | Sparse-text mode plus words, confidence, lines, and bounding boxes map correctly |
| Missing Tesseract runtime | Friendly provider error without internal details |
| EXIF-rotated image | Orientation is corrected and metadata is removed |
| Low-contrast image | Contrast enhancement is applied |
| Small skew | Bounded correction angle is detected |
| Evidence selection | Result selection highlights the matching OCR polygon |

## Golden fixtures

`tests/fixtures/labels` includes pass, brand mismatch, ABV mismatch, warning-format, rotated, low-contrast, and unreadable regression labels. PNG metadata contains the exact deterministic OCR result used by demo mode; displayed artwork and metadata are generated from the same source values. The unreadable fixture intentionally contains no demo metadata.

## Manual acceptance

Public acceptance on 2026-09-08 passed all seven live fixtures plus safe API errors, desktop/mobile flows, invalid-image recovery, keyboard evidence selection and timings. Public screenshots and machine-readable results are linked from PROJECT_STATUS. Warm median/p95 is 4857.8/5304.0 ms; no strict five-second or cold-start pass is claimed. The sequence below can also be used locally; do not use fixture-mode timings as production OCR evidence.

1. Start API in demo mode and start the frontend.
2. Enter `OLD TOM DISTILLERY`, `Kentucky Straight Bourbon Whiskey`, `45`, and `750 mL`.
3. Upload `demo-pass.png` and verify.
4. Confirm a visible Pass summary, expected/detected values, confidence, warning disclaimer, and extracted text.
5. Repeat with mismatch fixtures and confirm the relevant issue is explained.
6. Upload a text file renamed as PNG and confirm the API rejects it without a stack trace.
7. Check desktop and mobile layouts with keyboard-only navigation.
8. With Tesseract installed, run `$env:RUN_LIVE_OCR='1'; .\.venv\Scripts\pytest apps\api\tests\test_live_tesseract.py; Remove-Item Env:RUN_LIVE_OCR`.

Current result on 2026-09-06: **passed**. All seven cases also passed against the final Linux container. Desktop/mobile browser verification covered pass, brand mismatch, unreadable, invalid-image error and recovery, clickable evidence, timings, and zero horizontal overflow. The final fresh-page console had zero errors/warnings. See PROJECT_STATUS for runtime identifiers and measurements; run `scripts/verify_container.py --base-url <url>` with the project Python environment to reproduce API acceptance and benchmarking.
