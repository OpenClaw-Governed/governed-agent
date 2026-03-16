# TASKS.md -- OpenClaw Task Board

**Last updated:** 2026-03-16 10:45 PT

## Active

### P0: Mission Control Reorientation [DONE]
- [x] Strip trading code from home page
- [x] Rewrite home page: fidelity, verdicts, boundary triggers, audit trail, agents
- [x] Rewrite sidebar: governance-first, no trading link
- [x] Add /api/audit route (reads live from telos_audit.jsonl)
- [x] Relocate trading page + portfolio API to _relocated_trading/
- [x] Build passes clean, no trading routes in output
- [x] Screenshot verified -- dashboard shows live governance telemetry

### P1: Diary Content Pipeline [IN PROGRESS]
- [x] Entry 03: "The Day the Scoring Started" (seq 4921-4941)
- [x] Posted to Discord #diary
- [x] Committed to governed-agent repo
- [ ] Entry 04: draft from boundary trigger patterns (23 triggers, web_navigate scoring)
- [ ] Queue formatted X/LinkedIn versions for post-April 9

### P2: Discord Content Flow [IN PROGRESS]
- [x] Bot live, server operational (25 channels)
- [x] Diary entry posted to #diary
- [x] Governance alert posted to #governance-live
- [ ] Webhook-based governance feed (avoid full bot deploy)
- [ ] Welcome message and channel descriptions for public launch
- [ ] Community scanner (local, no bot token needed)

### P3: governed-agent Repo Maintenance [IN PROGRESS]
- [x] Telemetry summary committed (first live scoring)
- [x] Diary entry committed
- [x] Stream/engagement data committed
- [x] TASKS.md updated
- [ ] Update MEMORY.md stale references (telos_hardened -> TELOS IP, GPT-5.3-codex -> Claude Opus 4.6)
- [ ] Populate repo HANDOFF.md

### P4: Sub-Agent Governance Documentation [QUEUED]
- [ ] Document full lifecycle: PA authoring -> JB review -> commissioning -> activation -> governance
- [ ] Identify governed tool calls per step
- [ ] Propose daemon categorization for "authority delegation" actions
- [ ] Spec for T to implement
- [ ] Advisory agents NOT commissioned until process documented and JB approves

### P5: Corpus Seeding [QUEUED]
- [ ] Day Two observations (pending since March 9)
- [ ] Feed Stewart's corpus with real governance events
- [ ] Dual-persist to Supabase + ChromaDB

## Completed (This Session)

- [x] Plugin build fix (bridge.ts numerical scores stripped)
- [x] Plugin event shape fix (toolName/params -> action.tool_name/action.input normalization)
- [x] gateMode support wired into config.ts/types.ts/index.ts
- [x] Governance daemon restarted and healthy
- [x] X API cost analysis and zero-cost strategy (proposals/x-cost-zero-strategy.md)
- [x] Stream monitor circuit breaker + rule caching (commit 95ce3ea)
- [x] StewartBot 16 commits pushed (clean working tree)
- [x] Observatory dashboard running on :8501

## Blocked

- **X API:** Spend cap hit, resets April 9. No paid API calls. Draft content locally.
- **Advisory agents:** Requires P4 documentation + JB approval before commissioning.
- **Enforce mode:** Observe mode active. web_fetch scoring too low (0.272) for enforce.

## Standing Rules

- No sub-agent commissioning without JB approval
- No X API calls until April 9 + JB approval
- No trading development
- No governance threshold/boundary/PA modifications (T's domain)
- No pushes to repos other than governed-agent without JB approval
- All tool calls scored in observe mode -- more work = more telemetry
