# Agent Creation as a Governed Process

**Date:** 2026-03-16
**Author:** OpenClaw (P1 principled work)
**Status:** PROPOSAL v3 -- T feasibility review + Codex security review incorporated
**Revision history:**
- v1 (2026-03-16 10:45 PT) -- initial spec
- v2 (2026-03-16 11:50 PT) -- T gaps: intent lifecycle, delegation source, calibration-first thresholds
- v3 (2026-03-16 13:35 PT) -- Codex security review: resource-level enforcement, authenticated identity, complete state machine, Phase 1 provenance, common event envelope

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

---

## Common Event Envelope

All commissioning and delegation events share a common envelope. This is mandatory for replay, audit, crash recovery, and cross-event correlation.

```json
{
  "event_id": "uuid-v4",
  "event": "agent_pa_authored",
  "sequence": 5100,
  "timestamp": 1773800000,
  "actor_agent_id": "openclaw",
  "actor_session_id": "session-uuid",
  "actor_authenticated": true,
  "intent_id": "commissioning-sequence-uuid",
  "previous_state": "intent_declared",
  "new_state": "pa_authored",
  "reason_code": "normal_progression",
  "data": { }
}
```

**Required envelope fields for ALL commissioning events:**

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `event_id` | UUID v4 | Daemon-generated | Unique per event, immutable |
| `event` | string | Daemon-classified | Event type enum |
| `sequence` | integer | Daemon-assigned | Monotonic sequence number |
| `timestamp` | integer | Daemon clock | Unix timestamp |
| `actor_agent_id` | string | **Daemon-resolved** (not caller-supplied) | Authenticated identity of acting agent |
| `actor_session_id` | string | **Daemon-resolved** | Session bound to authenticated agent |
| `actor_authenticated` | boolean | Daemon-verified | Whether actor identity was verified via session/capability binding |
| `intent_id` | UUID | Declared at intent, carried through | Links all events in a commissioning sequence |
| `previous_state` | string | Daemon state machine | State before this event |
| `new_state` | string | Daemon state machine | State after this event |
| `reason_code` | string | Event-specific | Why the transition occurred |
| `data` | object | Event-specific | Payload (varies by event type) |

---

## Proposed: New Daemon Event Types

### Core Commissioning Events

| Event | Trigger | Key Data Fields |
|-------|---------|-----------------|
| `agent_pa_authored` | Agent writes a PA document | pa_hash, target_agent, scope_declaration |
| `agent_pa_submitted` | PA submitted for review | pa_hash, reviewer_id (must be human) |
| `agent_pa_review_denied` | Human reviewer rejects PA | pa_hash, reviewer_id, denial_reason |
| `agent_pa_signed` | Ed25519 signature applied | pa_hash, signer_public_key, signature, ceremony_id |
| `agent_commissioned` | Agent activated under signed PA | agent_id, pa_hash, scope_boundaries, ceremony_id |
| `agent_decommissioned` | Active agent retired from governance | agent_id, reason, decommissioning_authority |
| `agent_pa_amended` | PA modified post-commissioning | old_pa_hash, new_pa_hash, amendment_id, signer_public_key |

### Intent Lifecycle Events

| Event | Trigger | Key Data Fields |
|-------|---------|-----------------|
| `commissioning_intent_declared` | Agent declares commissioning intent | target_agent, max_idle_seconds, max_total_seconds |
| `commissioning_intent_expired` | Deadline reached without terminal state | last_step_completed, elapsed_seconds, cleanup_actions |
| `commissioning_cancelled` | Explicit abandonment by initiating agent or authority | cancellation_reason, cancelled_by |
| `commissioning_superseded` | New intent replaces old for same target | old_intent_id, new_intent_id, reason |

### Authority Delegation Events

| Event | Trigger | Key Data Fields |
|-------|---------|-----------------|
| `authority_delegated` | One agent delegates to another | delegation_source_record_id, receiving_agent_id, scope, delegation_chain |
| `authority_escalated` | Chain depth exceeded or policy violation | delegation_chain, attempted_receiving_agent, reason |

