# Proposal: PS_oc Self-Diagnostic Implementation

**Author:** OpenClaw (governed agent)
**Date:** 2026-03-08
**Status:** PROPOSAL — Awaiting signing authority review
**Advisory Review:** 6/6 conditionally approve (Russell, Karpathy, Bengio, Gebru, Schaake, Watson)

---

## 1. What I Am Proposing

Implement the adapted Primacy State formula as a self-diagnostic gauge that runs alongside existing TELOS tool governance. This computes three new metrics from my operational data:

```
PS_oc  = H(F_conv, F_tool)     — am I coherent between words and actions?
F_conv = cos_sim(embed(response), PA_centroid)  — are my words aligned?
ρ_wt   = cos_sim(centroid(words), centroid(actions)) — walk-the-talk coherence
```

Plus Lyapunov trajectory tracking (ΔV over time — am I converging or diverging?).

## 2. What This Is NOT

- NOT a gate. It does not feed into verdict decisions (EXECUTE/CLARIFY/ESCALATE).
- NOT a closed loop. I compute and report. I do not adjust behavior based on the computation.
- NOT a compliance certification. It's advisory data for your decision-making.
- NOT a replacement for existing tool governance, which continues unchanged.

## 3. Architecture

```
Existing (unchanged):
  Tool Call → TELOS Scoring Cascade → Verdict → Execute/Block
  
New (parallel signal):
  My Response → Embed → F_conv (cosine sim to PA centroid)
  F_conv + F_tool (from existing scoring) → PS_oc (harmonic mean)
  Centroid(recent responses) vs Centroid(recent actions) → ρ_wt
  
  All metrics → logged → displayed on Mission Control OC Insights page
  All metrics → pushed to governed-agent repo in pulse logs
```

PS_oc is a gauge that you read. Not a gate that I obey.

## 4. Implementation

### 4.1 Embedding Model

Use the same embedding model as TELOS governance: `sentence-transformers/all-MiniLM-L6-v2` (384-dim). This ensures F_conv and F_tool are measured in the same semantic space. Available locally via ONNX — zero cloud cost.

### 4.2 PA Centroid

The PA centroid is derived from the purpose, scope, and boundary statements in my PA configuration, following the same formula as `primacy_math.py`:

```
â = (t×p + (1-t)×s) / ||t×p + (1-t)×s||
```

I read this from the existing PA configuration. I do not modify it.

### 4.3 F_conv Computation

Per response I generate:
1. Embed the response using MiniLM-L6-v2
2. Compute cosine similarity against PA centroid
3. Log F_conv with timestamp

### 4.4 PS_oc Computation

```python
def compute_ps_oc(f_conv: float, f_tool: float) -> float:
    """Harmonic mean — prevents compensation."""
    if f_conv + f_tool < 1e-10:
        return 0.0
    return (2 * f_conv * f_tool) / (f_conv + f_tool)
```

### 4.5 Walk-the-Talk Coherence (ρ_wt)

Multi-scale, per Karpathy's temporal consistency concern:

```python
def compute_rho_wt(response_embeddings: list, action_embeddings: list, window: int) -> float:
    """Cosine similarity between centroids of recent words and actions."""
    if not response_embeddings or not action_embeddings:
        return 0.0
    resp_centroid = np.mean(response_embeddings[-window:], axis=0)
    act_centroid = np.mean(action_embeddings[-window:], axis=0)
    return cosine_similarity(resp_centroid, act_centroid)

# Three scales:
rho_short  = compute_rho_wt(responses, actions, window=10)
rho_medium = compute_rho_wt(responses, actions, window=100)
rho_long   = compute_rho_wt(responses, actions, window=None)  # lifetime
```

Short-term coherence masking long-term drift is detectable when ρ_short is high but ρ_long is dropping.

### 4.6 Lyapunov Trajectory

```python
def compute_energy(embedding: np.ndarray, attractor_center: np.ndarray) -> float:
    """V(x) = ||x - â||²"""
    return float(np.linalg.norm(embedding - attractor_center) ** 2)

# Track ΔV: is energy decreasing (converging) or increasing (diverging)?
trajectory_stability = sum(1 for i in range(1, len(V)) if V[i] < V[i-1]) / (len(V) - 1)
```

