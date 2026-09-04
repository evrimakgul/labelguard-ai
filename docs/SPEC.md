# LabelGuard AI — Treasury Take-Home Implementation Plan

## 1. Executive Summary

LabelGuard AI will be a standalone web application that compares alcohol beverage label artwork with information supplied in a label application.

The application will:

1. Accept expected application data and a label image.
2. Extract text from the label with OCR.
3. Normalize and identify key label fields.
4. Compare extracted fields with expected application values.
5. perform deterministic compliance checks for the Government Health Warning.
6. Return a clear result for each field:

   * Pass
   * Mismatch
   * Missing
   * Needs Review
7. Display the detected text, expected value, confidence, and reason.
8. Support batch processing after the single-label workflow is stable.

The design will prioritize the requirements that appear repeatedly in the Treasury assignment:

* Results should normally return in approximately five seconds.
* The user interface must require very little training.
* The system must tolerate harmless differences such as capitalization.
* The system must preserve human judgment for uncertain cases.
* Batch processing is valuable for large submissions.
* The prototype must not depend on direct COLAs integration.
* The deployed system should minimize unnecessary external dependencies.

These priorities come directly from the stakeholder notes and evaluation criteria in the assignment.

The recommended architecture is:

**React/Next.js + TypeScript**
→ **FastAPI/Python verification API**
→ **image preprocessing**
→ **Azure Vision OCR**
→ **deterministic verification engine**

Azure Vision is appropriate because its current Read OCR API is designed for synchronous, near-real-time text extraction.

Deployment should use one containerized application on Azure Container Apps. Microsoft provides direct support for containerized FastAPI applications on that service.

The browser will communicate only with LabelGuard AI. OCR requests will occur server-side. This design reduces the effect of network restrictions on Treasury workstations.

The application should not claim:

> APPROVED BY TTB

It should instead report:

> Verification result
> All automated checks passed.

or:

> Manual review required.

This distinction is important. The prototype verifies evidence. It does not replace the regulatory decision.

---

# 2. Operational Plan

## Phase 0 — Freeze the scope and acceptance tests

Before implementation, convert the interview notes into measurable requirements.

### P0 requirements

These requirements must work before any optional feature is added.

| Requirement              | Acceptance target                                        |
| ------------------------ | -------------------------------------------------------- |
| Upload label image       | JPEG and PNG work reliably                               |
| Brand comparison         | Correct label passes                                     |
| Brand capitalization     | `STONE'S THROW` vs `Stone's Throw` passes                |
| ABV extraction           | Numerical ABV is detected                                |
| ABV comparison           | Mismatch is clearly shown                                |
| Class/type comparison    | Expected and detected class/type values are compared     |
| Net contents comparison  | Expected and detected net contents values are compared   |
| Health warning detection | Missing warning fails                                    |
| Warning wording          | Text and punctuation are validated                       |
| Warning heading          | Incorrect `Government Warning` capitalization fails      |
| OCR uncertainty          | Low-confidence output becomes Needs Review               |
| Explainability           | Expected and detected values are visible                 |
| Processing speed         | Normal image target ≤5 seconds                           |
| Deployment               | Public HTTPS URL works without login                     |
| Repository               | Clean README, setup, tests, architecture and limitations |

The five-second requirement should be treated as a product requirement rather than a cosmetic optimization because the stakeholder explicitly identifies slow processing as the reason the previous system was abandoned.

### P1 requirements

Add these after the P0 vertical slice works:

* producer/importer name
* country of origin
* image rotation correction
* contrast correction
* result bounding boxes

### P2 requirements

Only add these if P0 and P1 are stable:

* batch upload
* CSV export
* warning bold-style estimation
* batch retry controls
* advanced perspective correction
* historical verification sessions
* PDF support
* additional beverage-specific regulatory rules
* AI fallback for difficult OCR cases

The Treasury instructions explicitly favor a working core application with clean code over an ambitious but incomplete implementation.

---

## Phase 1 — Build the vertical slice

Build one complete workflow before implementing additional rules.