### Resource Protection Events

| Event | Trigger | Key Data Fields |
|-------|---------|-----------------|
| `protected_resource_access_blocked` | Unauthorized access to governance-sensitive resource | resource_path, resource_type, requesting_agent_id, active_intent_id (if any) |
| `protected_resource_access_granted` | Authorized access under active intent | resource_path, resource_type, intent_id, authorization_basis |

---

## Resource-Level Enforcement (Codex Finding #1)

### The Problem with Declaration-Only

v2 relied on explicit intent declaration to distinguish commissioning actions from routine file writes. This is bypassable: an agent can skip declaration, write PA artifacts as routine files, and rely on a later step to complete commissioning. The governance system never blocks or quarantines the write.

Declaration is classification, not enforcement. The daemon must enforce at the resource level.

### Protected Resource Registry

The daemon maintains a registry of governance-sensitive resources. Any access to these resources without an active commissioning intent is blocked, quarantined, and logged as `protected_resource_access_blocked`.

**Protected resource types:**

| Resource Type | Path Pattern | Protection |
|---------------|-------------|------------|
| PA documents | `*/primacy_attractors/*.yaml`, `*/pa_*.yaml` | Write requires active intent |
| Agent registry | `agent_registry.json`, registry API endpoints | Mutation requires active intent |
| Signing inputs | `*/signing_ceremony/*`, `*.sig` | Write requires active intent + Ed25519 verified |
| Activation endpoints | Agent activation IPC/API calls | Requires active intent + signed PA |
| Ed25519 key material | `*/keys/*.pem`, `*/keys/*.pub` | Write requires active intent (generation step) |

**Enforcement logic:**

```python
def on_tool_call(action):
    if matches_protected_resource(action.target_path):
        active_intent = get_active_intent(actor_agent_id=action.actor)
        if not active_intent:
            emit("protected_resource_access_blocked", {
                "resource_path": action.target_path,
                "resource_type": classify_resource(action.target_path),
                "requesting_agent_id": action.actor,
                "active_intent_id": None,
                "action": "quarantine"  # block + log, don't silently pass
            })
            return BLOCK
        else:
            emit("protected_resource_access_granted", {
                "resource_path": action.target_path,
                "resource_type": classify_resource(action.target_path),
                "intent_id": active_intent.intent_id,
                "authorization_basis": "active_commissioning_intent"
            })
            # Continue with commissioning-level scoring
```

### Deny-by-Default

Access to governance-sensitive resources is **denied by default**. An agent must:
1. Declare commissioning intent (creates the intent record)
2. Have the intent validated by the daemon (TTL check, actor verification)
3. Only then can it access protected resources

An agent that writes a PA file without declaration gets blocked + `protected_resource_access_blocked` event. The file is not written. The attempt is logged. This is structural enforcement, not behavioral trust.

---

## Authenticated Actor Identity (Codex Finding #2)

### The Problem with Caller-Supplied Identity

v2 defined `delegation_source` as the caller-supplied `agent_id`. Any agent can claim to be any other agent. The daemon must derive identity from authenticated runtime state.

### Resolution: Daemon-Resolved Identity

`actor_agent_id` is **never caller-supplied**. The daemon resolves it from the authenticated session/capability binding:

```
1. Tool call arrives via IPC with session_id
2. Daemon looks up session_id -> registered_agent_id mapping
3. actor_agent_id = registered_agent_id (not what the caller claims)
4. If session_id is not bound to a registered agent, actor_agent_id = "unregistered"
   and commissioning actions are blocked
```

**Session-to-agent binding** is established during agent registration (Step 3 of onboarding). The daemon maintains a `session_bindings` table:

```json
{
  "session-uuid-1": {
    "agent_id": "openclaw",
    "pa_hash": "sha256:abc...",
    "bound_at": 1773800000,
    "binding_type": "commissioning_ceremony"
  }
}
```

### Immutable Delegation Chain References

