# Known Limitations

- Glare, curvature, perspective, decoration, unusual fonts, and low resolution can reduce OCR quality.
- Brand and class/type candidate selection is deterministic and optimized for the supplied single-label workflow, not every possible label composition.
- Bold heading, non-bold body, physical type size, and statement separation are not automatically verified.
- A photograph cannot always prove same-field-of-vision requirements.
- The prototype does not implement every conditional rule for distilled spirits, wine, or malt beverages.
- No COLAs integration, identity system, case history, or document retention policy is included.
- Fixture demo mode is not OCR and only reads embedded text from the repository fixtures.
- Local Tesseract accuracy varies with font, decoration, language data, and host CPU resources.
- Bounding boxes can be approximate after geometric preprocessing.
- The current live Tesseract pass/rotation/contrast fixtures miss the brand heading and therefore fail acceptance; fixture demo mode does not reveal this defect.
- Live Tesseract benchmarking is paused until the brand-detection and unreadable-image behaviors are corrected.
- Batch processing and CSV workflows are intentionally deferred until P0 and P1 remain stable.