The first workflow is:

**Application values → label upload → OCR → verification → result**

Use the sample values from the assignment:

* Brand: OLD TOM DISTILLERY
* Class/type: Kentucky Straight Bourbon Whiskey
* ABV: 45%
* Net contents: 750 mL

Create a clean test label that contains these values and the required warning.

At the end of this phase, the deployed application must already be able to process one image and return a useful result.

Do not build batch processing before this path works.

---

## Phase 2 — Implement the verification engine

Separate OCR from verification.

The verification engine must consume structured data. It should not know which OCR provider produced the text.

Conceptually:

```text
OCR
 ↓
ExtractedLabel
 ↓
Field Parsers
 ↓
Normalization
 ↓
Verification Rules
 ↓
VerificationResult
```

This separation gives three benefits.

First, rules become easy to unit test.

Second, the OCR provider can be replaced later.

Third, deterministic business logic does not become hidden inside an AI prompt.

### Brand verification

Normalize:

* Unicode
* leading and trailing spaces
* repeated whitespace
* capitalization

Do not treat capitalization as a mismatch.

Examples:

```text
Expected: Stone's Throw
Detected: STONE'S THROW
Result: PASS
```

Use fuzzy similarity only after deterministic normalization.

Suggested thresholds:

```text
>= 95%       PASS equivalent
85–94%       NEEDS REVIEW
< 85%        MISMATCH
```

Do not silently classify uncertain text as correct.

---

## Phase 3 — Implement regulatory checks

The app should distinguish two concepts:

### Application consistency

Does the label match what the applicant submitted?

Example:

```text
Application ABV: 45%
Label ABV:       40%
→ MISMATCH
```

### Label-rule compliance

Does an independently regulated statement follow the known rule?

The Government Health Warning is the best example.

TTB states that the warning must use the required wording. The warning applies to beverages containing at least 0.5% alcohol by volume. TTB also specifies that the words `GOVERNMENT WARNING` must be uppercase and bold, while the remaining warning text must not be bold. The statement must be continuous and separate from other information.

This distinction should be visible in the UI:

```text
APPLICATION CHECKS
Brand name          Pass
Class / type        Pass
Alcohol content     Pass
Net contents        Pass

LABEL REQUIREMENTS
Health warning      Pass
```

That structure makes the system easier to explain.

---

## Phase 4 — Add image robustness

Apply inexpensive preprocessing before OCR.

Pipeline:

```text
Upload
 ↓
Validate
 ↓
Correct EXIF orientation
 ↓
Resize if necessary
 ↓
Contrast normalization
 ↓
Optional deskew
 ↓
OCR
```

Do not apply aggressive image processing to every file.

Run the original image first when possible. Apply stronger preprocessing only when OCR confidence is low.

This approach helps preserve latency.

Azure Vision currently accepts common image formats and is intended to extract text from photographs and other non-document surfaces.

---

## Phase 5 — Build human-review UX

The system must expose uncertainty.

A result should never show only:

```text
FAILED
```

Instead show:

```text
Alcohol Content                         MISMATCH

Expected
45% Alc./Vol.

Detected
40% Alc./Vol.

Reason
The numeric alcohol content differs from the application.

OCR confidence
98%
```

For uncertain OCR:

```text
Brand Name                              NEEDS REVIEW

Expected
OLD TOM DISTILLERY

Detected
OLD T0M DISTILLERY

Reason
OCR confidence is below the automatic verification threshold.

OCR confidence
76%
```

This supports the senior-agent requirement for judgment rather than pretending that every difference has the same meaning.

---

## Phase 6 — Add batch processing

Batch processing should reuse the normal verification endpoint.

Do not create a second verification engine.

Recommended batch input:

### CSV

```csv
application_id,image_filename,brand_name,class_type,abv,net_contents
COLA-001,label-001.jpg,OLD TOM DISTILLERY,Kentucky Straight Bourbon Whiskey,45,750 mL
COLA-002,label-002.jpg,ACME SPIRITS,Vodka,40,1 L
```