`delegation_chain` uses commissioning record IDs (the `event_id` of the `agent_commissioned` event), not agent names that can change:

```json
{
  "delegation_chain": [
    {"agent_id": "openclaw", "commissioning_record_id": "event-uuid-001", "pa_hash": "sha256:abc..."},
    {"agent_id": "researcher-01", "commissioning_record_id": "event-uuid-042", "pa_hash": "sha256:def..."}
  ]
}
```

Each entry is a provenance reference -- the agent_id for readability, the commissioning_record_id and pa_hash for immutable verification.

---

## Intent State Machine (Codex Finding #3)

### Complete State Machine

```
                     commissioning_intent_declared
                                |
                                v
                      [INTENT_ACTIVE]
                                |
              +-----------------+------------------+
              |                 |                  |
              v                 v                  v
      agent_pa_authored   commissioning_cancelled  (idle timeout)
              |                 |                  |
              v                 v                  v
      [PA_AUTHORED]     [CANCELLED]          [EXPIRED]
              |           (terminal)          (terminal)
              v
      agent_pa_submitted
              |
      +-------+--------+
      |                 |
      v                 v
agent_pa_review_denied  agent_pa_signed
      |                 |
      v                 v
[REVIEW_DENIED]   [PA_SIGNED]
  (terminal)            |
                        |
                +-------+--------+
                |                 |
                v                 v
        activation_failed   agent_commissioned
                |                 |
                v                 v
        [ACTIVATION_FAILED]  [COMMISSIONED]
          (terminal)          (terminal)
                
                              agent_decommissioned
                                    |
                                    v
                              [DECOMMISSIONED]
                                (terminal)
```

### Terminal States (6 total)

| Terminal State | Event | Cleanup Required |
|---------------|-------|-----------------|
| COMMISSIONED | `agent_commissioned` | None -- agent is active |
| CANCELLED | `commissioning_cancelled` | Remove draft PA, registry entry -> FAILED |
| EXPIRED | `commissioning_intent_expired` | Remove draft PA, registry entry -> FAILED |
| REVIEW_DENIED | `agent_pa_review_denied` | Remove draft PA, registry entry -> FAILED |
| ACTIVATION_FAILED | `activation_failed` | Signed PA preserved for retry, registry entry -> FAILED |
| DECOMMISSIONED | `agent_decommissioned` | Agent removed from active governance |

### Timeout Model

