# Assumptions

1. The prototype compares a user-entered application with one label image and does not integrate with COLAs Online.
2. Distilled spirits are the primary regulatory test profile supplied by the assignment. Wine and malt beverage values can be entered, but broader beverage-specific rules are outside the first release.
3. Case-only, whitespace-only, Unicode-equivalent, and typographic-apostrophe differences are not substantive brand mismatches.
4. OCR confidence below 80% requires human review and never automatically passes.
5. The application treats a missing required field as an overall mismatch and unreadable OCR as overall Needs Review.
6. Physical type size cannot be established from an arbitrary image without trustworthy scale information.
7. OCR alone cannot reliably prove bold styling, body-font weight, statement separation, or continuity; those items are disclosed as not evaluated.
8. Uploaded images and application values are transient and are not retained.
9. The fixture-only demo provider reads explicit metadata embedded in repository fixtures. It returns no text for arbitrary images.
10. Normal operation uses local Tesseract and requires no OCR API key, paid service, or cloud subscription.
11. Tesseract is not installed on the current Windows host; fixture OCR keeps deterministic development unblocked, and the container installs the complete runtime.
12. Podman is the selected free OCI engine for future local container verification because it requires no hosted account or payment information.
13. No final public host will be selected until it provides HTTPS without billing information, a payment method, prepaid credits, or a paid subscription.
14. LabelGuard AI provides decision support and never represents an official TTB determination.