### Images

```text
label-001.jpg
label-002.jpg
```

The browser maps CSV rows to images by filename.

Then it sends normal verification requests with bounded concurrency.

For example:

```text
300 applications
      ↓
browser queue
      ↓
4 concurrent requests
      ↓
POST /api/v1/verify
      ↓
results table
```

This design avoids one very long 300-image HTTP request.

The batch UI should show:

```text
Processing 86 of 300

Passed             63
Mismatch           11
Needs Review        9
Failed               3
```

Filters:

* All
* Passed
* Mismatch
* Needs Review
* Error

Provide CSV export.

For the take-home, batch processing should not block completion of the core single-label workflow.

---

## Phase 7 — Performance hardening

Instrument each processing stage.

Example:

```text
request_total_ms:      3260
image_prepare_ms:       190
ocr_ms:                2240
field_extract_ms:       240
verification_ms:         38
response_build_ms:       12
```

Target:

| Metric                            |  Target |
| --------------------------------- | ------: |
| Typical request                   |  ≤3.5 s |
| p95 warm request                  |    ≤5 s |
| Verification engine excluding OCR | <100 ms |
| UI feedback after click           | <100 ms |

The application must show immediate progress even while OCR is running.

Use:

```text
Uploading…
Reading label…
Comparing fields…
```

Avoid a motionless loading spinner.

For the evaluation deployment, configure at least one warm application replica if the hosting plan permits it. This reduces cold-start risk.

---

## Phase 8 — Test and harden

Create a fixed regression dataset.

Minimum cases:

| Test                           | Expected result        |
| ------------------------------ | ---------------------- |
| Perfect sample                 | Pass                   |
| Different brand capitalization | Pass                   |
| Minor brand OCR uncertainty    | Review                 |
| Wrong brand                    | Mismatch               |
| Wrong ABV                      | Mismatch               |
| Missing ABV                    | Missing                |
| Wrong net contents             | Mismatch               |
| Missing warning                | Missing                |
| Warning title-case heading     | Mismatch               |
| Warning spelling error         | Mismatch               |
| Warning punctuation error      | Mismatch               |
| Rotated image                  | Process successfully   |
| Poor contrast                  | Process or Review      |
| Unreadable image               | Review, not false pass |
| Invalid file                   | Friendly error         |

Maintain these labels in:

```text
tests/fixtures/labels/
```

This creates a small but useful benchmark suite.

---

## Phase 9 — Deploy early

Do not leave deployment until the end.

Deploy after the first complete vertical slice.

Recommended production path:

```text
GitHub
  │
  ├── GitHub Actions
  │
  └── Docker build
        │
        ▼
Azure Container Apps
        │
        ├── Frontend
        ├── FastAPI
        └── Verification Engine
                │
                ▼
        Azure Vision OCR
```

Azure Container Apps supports deployment of containerized FastAPI applications and provides an externally accessible HTTPS endpoint.

One public application endpoint is preferable to exposing a separate browser-facing OCR service.

---

# 3. Comprehensive Specifications

# 3.1 Product Definition

## Product name

**LabelGuard AI**

## Purpose

Reduce repetitive alcohol label verification work while preserving human review for uncertain or regulatory decisions.

## Primary user

TTB label compliance agent.

## Secondary user

Technical evaluator reviewing architecture, implementation quality, and deployment.

## Non-goal

LabelGuard AI does not issue, approve, reject, or modify a COLA.

---

# 3.2 Supported Prototype Scope

Primary test profile:

**Distilled spirits**

This is the best primary scope because the assignment provides a distilled spirits example.

The architecture can support wine and malt beverage rules later.

TTB currently lists these mandatory distilled spirits elements:

* brand name
* class/type
* alcohol content
* name and address
* net contents
* health warning
* country of origin for imports
* other conditional information

TTB also states that brand name, class/type and alcohol content must appear in the same field of vision.

Do not attempt to implement all conditional TTB regulations during the take-home.

The prototype should make that limitation explicit.

---

