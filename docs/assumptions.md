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
11. Tesseract 5.5.3 with English and orientation data is installed on the current Windows host.
12. Podman 6.0.2 is the selected free OCI engine. Its rootless WSL2 machine, image build, container process startup, internal health, and direct machine-address access pass; Windows localhost forwarding remains unavailable.
13. GitHub CLI is authenticated through the operating-system keyring, and no GitHub token belongs in project configuration.
14. No final public host will be selected until it provides HTTPS without billing information, a payment method, prepaid credits, or a paid subscription.
15. Deterministic fixtures do not replace live OCR evidence; the current Windows Tesseract acceptance and benchmark therefore run as separate opt-in checks.
16. LabelGuard AI provides decision support and never represents an official TTB determination.
17. Codex executes all accessible local verification and runtime operations. Sandbox approval is distinct from a user running commands manually; approved host access to Podman, WSL and the GitHub keyring works.
18. Direct Podman-machine IP access is sufficient for local acceptance while Windows localhost forwarding is unavailable. A public HTTPS URL remains required for final delivery.
19. The current P1 inventory follows the accepted continuation plan; producer/importer and country-of-origin checks are deferred expanded beverage rules. SPEC now reflects that scope explicitly.
