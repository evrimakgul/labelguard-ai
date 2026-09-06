# LabelGuard AI — Codex operating rules

Build and prepare the Treasury take-home prototype. The root agent owns project management, integration, verification, and delivery readiness. Keep replies concise.

## Authority and retrieval

The repository is authoritative: `docs/TREASURY_ASSIGNMENT.md` > `docs/SPEC.md` > this file > engineering judgment. Explicit user overrides apply, including the no-cost platform requirement. Preserve the Treasury source unchanged.

On recovery read `docs/CODEX_STATE.md`, inspect Git status/diff/untracked files/recent commits, then retrieve only the documents relevant to the current gate. Read Treasury/SPEC before product implementation decisions; reuse still-current reads.

- Product requirements and P0/P1/P2 inventory: `docs/SPEC.md`.
- Architecture and concern boundaries: `docs/architecture.md`.
- Current evidence/delivery gate: `docs/PROJECT_STATUS.md`; execution sequence: `docs/IMPLEMENTATION_PLAN.md`.
- Detailed delegation, model selection, usage preservation, and recovery: `docs/CODEX_ORCHESTRATION.md`.
- Run/deploy procedures: `docs/deployment.md`; genuine human dependencies only: `docs/USER_REQUIREMENTS.md`.

## Execution

Work autonomously through the current gate. Use safe assumptions, record material ones in `docs/assumptions.md`, and continue. Perform accessible terminal, Git, Podman, WSL, testing, and browser work yourself; try available access and approval mechanisms before requesting manual commands.

Preserve useful work and unrelated edits. Diagnose/fix failing checks; never stop at planning/scaffolding or weaken valid tests. Complete P0 before optional work, stabilize P1 before P2, and keep P2 deferred for the current submission.

Delegate only independent bounded work when expected total usage (including context, reasoning, coordination and rework) benefits. Choose the lowest adequate available model/effort dynamically; root reviews and integrates results. Do not delegate tiny work automatically.

Update `docs/CODEX_STATE.md` after significant stages, decisions, checks, blockers, before risky/delegated work, and before stopping. Verify and create logical local commits. Check actual usage when available; preserve a safety reserve and checkpoint before low capacity. Never invent usage figures or claim monitoring guarantees.

## Hard boundaries

No paid OCR/cloud services, billing information, payment method, prepaid credits, paid subscriptions, unnecessary external accounts, or secrets in Git. Local Tesseract remains the production default behind `OCRProvider`; fake/demo OCR keeps automated unit tests deterministic.

LabelGuard supports human review and must never claim regulatory approval. Keep uncertainty and limitations visible. Use the minimal architecture in `docs/architecture.md`.

Do not push, deploy, provision, create cloud accounts, or make external commitments without the required gate and explicit user authorization. Local implementation and verification continue without deployment credentials. Finishing local gates does not grant publication permission.