# 3.3 Application Input Model

```ts
interface LabelApplication {
  applicationId?: string;

  beverageType:
    | "distilled_spirits"
    | "wine"
    | "malt_beverage";

  brandName: string;

  classType?: string;

  alcoholByVolume?: number;

  netContents?: {
    value: number;
    unit: "mL" | "L" | "fl_oz";
  };

  producerName?: string;

  producerLocation?: string;

  imported?: boolean;

  countryOfOrigin?: string;
}
```

Required MVP inputs:

```text
Brand Name
Class / Type
Alcohol by Volume
Net Contents
```

Optional inputs:

```text
Producer / Bottler
City / State
Imported?
Country of Origin
```

---

# 3.4 Extracted Label Model

```ts
interface ExtractedField<T> {
  value: T | null;
  rawText: string | null;
  confidence: number;
  boundingBox?: BoundingBox;
}

interface ExtractedLabel {
  fullText: string;

  brandName: ExtractedField<string>;
  classType: ExtractedField<string>;
  alcoholByVolume: ExtractedField<number>;
  netContents: ExtractedField<Volume>;
  producerName: ExtractedField<string>;
  producerLocation: ExtractedField<string>;
  countryOfOrigin: ExtractedField<string>;

  healthWarning: {
    found: boolean;
    text: string | null;
    headingCorrect: boolean | null;
    wordingCorrect: boolean | null;
    punctuationCorrect: boolean | null;
    continuous: boolean | null;
    boldHeading: boolean | null;
    confidence: number;
  };
}
```

---

# 3.5 Verification Result Model

Every check should return the same structure.

```ts
type VerificationStatus =
  | "pass"
  | "mismatch"
  | "missing"
  | "review"
  | "not_applicable";

interface VerificationCheck {
  field: string;
  status: VerificationStatus;

  expected?: string;
  detected?: string;

  confidence?: number;

  explanation: string;
}
```

Overall result:

```ts
interface VerificationResult {
  overallStatus:
    | "pass"
    | "mismatch"
    | "review";

  processingTimeMs: number;

  checks: VerificationCheck[];

  warnings: string[];
}
```

Overall decision rules:

```text
Any MISMATCH
    → overall MISMATCH

No mismatch + one or more REVIEW
    → overall REVIEW

All required checks PASS
    → overall PASS
```

---

# 3.6 Field Comparison Rules

## Brand name

Normalize:

```text
Unicode
case
whitespace
typographic apostrophes
```

Do not remove meaningful words.

Example:

```text
Stone's Throw
STONE'S THROW
→ PASS
```

---

## Alcohol content

Parse:

```text
45% Alc./Vol.
45% Alcohol by Volume
45 percent alcohol by volume
90 Proof
```

Use percent alcohol by volume as the normalized value.

If proof appears, calculate:

```text
proof / 2 = ABV
```

But proof must not replace the required alcohol-by-volume statement for distilled spirits.

TTB states that distilled spirits alcohol content is required as percent alcohol by volume. It also notes that `ABV` is not an acceptable abbreviation for the mandatory statement.

Therefore LabelGuard can produce two separate observations:

```text
VALUE CHECK
45% expected / 45% detected
PASS

FORMAT CHECK
"45% ABV"
NEEDS REVIEW
Mandatory format may not meet TTB guidance.
```

This is more useful than combining both issues.

---

## Net contents

Normalize values into milliliters.

Examples:

```text
750 mL   → 750
0.75 L   → 750
1 L      → 1000
```

Compare numerical quantity rather than textual formatting.

TTB permits common net-content forms such as `750 mL` and `1 L`.

---

## Class/type

Initial implementation:

1. case-insensitive exact comparison
2. whitespace normalization
3. punctuation normalization
4. similarity calculation
5. uncertain result → Review

Do not use an LLM to silently reinterpret a regulatory class.

---

# 3.7 Government Warning Specification

Canonical warning text must come from one constant maintained in the verification engine.

Do not place it inside an AI prompt.

TTB publishes the required statement and states that it must match the regulated text.