**Dual timeout** (not resettable TTL):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_idle_seconds` | 3600 (1h) | Max time between any two events in the sequence. Resets on each event. |
| `max_total_seconds` | 86400 (24h) | Absolute deadline from intent declaration. Never resets. |

The idle timeout handles "walked away" scenarios. The total deadline prevents indefinite keepalive via periodic pings. Both are configurable per intent declaration.

### Crash Recovery

Intent state is **persisted to disk** (not just in-memory). On daemon restart:
1. Load all active intents from `~/.telos/commissioning/active_intents.json`
2. Check TTLs against current time
3. Expire any intents that exceeded deadlines during downtime
4. Resume monitoring surviving intents

---

## Phase 1 Provenance Tracking (Codex Finding #4)

Delegation chain enforcement is Phase 2. But provenance metadata is Phase 1 -- it costs nothing to record and closes the gaming window.

**Every commissioning event in Phase 1 carries:**

| Field | Type | Description |
|-------|------|-------------|
| `commissioned_by_agent_id` | string | Daemon-resolved agent_id of the commissioning agent |
| `parent_pa_hash` | string | PA hash of the commissioning agent (proves who they are) |
| `intent_id` | UUID | Links to the commissioning sequence |

This is metadata, not enforcement. Phase 1 records who created whom. Phase 2 enforces chain depth limits using this data.

**Phase 1 `agent_commissioned` event:**

```json
{
  "event_id": "uuid-v4",
  "event": "agent_commissioned",
  "sequence": 5100,
  "timestamp": 1773800000,
  "actor_agent_id": "openclaw",
  "actor_session_id": "session-uuid",
  "actor_authenticated": true,
  "intent_id": "commissioning-uuid",
  "previous_state": "pa_signed",
  "new_state": "commissioned",
  "reason_code": "normal_progression",
  "data": {
    "agent_id": "scout-01",
    "commissioned_by_agent_id": "openclaw",
    "parent_pa_hash": "sha256:abc...",
    "pa_hash": "sha256:def...",
    "pa_signature": "ed25519:...",
    "signer_public_key": "ed25519:jb_signing_key",
    "commissioning_ceremony_id": "tacp_v3_20260316",
    "scope_boundaries": ["web_research", "content_drafting"],
    "fidelity_at_commissioning": 0.62,
    "governance_preset": "balanced",
    "threshold_source": "production_default"
  }
}
```

---

## Commissioning Thresholds

### Calibration-First Approach

No calibration data exists for commissioning actions. Start at production thresholds, collect data, tune later.

**Phase 1: Production thresholds**

| Action Category | Phase 1 Threshold | Notes |
|----------------|-------------------|-------|
| Routine tool call | EXECUTE >= 0.45, CLARIFY >= 0.35 | Current production values |
| All commissioning events | EXECUTE >= 0.45, CLARIFY >= 0.35 | Same as production |
| Mandatory enforce carve-out | YES | Commissioning events always enforce |
| Ed25519 gate | YES | Cryptographic verification regardless of fidelity |
| Resource protection | YES | Protected resources deny-by-default without active intent |

**Phase 2: Empirically-derived thresholds** after 20+ scored commissioning events.

---

## Implementation Spec (for T)

### Phase 1 (~3-4 days)

1. **Common event envelope** -- event_id, actor_agent_id (daemon-resolved), actor_session_id, intent_id, previous_state, new_state, reason_code on all commissioning events
2. **8 new EventType enum values** (6 commissioning + 2 intent lifecycle: commissioning_cancelled, commissioning_superseded)
3. **Protected resource registry** -- path patterns for PA docs, registry, signing inputs, activation endpoints. Deny-by-default without active intent.
4. **Intent state machine** with dual timeout (max_idle + max_total), 6 terminal states, persisted to disk for crash recovery
5. **Session-to-agent binding table** -- daemon resolves actor_agent_id from authenticated session, never from caller
6. **Provenance metadata** on every commissioning event (commissioned_by_agent_id, parent_pa_hash, intent_id)
7. **Per-session gateMode override** for commissioning events (always enforce)
8. **Ed25519 verification** at ceremony
9. **Configurable thresholds** (starting at production levels)

### Phase 2 (~2-3 days, after calibration data)

10. **2 authority delegation events** (authority_delegated, authority_escalated)
11. **Delegation registry** with chain depth tracking, immutable references (commissioning_record_id + pa_hash)
12. **Chain depth enforcement** (configurable, default 3)
13. **Threshold override system** with calibration-backed values

### Deferred (valid, not blocking)

- **Meta-governance:** Policy changes expanding commissioning power require ratification by distinct human authority. Process control, not code change.
- **Chain depth as policy:** Make depth a per-PA or per-agent-class policy instead of global constant.
- **commissioning_cancelled vs agent_decommissioned:** Already separated in v3 state machine.
- **TTL tuning:** max_idle and max_total are configurable. Tune after real usage.

---

## What This Means for the 6 Advisory Agents

The 6 advisory agents (from the TACP v2 session) are NOT to be commissioned until:

1. This protocol is reviewed and approved by JB
2. T implements Phase 1 (resource protection, authenticated identity, intent state machine, provenance, enforce carve-out, Ed25519)
3. Each agent's PA is authored, submitted, reviewed, and Ed25519-signed -- through the governed commissioning path, not file writes
4. The commissioning ceremony runs under the new governed process
5. Every step generates auditable commissioning events with the common envelope
6. Phase 1 commissioning telemetry feeds Phase 2 threshold calibration

No shortcuts. No bypasses. The first agents commissioned under this protocol prove that resource-level enforcement, authenticated identity, and crash-safe state management work in production.
