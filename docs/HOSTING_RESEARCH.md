# Public hosting assessment

Checked against official documentation on 2026-09-07. Research only: no account created, host selected, resource provisioned, or deployment performed. Existing local and CI acceptance remain valid; P2 stays deferred.

## Findings

**Koyeb and Northflank: rejected.** Koyeb's pricing FAQ requires a credit card; Northflank's billing documentation requires a payment method for creating resources on every plan, including its sandbox. Free compute is not sufficient under this project's no-payment-method constraint. [Koyeb FAQ](https://www.koyeb.com/docs/faqs/pricing), [Northflank billing](https://northflank.com/docs/v1/application/billing/pricing-on-northflank)

**Hugging Face Docker Spaces: rejected.** Current documentation requires a paid plan to create Docker Spaces, even though CPU Basic has no hourly charge. Older free-compute guides are insufficient evidence. Static hosting cannot run the existing FastAPI/Tesseract service. [Spaces overview](https://huggingface.co/docs/hub/spaces-overview)

**Render Free web service: conditional candidate, not approved.** Render documents free service creation and operation without a payment method, including suspension rather than supplementary billing when no payment method is present. This supports further evaluation, not a guarantee of account-specific onboarding eligibility. If registration or service creation requires billing details, a card, credits, or a paid plan, stop and reject this path; do not provide them. Do not use a workspace with an existing payment method. [Free deployment](https://render.com/docs/your-first-deploy), [billing FAQ](https://render.com/docs/faq)

Render supports Docker web services and a public onrender.com address with managed TLS. Building the existing repository-root Dockerfile would keep the static frontend and local Tesseract API together, without a database, external OCR service, registry account, or app secret. This is an architectural fit inferred from the repository and platform documentation, not a tested deployment. [Web services](https://render.com/docs/web-services), [Docker support](https://render.com/docs/docker)

## Remaining technical risks

- Free compute is 0.1 CPU and 512 MB RAM. Our unrestricted local benchmark does not establish performance or memory safety at those limits. [Compute plans](https://render.com/docs/compute-plans)
- Idle services sleep after 15 minutes; restarting takes about a minute. Document cold starts separately from the warm approximately five-second target. Do not add artificial keep-alive traffic or promise continuous availability.
- Free service hours, bandwidth and build allowances are limited; services/builds can be suspended. Filesystem state is ephemeral, which fits transient image processing. Render explicitly does not recommend free instances for production applications; this proposal is for the assessment prototype only. [Free-tier limitations](https://render.com/docs/free)
- Free services have no SSH/dashboard shell. Public OCR verification must use the existing real-HTTP verifier and deployment logs, not promise a remote `podman exec` equivalent. Keep local container Tesseract/version evidence distinct from hosted functional evidence. [Shell availability](https://render.com/docs/ssh)

## Local feasibility result: failed at default settings

On 2026-09-07, Codex tested verified image `4c2d0173a860192822bf39fe348225ad40265773a1c272a6905a3e5acaa603ae` in isolated container `labelguard-ai-resource-check`, published at VM port 8002. Effective cgroup values were `cpu.max=10000 100000`, `memory.max=536870912`, and `memory.swap.max=0`: the intended limits were enforced.

Readiness succeeded after a bounded startup retry. The unchanged verifier (`--requests 20`) stopped on its **first label**, returning HTTP 503; therefore the seven-case suite and 20-request benchmark did **not** complete. Logs reported `Local OCR timed out.` A separate demo-pass multipart request confirmed safe `ocr_unavailable`, HTTP 503, in 12.861948 seconds total. The configured OCR timeout remained 8 seconds; total request time includes other processing and scheduling.

Peak cgroup memory was 220,921,856 bytes (about 210.7 MiB), with zero OOM/OOM-kill events. Final CPU counters recorded 526 throttled periods out of 682 and 40,349,603 throttled microseconds. The container remained running, not OOM-killed. This indicates CPU pressure rather than an observed memory failure; it does not prove that every allowed upload fits the memory limit. The disposable container was stopped and removed; both existing containers were preserved.

**Decision:** do not approve deployment on this evidence. Local strict-quota performance is not equivalent to Render scheduling, but the default application failed this feasibility screen. No timeout/assertion was relaxed, and no application code changed. Next Codex stage is a small CPU-efficiency investigation (including thread oversubscription) or another qualifying-host assessment. Any optimization must retain all existing correctness checks and rerun the complete constrained suite before claiming success. No user account or deployment action is needed yet.

## Single-thread follow-up: correctness passed, speed target missed

The follow-up used the same image and effective resource limits, with only `OMP_THREAD_LIMIT=1` added. The completed verifier output was recovered during cleanup after the user requested a usage stop: all seven live cases and both safe 400/422 error cases passed. Twenty warm demo-pass requests measured wall median/p95 **9070.0/9599.8 ms**, API **8999.0/9593 ms**, and OCR **5799.0/6097 ms** (nearest-rank p95). The 8-second OCR timeout and all assertions were unchanged. Container `labelguard-ai-thread-check` was stopped and removed successfully.

This establishes a useful timeout improvement, not a five-second performance pass or Render deployment approval. It remains a strict local CPU-quota simulation, not a public-host benchmark. Do not reuse the default-thread run's memory measurements as measurements of this follow-up.

The Docker runtime now defaults to `OMP_THREAD_LIMIT=1`; CI asserts that setting before exercising real OCR. Native users may export the same variable explicitly; it is not injected into every host process by the application. Runtime overrides remain possible for separately benchmarked hardware. This follows Tesseract's documented single-thread control and the measured quota result. [Tesseract FAQ](https://tesseract-ocr.github.io/tessdoc/FAQ.html)

## Rebuilt image sizing: 0.25 CPU passes the fixture target

The rebuilt `labelguard-ai:single-thread` image (`d653e81cfa2fac0899119b27bae06c35fcc8ae048fb8f33cd3be0089c175e538`) includes the default without a `podman run` thread override. Its temporary sizing container enforced `cpu.max=25000 100000`, 536870912-byte RAM, and zero swap. Runtime assertion confirmed `OMP_THREAD_LIMIT=1`; Tesseract 5.5.0 with eng/osd and dependency consistency passed.

All seven fixtures and 400/422 cases passed. Twenty warm demo-pass requests measured wall median/p95 **3789.1/3996.8 ms**, API **3719.0/3917 ms**, OCR **2399.0/2608 ms**. Peak cgroup memory was 137,883,648 bytes (about 131.5 MiB), with no OOM events. The container was removed after verification; the two existing review containers and old image were preserved.

This is a measured local sizing point, not a proven minimum, concurrency capacity, or hosted SLA. The image rebuild also re-resolved allowed dependency ranges, so do not attribute differences from the older image solely to the CPU change. Render Free offers less CPU than this tested point; no upgrade, account creation, or deployment is authorized. Next: find a qualifying host with adequate measured resources, or investigate further performance improvements without reducing OCR correctness.

## Reproduction procedure (Codex-owned)

1. Refresh Podman/WSL access and identify the already verified image. Preserve both existing containers.
2. Run a separately named disposable container from that image with a 512 MB memory limit, no additional swap, and 0.1 CPU quota. Inspect its effective limits; unsupported rootless resource controls invalidate the simulation.
3. Run `scripts/verify_container.py` against it, including all seven cases and the 20-request benchmark; inspect container exit/OOM state and memory usage. Do not weaken assertions or timeouts to make this pass.
4. Record measured timings and memory failures. This is a local feasibility screen, not a prediction of Render hardware performance. Stop/remove only the disposable test container afterward.
5. If feasible, present the concrete deployment approval request below. If infeasible, investigate optimization or another qualifying host without switching to paid compute or changing product scope.

## Conditional deployment proposal: requires separate approval

Only after local feasibility: request approval to use/create one necessary Render account and deploy one **Free** Docker web service from the existing GitHub repository. No account action is required now. Codex performs accessible setup; the user handles only unavoidable sign-in/authorization challenges, without sharing credentials.

Proposed settings: repository-root build context and Dockerfile, reviewed `main` revision, `OCR_PROVIDER=tesseract`, `PORT=8000`, health path `/api/health`, existing Docker start command, same-origin frontend/API. Do not set `TESSERACT_CMD` to a Windows path or a localhost frontend API override. No disk, database, custom domain, paid build tier or other add-on. Disable automatic deployment initially so publication does not implicitly deploy later changes. Recheck the actual Free selection and no-billing path before creating the service.

Keep Dockerfile HEALTHCHECK for engines that support it; the host HTTP health probe is the deployment gate. OCI ignoring Docker health metadata is not itself an application failure and does not justify changing image format for this candidate.

After an approved deployment, Codex verifies public HTTPS/no-login access, live OCR fixture/error flows, desktop/mobile browser behavior, warm timings and a separate cold-start observation. Update README with the real URL and measured limitations, inspect CI for any source/config changes, then review both Treasury deliverables. No final submission readiness claim until these checks pass.
