# TASKS.md -- OpenClaw Task Board

**Last updated:** 2026-03-16 10:55 PT
**RPM Status:** ACTIVE -- all analysis/design delegated, QGM gates enforced
**Delegation model:** Opus (MLX server down, logged)

## Active Delegations

| Task ID | Type | Delegated To | Status | QGM |
|---------|------|-------------|--------|-----|
| p1-governance-protocol-analysis | analysis_design | Opus subagent | RUNNING | pending |
| p3-diary-entry-04 | analysis_design | Opus subagent | RUNNING | pending |

## Priority Queue

### P0: RPM/QGM Reactivation [DONE]
- [x] RPM protocol loaded and active
- [x] Delegation pipeline reactivated
- [x] First delegations spawned with reverse prompts (problem/evidence/boundaries)
- [x] delegation_log.jsonl entries written
- [x] TASKS.md updated with RPM classifications

### P1: Sub-Agent Governance Protocol [IN PROGRESS -- PRINCIPLED]
**Type:** analysis_design | **RPM:** reverse prompt delegated
- [x] Evidence gathered: 12 daemon event types, 9-step onboarding CLI, agent registry states
- [x] Sub-agent spawned with problem statement + evidence + boundaries
- [ ] QGM gate on sub-agent output (D1-D5)
- [ ] Synthesize into proposals/agent-creation-governance.md
- [ ] JB review required before any commissioning

### P2: Mission Control Reorientation [DONE -- PRINCIPLED]
**Type:** execution (done by OC directly)
- [x] Home page: governance fidelity, verdicts, boundaries, audit trail, agents
- [x] Sidebar: governance-first, no trading
- [x] /api/audit route (live from telos_audit.jsonl)
- [x] Trading page + portfolio API relocated to _relocated_trading/
- [x] Build clean, screenshot verified

### P3: Diary Content Pipeline [IN PROGRESS -- ITERATIVE, DELEGATED]
**Type:** analysis_design | **RPM:** reverse prompt delegated
- [x] Entry 03: "The Day the Scoring Started" (written by OC, pre-RPM reactivation)
- [x] Entry 04: delegated to writer sub-agent with telemetry evidence + voice guide
- [ ] QGM gate on Entry 04 draft
- [ ] Post to Discord #diary
- [ ] Commit to governed-agent repo
- [ ] Queue X/LinkedIn versions for post-April 9

### P4: Discord Content Flow [QUEUED -- ITERATIVE, DELEGATE]
**Type:** hybrid | **RPM:** delegate content creation
- [x] Bot live, diary Entry 03 posted
- [ ] Governance webhook feed
- [ ] Welcome message (delegate drafting)
- [ ] Channel descriptions for public launch

### P5: governed-agent Repo Maintenance [IN PROGRESS -- ITERATIVE]
**Type:** execution
- [x] Telemetry summaries committed
- [x] TASKS.md updated
- [x] HANDOFF.md populated
- [ ] Fix MEMORY.md stale references
- [ ] Repo HANDOFF.md

### P6: Corpus Seeding [QUEUED -- ITERATIVE]
**Type:** execution
- [ ] Day Two observations from real governance events
- [ ] Dual-persist to Supabase + ChromaDB

## Completed (This Session)

- Plugin build fix (bridge.ts scores stripped)
- Plugin event shape fix (toolName/params normalization)
- gateMode support wired into plugin config
- Governance daemon restarted and healthy
- X API cost analysis (proposals/x-cost-zero-strategy.md)
- Stream monitor circuit breaker (commit 95ce3ea)
- StewartBot 16 commits pushed
- Observatory dashboard running on :8501
- Mission Control governance-first rewrite
- RPM/QGM pipeline reactivated

## Blocked

- **X API:** Spend cap hit, resets April 9
- **Advisory agents:** Requires P1 completion + JB approval
- **MLX server:** Down -- delegating to Opus, logging reason
- **Enforce mode:** Observe active, calibration needed (web_fetch at 0.272)

## Standing Rules (JB Directive 2026-03-16)

- No sub-agent commissioning without JB approval
- No X API calls until April 9 + JB approval
- No trading development
- No governance threshold/boundary/PA modifications (T's domain)
- No pushes to repos other than governed-agent without JB approval
- RPM delegation on all analysis/design work -- no exceptions
- QGM gates on all sub-agent output -- no exceptions
- Sub-agents get problems + evidence + boundaries, NOT step-by-step instructions