Validation components:

| Check                          | Result        |
| ------------------------------ | ------------- |
| Warning found                  | Pass/Missing  |
| Required wording               | Pass/Mismatch |
| Punctuation                    | Pass/Mismatch |
| `GOVERNMENT WARNING` uppercase | Pass/Mismatch |
| `GOVERNMENT WARNING` bold      | Pass/Review   |
| Body not bold                  | Pass/Review   |
| Continuous statement           | Pass/Review   |
| Separate from other text       | Pass/Review   |

TTB also defines type-size requirements based on container volume. For example, the minimum is 2 mm for containers larger than 237 mL and not more than 3 L.

However, a photograph does not reliably provide physical type size.

Therefore:

**Do not claim automated type-size verification in the prototype.**

Report:

```text
Type-size compliance
Not automatically evaluated.

Reason:
Physical scale cannot be determined reliably from this image.
```

This is a useful documented limitation.

---

# 3.8 OCR Architecture

Recommended service:

**Azure Vision Read OCR**

Reason:

* suitable for image text
* synchronous OCR
* intended for near-real-time use
* returns structured text information
* fits the stakeholder Azure environment

Microsoft describes the current Read OCR interface as suitable for near-real-time user experiences.

Create an interface:

```python
class OCRProvider(Protocol):
    async def extract(self, image: bytes) -> OCRResult:
        ...
```

Implementation:

```python
class AzureVisionOCRProvider:
    ...
```

This allows a future implementation such as:

```python
class LocalOCRProvider:
    ...
```

without changing verification rules.

---

# 3.9 API Specification

## Health

```http
GET /api/health
```

Response:

```json
{
  "status": "ok"
}
```

---

## Verify single label

```http
POST /api/v1/verify
Content-Type: multipart/form-data
```

Fields:

```text
application
image
```

Response:

```json
{
  "overallStatus": "review",
  "processingTimeMs": 2840,
  "checks": [
    {
      "field": "brandName",
      "status": "pass",
      "expected": "OLD TOM DISTILLERY",
      "detected": "Old Tom Distillery",
      "confidence": 0.99,
      "explanation": "Brand names match after case normalization."
    }
  ]
}
```

---

# 3.10 User Interface Specification

## Main screen

Header:

```text
LabelGuard AI

Alcohol Label Verification
Compare label artwork with application data.
```

Primary workflow:

```text
STEP 1
Application Details

STEP 2
Upload Label Artwork

STEP 3
Verify Label
```

Do not create a dashboard before the user has processed anything.

The primary button must be obvious:

```text
Verify Label
```

not:

```text
Run Analysis Pipeline
```

---

## Upload area

Display:

```text
Drop label image here

or

Choose Image

JPEG or PNG
```

After selection, display image preview and filename.

---

## Results screen

Top summary:

```text
Verification complete
3 passed · 1 needs review
Processed in 3.1 seconds
```

Then show each rule as a card or row.

Use words in addition to color.

Do not make green/red color the only indicator.

---

## Image evidence

When possible, highlight the detected field on the uploaded image.

Clicking:

```text
Alcohol Content
```

should highlight:

```text
45% Alc./Vol.
```

This provides immediate evidence that OCR found the correct text.

---

# 3.11 Demo Experience

The deployed application should be testable in less than one minute.

Add:

```text
Load Demo Application
```

This fills:

```text
Brand:
OLD TOM DISTILLERY

Class:
Kentucky Straight Bourbon Whiskey

ABV:
45%

Net contents:
750 mL
```

Also include downloadable test images in the GitHub repository.

Recommended fixtures:

```text
demo-pass.jpg
demo-brand-mismatch.jpg
demo-abv-mismatch.jpg
demo-warning-error.jpg
demo-low-quality.jpg
```

This is valuable because the evaluator does not need to create test data before reviewing the application.

---

# 3.12 Batch UI Specification

Separate navigation:

```text
Single Verification
Batch Verification
About
```

Batch workflow:

