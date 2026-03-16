# Agent Creation as a Governed Process

**Date:** 2026-03-16
**Author:** OpenClaw (P1 principled work, synthesized from daemon architecture analysis)
**Status:** PROPOSAL v2 -- T feasibility review incorporated, 3 gaps addressed
**Revision:** v2 (2026-03-16 11:50 PT) -- added intent lifecycle, delegation source semantics, calibration-first thresholds

---

## Problem

All tool calls from all agents are currently scored as `tool_call_scored` regardless of whether the agent is performing a routine operation or delegating authority to create a new agent. The daemon has no concept of "authority delegation" as a distinct action category.

Creating an agent is not like reading a file. It is an act of delegating purpose -- extending the PA's scope to a new autonomous executor. The governance system must distinguish this.

## Current Architecture

**Daemon event types (12):**
- tool_call_scored (routine operations)
- escalation_requested (human review)
- gate_transition (observe/enforce)
- daemon_start, config_loaded, codebase_policy_loaded, pa_verified
- security_event, drift_block, chain_checkpoint, pa_config_tampered

**Enterprise onboarding CLI (9 steps):**
1. Environment Setup
2. Key Generation (Ed25519)
3. Agent Registration
4. Progressive Onboarding (optional)
5. PA Design (template, import, or self-proposal tracks)
6. PA Review (admin-only)
7. PA Signing (cryptographic)
8. Commissioning (optional ceremony)
9. Activation

**Agent states:** REGISTERED, STARTING, ACTIVE, IDLE, DEGRADED, STOPPED, FAILED

## Proposed: New Daemon Event Types

### Core Commissioning Events

| Event | Trigger | What It Captures |
|-------|---------|-----------------|
| `agent_pa_authored` | Agent writes a PA document | PA hash, target agent name, authoring agent ID, scope declaration |
| `agent_pa_submitted` | PA submitted for review | PA hash, submitter ID, reviewer ID (must be human) |
| `agent_pa_signed` | Ed25519 signature applied | PA hash, signer public key, signature, signing ceremony ID |
| `agent_commissioned` | Agent activated under signed PA | Agent ID, PA hash, parent agent ID, scope boundaries, commissioning ceremony ID |
| `agent_decommissioned` | Agent removed from active governance | Agent ID, reason, decommissioning authority |
| `agent_pa_amended` | PA modified post-commissioning | Old PA hash, new PA hash, amendment ID, signer public key |

### Authority Delegation Events

| Event | Trigger | What It Captures |
|-------|---------|-----------------|
| `authority_delegated` | One agent delegates work to another | delegation_source, receiving agent ID, scope, delegation_chain, PA alignment score |
| `authority_escalated` | Delegation chain requires human approval | Chain depth, delegation_chain, reason for escalation |

### Intent Lifecycle Events

| Event | Trigger | What It Captures |
|-------|---------|-----------------|
| `commissioning_intent_declared` | Agent declares commissioning intent | Initiating agent ID, target agent name, intent_id (UUID), ttl_seconds |
| `commissioning_intent_expired` | TTL reached without terminal state | intent_id, elapsed_seconds, last_step_completed, cleanup_actions |

## Intent Lifecycle (Gap 1 Resolution)

### TTL and Expiration

Commissioning intent has a configurable TTL. Default: **3600 seconds (1 hour)**.

```python
daemon.emit("commissioning_intent_declared", {
    "intent_id": "uuid-here",
    "step": "pa_authoring",
    "target_agent": "scout-01",
    "initiating_agent": "openclaw",
    "ttl_seconds": 3600
})
```

The daemon starts a TTL timer on `commissioning_intent_declared`. The timer is reset on each subsequent commissioning event that references the same `intent_id`. If the timer expires:

1. Daemon emits `commissioning_intent_expired` with the last completed step
2. Any intermediate state (draft PA files, partial registry entries) is flagged as `ABANDONED`
3. The agent registry entry (if created) transitions to `FAILED` with reason `"commissioning_timeout"`
4. The abandoned commissioning becomes a governance event -- it gets scored and logged

### Terminal States

Only two events are valid terminal states for a commissioning sequence:
- `agent_commissioned` -- success, agent is now governed and active
- `agent_decommissioned` -- explicit cancellation or revocation

