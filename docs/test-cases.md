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
| Invalid/corrupt upload | Friendly 400 error |
| OCR provider failure | Friendly 503 without upstream details |
| Tesseract adapter output | Words, confidence, lines, and bounding boxes map correctly |
| Missing Tesseract runtime | Friendly provider error without internal details |

## Golden fixtures

`tests/fixtures/labels` includes pass, brand mismatch, ABV mismatch, and warning-format regression labels. PNG metadata contains the exact deterministic OCR result used by demo mode; displayed artwork and metadata are generated from the same source values.

## Manual acceptance

1. Start API in demo mode and start the frontend.
2. Enter `OLD TOM DISTILLERY`, `Kentucky Straight Bourbon Whiskey`, `45`, and `750 mL`.
3. Upload `demo-pass.png` and verify.
4. Confirm a visible Pass summary, expected/detected values, confidence, warning disclaimer, and extracted text.
5. Repeat with mismatch fixtures and confirm the relevant issue is explained.
6. Upload a text file renamed as PNG and confirm the API rejects it without a stack trace.
7. Check desktop and mobile layouts with keyboard-only navigation.
8. With Tesseract installed, repeat the pass fixture in normal production mode.