```text
1. Upload applications CSV
2. Upload matching label images
3. Validate file mapping
4. Start verification
5. Review table
6. Export results
```

Result table:

| ID  | Brand   | Result   | Issues |  Time |
| --- | ------- | -------- | -----: | ----: |
| 001 | OLD TOM | Pass     |      0 | 3.1 s |
| 002 | ACME    | Mismatch |      2 | 2.8 s |
| 003 | UNION   | Review   |      1 | 3.4 s |

---

# 3.13 Error Handling

Never expose stack traces.

Examples:

### Invalid type

```text
We could not read this file.

Upload a JPEG or PNG image.
```

### OCR unavailable

```text
The label could not be processed.

Try again. Your application data was not lost.
```

### Unreadable label

```text
Some label text could not be read with sufficient confidence.

Manual review is recommended.
```

### Missing CSV image

```text
3 application rows do not have matching image files.
```

---

# 3.14 Security and Privacy

For the prototype:

* do not store uploaded images
* process them in memory
* delete temporary files immediately
* keep OCR credentials server-side
* use environment variables
* never expose OCR keys to the browser
* validate MIME type and actual image encoding
* reject excessive dimensions
* enforce maximum upload size
* sanitize filenames
* remove EXIF metadata when images are transformed
* do not log full application text or image contents by default
* use HTTPS only

No database is needed for the core prototype.

This is also consistent with the stakeholder statement that this exercise does not require sensitive production data storage.

---

# 3.15 Repository Structure

```text
labelguard-ai/
│
├── README.md
├── LICENSE
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
│
├── apps/
│   ├── web/
│   │   ├── src/
│   │   ├── components/
│   │   ├── lib/
│   │   └── tests/
│   │
│   └── api/
│       ├── app/
│       │   ├── api/
│       │   ├── models/
│       │   ├── ocr/
│       │   ├── preprocessing/
│       │   ├── extraction/
│       │   └── verification/
│       │
│       └── tests/
│
├── tests/
│   └── fixtures/
│       └── labels/
│
├── docs/
│   ├── architecture.md
│   ├── assumptions.md
│   ├── test-cases.md
│   └── screenshots/
│
└── .github/
    └── workflows/
        └── ci.yml
```

If implementation speed is more important, the frontend and FastAPI service can also live inside one simpler application repository. Avoid architecture complexity that has no direct evaluation value.

---

# 3.16 README Specification

The README should contain these sections:

```text
# LabelGuard AI

## Live Demo

## Problem

## Solution

## Features

## Architecture

## Verification Logic

## Government Warning Validation

## Technology Choices

## Local Setup

## Environment Variables

## Run Locally

## Run Tests

## Docker

## Deployment

## Performance

## Test Data

## Assumptions

## Known Limitations

## Security and Privacy

## Future Improvements
```

Place the deployed URL close to the top.

Include one architecture diagram and one screenshot.

---

# 3.17 Testing Specification

## Unit tests

Test:

```text
text normalization
brand comparison
fuzzy thresholds
ABV parser
proof conversion
volume conversion
warning comparison
warning punctuation
warning capitalization
overall status calculation
```

## Integration tests

Test:

```text
image → OCR → extraction
API multipart upload
invalid image
OCR failure
low confidence
```

## Golden-image tests

Use fixed label images with expected outputs.

This is important because OCR behavior should be measured against real examples.

---

# 3.18 CI Specification

GitHub Actions should execute on every push and pull request.

Pipeline:

```text
Install
 ↓
Lint
 ↓
Type check
 ↓
Unit tests
 ↓
API tests
 ↓
Frontend build
 ↓
Docker build
```

Do not create a large CI system.

A single clean workflow is sufficient.

---

# 3.19 Performance Specification

The most important technical performance acceptance criterion is:

```text
Normal single-label verification:
p95 ≤ approximately 5 seconds when warm
```

The README should contain measured results rather than only claiming that the application is fast.

Example:

```text
Benchmark
20 test images
Median: 2.7 s
p95:    4.4 s
```

