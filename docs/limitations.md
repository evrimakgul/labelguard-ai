# Known Limitations

- Glare, curvature, perspective, decoration, unusual fonts, and low resolution can reduce OCR quality.
- Brand and class/type candidate selection is deterministic and optimized for the supplied single-label workflow, not every possible label composition.
- Bold heading, non-bold body, physical type size, and statement separation are not automatically verified.
- A photograph cannot always prove same-field-of-vision requirements.
- The prototype does not implement every conditional rule for distilled spirits, wine, or malt beverages.
- No COLAs integration, identity system, case history, or document retention policy is included.
- Fixture demo mode is not OCR and only reads embedded text from the repository fixtures.
- Local Tesseract accuracy varies with font, decoration, language data, and host CPU resources.
- Live OCR and timing cannot be validated on this Windows host until Tesseract is installed; fixture mode is not a substitute for that benchmark.
- Batch processing and CSV workflows are intentionally deferred until P0 and P1 remain stable.
