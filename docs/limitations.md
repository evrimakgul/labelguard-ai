# Known Limitations

- Render Free hosts the public prototype. It can sleep after 15 idle minutes, wake slowly (roughly a minute per platform documentation), restart or suspend under free-tier limits. This is not a production SLA. Cold-start time was not measured in the 2026-09-08 verification.
- Public warm benchmark: 20 demo-pass requests, wall median 4.86 seconds/p95 5.30 seconds. This is near the approximate five-second goal, not a strict ≤5-second p95 pass; network, load and artwork vary. No keep-alive workaround is configured.

- Glare, curvature, perspective, decoration, unusual fonts, and low resolution can reduce OCR quality.
- Brand and class/type candidate selection is deterministic and optimized for the supplied single-label workflow, not every possible label composition.
- Bold heading, non-bold body, physical type size, and statement separation are not automatically verified.
- A photograph cannot always prove same-field-of-vision requirements.
- The prototype does not implement every conditional rule for distilled spirits, wine, or malt beverages.
- Producer/importer name/address and country of origin are not checked. Selecting a beverage type does not enable a complete beverage-specific regulatory ruleset.
- Brand/class similarity ≥95% can pass as a prototype heuristic; similar but materially different wording can need human review despite that result. Warning wording uses a separate exact word-sequence check.
- No COLAs integration, identity system, case history, or document retention policy is included.
- This public prototype has no authentication, abuse-rate limiting or federal production accreditation. Use only synthetic/non-sensitive sample data.
- Fixture demo mode is not OCR and only reads embedded text from the repository fixtures.
- Local Tesseract accuracy varies with font, decoration, language data, and host CPU resources.
- Bounding boxes can be approximate after geometric preprocessing.
- Sparse OCR output below the usable-text threshold is conservatively classified as Needs Review; a human must inspect borderline images.
- Live benchmark timings are host- and fixture-specific and do not guarantee performance on arbitrary artwork or deployment hardware.
- Batch processing and CSV workflows are intentionally deferred until P0 and P1 remain stable.