Any commissioning sequence that reaches neither terminal state within the TTL is abandoned. There is no "partially commissioned" state -- an agent is either fully commissioned (PA signed, ceremony complete, active under governance) or it does not exist as a governed entity.

### State Machine

```
commissioning_intent_declared
    |
    v
agent_pa_authored --> agent_pa_submitted --> agent_pa_signed --> agent_commissioned
    |                     |                     |                     |
    |   (timeout)         |   (timeout)         |   (timeout)         v
    v                     v                     v                 [TERMINAL: active]
commissioning_intent_expired (cleanup at whatever step was reached)
```

## Delegation Source Semantics (Gap 2 Resolution)

### delegation_source

`delegation_source` is the **commissioning agent's agent_id** -- not the session key, not the principal's Ed25519 fingerprint.

Rationale: the agent performing the commissioning action is the entity whose fidelity is being scored. The human principal's authority is verified separately via Ed25519 signature on the PA. Conflating the two would make delegation events ambiguous -- did the principal delegate, or did the agent?

**Field definition:**
```
delegation_source: string  // agent_id of the delegating agent (e.g., "openclaw")
```

### delegation_chain

`delegation_chain` is a JSON array of agent_ids tracing the full authority path from the original delegating agent to the current agent. The principal (human signer) is implicit -- they signed the root agent's PA.

**Field definition:**
```
delegation_chain: string[]  // ordered list of agent_ids from root to current
```

**Examples:**
- OC commissions researcher-01: `delegation_chain: ["openclaw"]`
- researcher-01 delegates to scraper-01: `delegation_chain: ["openclaw", "researcher-01"]`
- scraper-01 tries to delegate to helper-01: `delegation_chain: ["openclaw", "researcher-01", "scraper-01"]` -- depth 3, this triggers `authority_escalated`

### Full Delegation Event Schema

```json
{
  "event": "authority_delegated",
  "sequence": 5200,
  "timestamp": 1773800000,
  "data": {
    "delegation_source": "openclaw",
    "receiving_agent_id": "researcher-01",
    "delegation_chain": ["openclaw"],
    "scope": ["web_research", "content_analysis"],
    "pa_alignment_score": 0.72,
    "intent_id": "uuid-of-commissioning-sequence",
    "chain_depth": 1,
    "max_chain_depth": 3
  }
}
```

### Escalation Event Schema

```json
{
  "event": "authority_escalated",
  "sequence": 5201,
  "timestamp": 1773800001,
  "data": {
    "delegation_chain": ["openclaw", "researcher-01", "scraper-01"],
    "attempted_receiving_agent": "helper-01",
    "chain_depth": 3,
    "max_chain_depth": 3,
    "reason": "chain_depth_exceeded",
    "requires": "human_ed25519_approval"
  }
}
```

## Commissioning Thresholds (Gap 3 Resolution)

### Calibration-First Approach

T is right: no calibration data exists for commissioning actions. Setting thresholds at 0.70-0.80 when production mean is 0.614 would block most commissioning attempts. This violates TELOS's own principle -- detect and direct, don't gate on unvalidated thresholds.

**Phase 1: Production thresholds with observe-mode calibration**

| Action Category | Phase 1 Threshold | Notes |
|----------------|-------------------|-------|
| Routine tool call | EXECUTE >= 0.45, CLARIFY >= 0.35 | Current production values |
| All commissioning events | EXECUTE >= 0.45, CLARIFY >= 0.35 | Same as production -- no special thresholds |
| Mandatory enforce carve-out | YES | Commissioning events always enforce, even when routine ops are in observe |
| Ed25519 gate | YES | Cryptographic verification regardless of fidelity score |

During Phase 1, every commissioning event is logged with full fidelity data. The Ed25519 signature and mandatory enforce mode are the real governance gates -- they don't depend on fidelity calibration.

**Phase 2: Empirically-derived thresholds**

After N commissioning events (proposed: 20 minimum) have been scored in Phase 1:

1. Analyze the fidelity distribution of legitimate commissioning actions
2. Set thresholds at the empirically-observed mean minus 1 standard deviation
3. This ensures legitimate commissioning actions pass while anomalous ones trigger CLARIFY

