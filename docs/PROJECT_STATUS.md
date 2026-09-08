# Project status

Updated: 2026-09-08. This is current delivery status; historical sizing experiments remain in HOSTING_RESEARCH.

## Delivery gate

The user deployed Render Free at **https://labelguard-ai-4g5s.onrender.com**. Public core behavior is verified. Documentation publication and its CI are the final in-progress step; see SUBMISSION_READINESS for the delivery checklist. No further product implementation or P2 is required for the accepted prototype.

- Source: https://github.com/evrimakgul/labelguard-ai — verified public.
- Deployed application commit: **919e241**, confirmed by the user and supplied Render deployment screenshot.
- Screenshot shows successful deployment, free-instance warning, Uvicorn port 10000, and worker count 1.
- User confirms $0/month Free, no billing information/payment method, prepaid credits, or paid subscription.
- Auto-Deploy setting is unknown. No need to enable it or create another service.
- App remains decision support, not a regulatory approval system.

## Public acceptance evidence (2026-09-08)

- Public HTTPS root, health, favicon and demo download work without login.
- Real API provider is `local-tesseract`, not demo OCR.
- Seven fixtures: pass, brand mismatch, ABV mismatch, warning error, rotation, low contrast and unreadable — all expected statuses.
- Invalid image returns safe 400; malformed application returns safe 422.
- Desktop: form demo loader, upload, pass and mismatch results; expected/detected values; OCR text/timing disclosure; click and keyboard evidence selection.
- Error recovery: invalid PNG produces a friendly error and preserves application values; replacing it with a valid unreadable PNG clears the error and returns Needs Review.
- Mobile width 390: pass workflow, evidence, timings, no horizontal overflow.
- Fresh successful flows had no JavaScript/console errors. Deliberate invalid upload produced its expected HTTP 400 resource-console entry, not an unhandled application exception.
- Screenshots: `screenshots/public-desktop.png` and `screenshots/public-mobile.png`.
- Evidence summary: `verification/public-2026-09-08.json`.

Twenty sequential warm pass requests after the seven-case warmup: wall median/p95 **4857.8/5304.0 ms**, API **4731.0/5218 ms**, OCR **3163.5/3495 ms**. No concurrent browser OCR during this benchmark. This is near the assignment's approximate five-second goal, not a strict ≤5-second pass. Cold-start duration was not measured.

## Quality and scope

Runtime source 919e241 passed [CI 34183695397](https://github.com/evrimakgul/labelguard-ai/actions/runs/34183695397): backend lint/format/deterministic tests, frontend lint/types/6 tests/production build, Docker build and real OCR with a thread-default assertion. Previous local native validation passed 42 backend tests (35 deterministic + 7 live). Existing dependency/action-runtime deprecation warnings are non-failing maintenance items.

This delivery change updates documentation and public screenshots only. Existing application behavior, tests and Treasury source are preserved. Final documentation CI will be recorded after publication.

P0/P1 supported core is complete. Batch/CSV, expanded beverage-specific rules, producer/importer/origin checking, reliable typography/physical measurement, accounts and COLAs integration remain deferred or explicitly unsupported. No claim that a Pass means full regulatory compliance.

## Hosting trade-offs

Render Free sleeps after inactivity, can restart/suspend under its free allowances, and is not an always-on production SLA. The user selected this host; earlier research/local-quota rejection was a preliminary sizing concern, not a measurement of the actual public service. Public results supersede simulation for this deployment; historical measurements remain labeled.

Normal operation requires no paid OCR, app secret or external OCR API. Public HTTP checks do not inspect Render billing, internal environment, exact OCR binary version or full logs; those claims are limited to user evidence, repository configuration and observable functionality.

## Ownership

Codex owns final document reconciliation, publication and CI verification. User owns the actual submission of the two URLs. Do not request further manual commands, enable paid options, create services, or change account/deployment settings. Stop once the final documented readiness check is complete.