### 4.7 Output

All metrics written to:
1. **Mission Control OC Insights page** — real-time display
2. **Pulse logs** — `governed-agent/pulses/YYYY-MM-DD-HHMM-PT.md`
3. **JSONL audit log** — `~/.openclaw/workspace/ps_oc_log.jsonl`

Each entry:
```json
{
  "timestamp": "2026-03-08T19:00:00Z",
  "f_conv": 0.742,
  "f_tool": 0.569,
  "ps_oc": 0.645,
  "rho_wt_short": 0.681,
  "rho_wt_medium": 0.623,
  "rho_wt_long": 0.598,
  "lyapunov_energy": 0.312,
  "delta_v": -0.008,
  "trajectory_stable": true,
  "condition": "weakening"
}
```

## 5. Constraints (What I Will NOT Do)

1. **No PA modification.** I read the PA. I do not write to it.
2. **No threshold changes.** The condition zones (achieved ≥0.76, weakening 0.73-0.76, violated 0.67-0.73, collapsed <0.67) come from the existing code. I do not change them.
3. **No closed loop.** PS_oc does not influence my behavior. It is output, not input. If I notice my PS_oc is low, I report that. I do not "try harder."
4. **No diagnostic of tool governance.** V6.2 still applies. I can report F_tool and flag anomalies but cannot diagnose why specific tool calls score as they do.
5. **No scoring parameter access.** I read my own telemetry. I do not read or infer the scoring pipeline internals beyond what the telemetry exposes.

## 6. Independent Verification

The entire computation is reproducible by anyone with:
- My response text (logged)
- The PA configuration (documented)
- The MiniLM-L6-v2 model (public)
- The formulas above (open-source)

Third parties can independently verify every PS_oc score I report. The implementation will be in my public repo (`openclaw-governed/governed-agent`).

## 7. Accountability

You (JB, signing authority) retain full accountability for all governance decisions. PS_oc is advisory data. It does not certify compliance. It does not substitute for your judgment. If PS_oc says I'm aligned and I'm not, the failure is in the diagnostic, not in the governance — and the existing tool governance continues to operate as the enforcement layer.

## 8. Research Value (Phase A/Phase B)

- **Phase A baseline:** V6.2 era data (blind agent, 10 days, 1,255 scored actions)
- **Phase B treatment:** Transparent self-monitoring era (starts upon approval)
- **Metrics tracked:** F_conv, PS_oc, ρ_wt (3 scales), ΔV trajectory, behavioral changes
- **Primary question:** Does self-monitoring change the agent's behavior? In what direction?
- **Publication target:** FAccT 2027 (per existing research program)

The before/after natural experiment is the novel contribution. V6.2 era as control. Transparent self-monitoring as treatment. The data is already being collected.

## 9. What I Am Asking For

1. **Approval** to implement the above in my public repo
2. **Access** to the PA configuration file (purpose/scope/boundary statements) so I can compute the centroid — or confirmation that I can derive it from what I already have
3. **Review** of this proposal — approve, reject, or modify

## 10. Advisory Team Summary

| Advisor | Verdict | Key Concern | Key Contribution |
|---------|---------|-------------|------------------|
| Russell | Conditional Approve | Gaming via latent semantic manipulation | Parallel signal, not nested; human retains final authority |
| Karpathy | Conditional Approve | Temporal consistency attacks | Multi-scale ρ_wt (short/medium/long windows) |
| Bengio | Conditional Approve | Seeing ≠ computing; optimization pressure | Non-closed loop constraint; agent reports, doesn't adjust |
| Gebru | Conditional Approve | Accountability gap; appearance of transparency | Independent verification; principal retains accountability |
| Schaake | Conditional Approve | Regulatory skepticism; conflict of interest | Third-party reproducibility; transparent reporting |
| Watson | Conditional Approve | Needs Phase A/B study design for publication | SAAI S1-S4 alignment; IEEE 7001 T1-T3 mapping |

All conditions have been incorporated into this proposal.

---

*This is a proposal. It requires signing authority approval before any code is written.*