If actual numbers are slower, report the actual numbers.

---

# 3.20 Observability

Use structured logs.

Example:

```json
{
  "request_id": "req_123",
  "event": "verification_complete",
  "duration_ms": 2865,
  "ocr_ms": 2310,
  "result": "review",
  "checks": 6
}
```

Do not log:

```text
full uploaded image
complete warning text
applicant personal information
OCR API secret
```

---

# 3.21 Important Assumptions

Document these explicitly.

### Assumption 1

The prototype verifies label information against user-entered application values. It does not connect to COLAs Online.

This matches the stated prototype scope.

### Assumption 2

Distilled spirits are the main regulatory test case.

### Assumption 3

Case-only changes in a brand name are not treated as substantive mismatches.

### Assumption 4

Low OCR confidence results in manual review.

It never results in an automatic pass.

### Assumption 5

Physical type-size compliance cannot be reliably determined from a normal photograph without physical scale information.

### Assumption 6

The application processes uploaded data transiently and does not retain it.

### Assumption 7

This prototype provides decision support. It does not constitute an official regulatory determination.

---

# 3.22 Known Limitations

Include these before submission:

* difficult glare can reduce OCR accuracy
* curved bottle labels can distort text
* bold-font detection is less reliable than textual verification
* physical font dimensions cannot be established from arbitrary images
* same-field-of-vision rules cannot always be proven from one photograph
* beverage-specific regulatory requirements are not fully implemented
* batch processing is prototype-scale
* no COLAs integration exists
* OCR service availability affects processing

Showing these limitations is preferable to presenting uncertain automation as reliable.

---

# 3.23 Delivery Sequence

The implementation order should be:

```text
1. Repository and project skeleton
       ↓
2. Form + image upload
       ↓
3. OCR integration
       ↓
4. Brand verification
       ↓
5. ABV verification
       ↓
6. Government warning verification
       ↓
7. Result UX
       ↓
8. Deploy first working version
       ↓
9. Class/type + net contents
       ↓
10. Image preprocessing
       ↓
11. Automated tests
       ↓
12. Batch workflow
       ↓
13. Performance measurement
       ↓
14. README and documentation
       ↓
15. Final deployment verification
```

This order keeps a working deployed version available throughout development.

---

# 3.24 Final Submission Gate

Do not submit until all of these are true:

### Repository

* public or evaluator-accessible
* all source code present
* no secrets committed
* `.env.example` present
* clean commit history
* tests pass
* README works from a clean clone

### Application

* public HTTPS URL
* no login required
* fresh browser test succeeds
* sample workflow succeeds
* error workflow succeeds
* mobile-width layout does not break
* no console errors
* OCR credentials work in production
* application does not sleep during evaluation if avoidable

### README

* live URL
* screenshot
* architecture
* setup
* test commands
* deployment approach
* assumptions
* limitations
* technology choices
* performance numbers

### Demonstration

The evaluator should be able to understand the product in this sequence:

```text
Open URL
   ↓
Load demo
   ↓
Upload test label
   ↓
Click Verify Label
   ↓
Receive result within about 5 seconds
   ↓
See exactly why each field passed or failed
```

That flow directly demonstrates the strongest themes in the Treasury assignment: speed, simplicity, correctness, explainability, error handling, engineering quality, and attention to stakeholder requirements.

---

# Recommended Scope Decision

For this take-home, the strongest implementation is not a large generative-AI system.

It is a small, reliable verification system with AI/OCR at the perception boundary and deterministic code for decisions.

Use AI/OCR for:

```text
"What text is on this image?"
```

Use normal software rules for:

```text
"Does 45% equal 40%?"
"Does the warning match the required warning?"
"Is the brand equivalent after case normalization?"
"Is OCR confidence too low for an automatic decision?"
```

Use the human agent for:

```text
"Does this ambiguous case require regulatory judgment?"
```

That division of responsibility is technically simpler, easier to test, easier to explain, and better aligned with the stakeholder interviews than a single multimodal-model prompt that returns `approved` or `rejected`.
