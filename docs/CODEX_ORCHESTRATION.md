# Codex orchestration

Persistent context contains operating rules; retrieve project knowledge only when needed.

## Ownership and recovery

The root owns planning, dependencies, architecture, task decomposition, integration, review, verification, consistent documentation, continuity, and delivery readiness. Start from AGENTS, CODEX_STATE, Git status/diff/untracked files/recent commits, then only relevant status or product sections. Git and current runtime evidence supersede stale checkpoints. Preserve completed and unrelated work; verify again only when changes or contradictory evidence warrant it.

Before requesting manual work, attempt the task directly. If sandbox permissions block host resources, use the runtime approval mechanism and retry. Record the exact resource, attempted action, error, and necessary user action only when access remains blocked. Do not read or print credential contents. Normal commands belong in deployment documentation, not USER_REQUIREMENTS.

## Delegation decision

Do not delegate automatically. Delegate only a bounded independent task whose parallelism, reduced root context, or lower expected usage outweighs context transfer, coordination, and review. Tiny edits are usually cheaper locally. Reuse verified findings. Do not spawn duplicate investigations or concurrent writers to the same file.

Each assignment includes one objective, allowed files/resources, concise necessary context, success criteria, required verification, write boundaries, and a compact return format (finding/change, evidence, unresolved issue). Prefer a fresh context rather than full history. Inspect the runtime's actual capabilities before selecting settings.

## Dynamic intelligence selection

Estimate complexity, ambiguity, risk, context volume, verification difficulty, and failure/rework cost. Choose the lowest-capability available model and lowest supported reasoning effort likely to succeed reliably. Do not inherit the root's model automatically or maintain permanent model-to-task mappings. A stronger model once can cost less overall than repeated weak attempts.

Optimize expected total consumption: model + reasoning + context + orchestration + retry/rework. Correctness and constraints remain hard requirements. Explicitly select runtime-exposed model/effort controls when available; otherwise use available context/task controls and do not claim a selection that did not occur. Do not invent pricing or usage measurements.

Review results before integration. Escalate only if evidence is inadequate, incorrect, ambiguous, or difficulty increased; narrow or stop repeatedly failing work. Reuse an existing agent for a follow-up when cheaper than recreating context. The root resolves conflicts, verifies integration, and owns the final answer.

## Parallel work and execution

Parallelize independent reads/tests or disjoint bounded work. Keep dependent changes, builds, starts, readiness checks, and tests sequential. A tool session ID means work is still running: wait for its completion and check exit status before consuming its output. Do not run verification during container replacement. Use bounded waits and concise progress updates.

## Stages and checkpoints

Use small stages: recover -> change -> targeted verification -> state update -> logical local commit -> next stage. Update CODEX_STATE after recovery, meaningful decisions/changes/tests, new blockers, before risky or large delegated stages, at low usage, and before stopping. Include exact unfinished operation, next commands, current runtime identifiers, Git state, evidence, and known limitations. Keep it short; PROJECT_STATUS owns overall evidence and delivery status, not a second execution history.

Keep source and generated changes distinguishable. Review every changed file, preserve secrets boundaries, and use commits as recoverable milestones; never claim a clean tree or completed check without inspecting it. Historical image IDs/addresses must be labeled and refreshed when needed.

## Usage preservation

Query actual account usage near the start of substantial work, between substantial stages, before delegation waves, and periodically during long work (for example every 10-15 minutes). Record timestamp and remaining percentages only when supplied by the runtime. Use the most constrained applicable window; account usage is shared and is not exact per-task consumption. Never redeem a reset, purchase credits, or change subscriptions without explicit authorization.

| Remaining capacity | Behavior |
| --- | --- |
| Above ~50% | Normal bounded execution |
| ~25-50% | Smaller stages, economical delegation |
| ~15-25% | No large new workstream; finish smallest safe unit and essential verification; checkpoint |
| ~10-15% | Preservation: stop substantive new work; save exact continuation and stable local checkpoint |
| Below ~10% | Preserve immediately; avoid optional analysis, cleanup, and repeated checks |

Reserve roughly the final 15-20% for safe completion/checkpointing. If usage is unavailable, say so, use shorter stages and checkpoint often. Monitoring cannot guarantee uninterrupted execution; no background monitoring automation is implied.

## Instruction migration map

The former AGENTS mission/autonomy/hierarchy remain in the compact AGENTS file; detailed recovery/delegation lives here. Its product goal and 20 P0 items map to SPEC executive summary and Phase 0 inventory; the accepted P1/P2 lists now live there as well. Stack, seven concern boundaries, prohibited complexity, and safe result wording are retained in architecture.md. The illustrative OCR protocol is already in SPEC 3.8 and implemented in app/ocr/base.py. Current priorities and delivery sequence live in IMPLEMENTATION_PLAN; status and assumptions remain in their existing documents. Treasury source is unchanged.

## Publication authority

No push, deployment, provisioning, cloud account creation, paid resource, external commitment, or message to others without the appropriate gate and user authorization. Completing local checks does not itself grant publication permission. A public/evaluator-accessible source repository and public HTTPS application remain final Treasury deliverables; the host must meet the no-cost/no-billing constraints.