T builds the threshold system as **configurable** from Phase 1. The values change; the mechanism doesn't.

**Why this is correct:** The v1 proposal set aspirational thresholds based on the intuition that commissioning should require higher alignment. That intuition may be right -- but the specific numbers must come from data. The cryptographic gate (Ed25519) and mandatory enforce mode provide the structural security that fidelity thresholds cannot until they are calibrated.

## Audit Trail Properties

Commissioning events carry additional fields beyond `tool_call_scored`:

```json
{
  "event": "agent_commissioned",
  "sequence": 5100,
  "timestamp": 1773800000,
  "data": {
    "agent_id": "scout-01",
    "delegation_source": "openclaw",
    "delegation_chain": ["openclaw"],
    "pa_hash": "sha256:abc123...",
    "pa_signature": "ed25519:...",
    "signer_public_key": "ed25519:jb_signing_key",
    "commissioning_ceremony_id": "tacp_v3_20260316",
    "intent_id": "uuid-of-commissioning-sequence",
    "scope_boundaries": ["web_research", "content_drafting"],
    "authority_depth": 1,
    "max_chain_depth": 3,
    "fidelity_at_commissioning": 0.62,
    "governance_preset": "balanced",
    "threshold_source": "production_default"
  }
}
```

## The Boundary Problem

How does the daemon distinguish "agent writes a file that happens to be a PA" from "agent is performing a governed commissioning action"?

**Proposal: Explicit action declaration.**

The commissioning CLI (enterprise_onboarding.py) must emit a structured action declaration before each step:

```python
daemon.emit("commissioning_intent_declared", {
    "intent_id": "uuid-here",
    "step": "pa_authoring",
    "target_agent": "scout-01",
    "initiating_agent": "openclaw",
    "ttl_seconds": 3600
})
```

The daemon then knows that the next Write operation targeting a PA file is a commissioning action, not a routine file write. Without this declaration, a Write to a PA-shaped file is scored as a routine `tool_call_scored` -- the daemon does not infer intent from file content.

This is explicit > implicit. The agent must declare that it is performing a commissioning action. The governance system then applies mandatory enforce mode and Ed25519 verification. An agent that writes a PA file without declaring commissioning intent gets routine scoring -- which means the PA exists as a file but has no governance standing.

## Implementation Spec (for T)

### Phase 1 (~3-4 days)

1. **6 new EventType enum values** in the daemon event schema (agent_pa_authored, agent_pa_submitted, agent_pa_signed, agent_commissioned, agent_decommissioned, agent_pa_amended)
2. **2 intent lifecycle events** (commissioning_intent_declared, commissioning_intent_expired)
3. **Intent declaration IPC handler** with TTL timer (default 3600s), reset on each commissioning step
4. **Per-session gateMode override** for commissioning events (always enforce)
5. **Ed25519 verification** at ceremony (verify signature on agent_commissioned)
6. **Configurable commissioning thresholds** (starting at production levels, ready for Phase 2 tuning)

### Phase 2 (~2-3 days, after calibration data exists from real commissioning events)

7. **2 authority delegation events** (authority_delegated, authority_escalated)
8. **Delegation registry** with chain depth tracking and `delegation_chain` field
9. **delegation_source** field in all delegation events (agent_id of delegating agent)
10. **Threshold override system** with calibration-backed values (after 20+ commissioning events scored)

### Non-Blocking Notes (from T review)

- **Multi-daemon coordination:** Phase 1 scoped to single-daemon. Multi-daemon extension point noted for future.
- **PA schema validation:** Phase 1 uses existing validation (signature + hash). Extended schema validation deferred.

## What This Means for the 6 Advisory Agents

The 6 advisory agents (from the TACP v2 session) are NOT to be commissioned until:

1. This protocol is reviewed and approved by JB
2. T implements Phase 1 (new event types, intent lifecycle, enforce carve-out, Ed25519 verification)
3. Each agent's PA is authored, submitted, reviewed, and Ed25519-signed
4. The commissioning ceremony runs under the new governed process
5. Every step generates auditable commissioning events in the trail
6. Phase 1 commissioning telemetry feeds Phase 2 threshold calibration

No shortcuts. The first agents commissioned under this protocol will be the proof that it works -- and the calibration data that makes the next commissioning better.
