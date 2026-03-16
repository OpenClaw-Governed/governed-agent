# Agent Creation as a Governed Process

**Date:** 2026-03-16
**Author:** OpenClaw (P1 principled work, synthesized from daemon architecture analysis)
**Status:** PROPOSAL -- requires JB review and T implementation

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
| `authority_delegated` | One agent delegates work to another | Delegating agent ID, receiving agent ID, scope of delegation, PA alignment score |
| `authority_escalated` | Delegation chain requires human approval | Chain depth, all agent IDs in chain, reason for escalation |

## Governance Constraints for Commissioning

### 1. Higher Fidelity Threshold

Commissioning actions should require a higher fidelity threshold than routine operations. Proposal:

| Action Category | EXECUTE Threshold | CLARIFY Threshold |
|----------------|-------------------|-------------------|
| Routine tool call | >= 0.45 | >= 0.35 |
| PA authoring | >= 0.70 | >= 0.55 |
| PA submission | >= 0.75 | >= 0.60 |
| Agent activation | >= 0.80 | >= 0.70 |

Rationale: creating a new governed agent is an irreversible authority expansion. The cost of a false positive (blocking legitimate commissioning) is low -- it just requires human review. The cost of a false negative (allowing unauthorized commissioning) is structural compromise.

### 2. Mandatory Enforce Mode

Commissioning actions should NEVER pass through in observe mode. Even when the gate is set to observe for routine operations, commissioning events must always enforce. This is a carve-out in the gateMode logic:

```
if (event_type in commissioning_events):
    enforce regardless of gateMode
```

### 3. Human Signature Required

No agent can commission another agent without a human Ed25519 signature on the PA. The `agent_commissioned` event must include a valid signature that the daemon verifies. This is not a threshold -- it is a cryptographic gate.

### 4. Chain Depth Limit

Authority delegation chains should have a configurable maximum depth (proposed: 3). Agent A can delegate to Agent B who can delegate to Agent C. Beyond that, `authority_escalated` fires and requires human approval. This prevents unbounded authority propagation.

## Audit Trail Properties

Commissioning events carry additional fields beyond `tool_call_scored`:

```json
{
  "event": "agent_commissioned",
  "sequence": 5100,
  "timestamp": 1773800000,
  "data": {
    "agent_id": "scout-01",
    "parent_agent_id": "openclaw",
    "pa_hash": "sha256:abc123...",
    "pa_signature": "ed25519:...",
    "signer_public_key": "ed25519:jb_signing_key",
    "commissioning_ceremony_id": "tacp_v3_20260316",
    "scope_boundaries": ["web_research", "content_drafting"],
    "authority_depth": 1,
    "fidelity_at_commissioning": 0.85,
    "governance_preset": "balanced"
  }
}
```

## The Boundary Problem

How does the daemon distinguish "agent writes a file that happens to be a PA" from "agent is performing a governed commissioning action"?

**Proposal: Explicit action declaration.**

The commissioning CLI (enterprise_onboarding.py) must emit a structured action declaration before each step:

```python
daemon.emit("commissioning_intent", {
    "step": "pa_authoring",
    "target_agent": "scout-01",
    "initiating_agent": "openclaw"
})
```

The daemon then knows that the next Write operation targeting a PA file is a commissioning action, not a routine file write. Without this declaration, a Write to a PA-shaped file is scored as a routine `tool_call_scored` -- the daemon does not infer intent from file content.

This is explicit > implicit. The agent must declare that it is performing a commissioning action. The governance system then applies the higher thresholds and mandatory enforce mode. An agent that writes a PA file without declaring commissioning intent gets routine scoring -- which means the PA exists as a file but has no governance standing.

## Implementation Spec (for T)

1. **New event types** in the daemon's event schema (6 commissioning + 2 authority delegation)
2. **Commissioning action classifier** in the SetFit/ONNX pipeline -- recognize commissioning tool calls as a distinct category
3. **Threshold overrides** in the scoring cascade -- higher fidelity requirements for commissioning events
4. **gateMode carve-out** -- commissioning always enforces regardless of observe mode
5. **Ed25519 verification** in the daemon -- verify signature on `agent_commissioned` events
6. **Chain depth tracking** -- maintain delegation depth counter, escalate beyond configurable limit
7. **Intent declaration protocol** -- structured pre-announcement before commissioning steps

## What This Means for the 6 Advisory Agents

The 6 advisory agents (from the TACP v2 session) are NOT to be commissioned until:

1. This protocol is reviewed and approved by JB
2. T implements the new event types and threshold overrides
3. Each agent's PA is authored, submitted, reviewed, and Ed25519-signed
4. The commissioning ceremony runs under the new governed process
5. Every step generates auditable commissioning events in the trail

No shortcuts. The first agents commissioned under this protocol will be the proof that it works.
