# Advisory Review: Self-Diagnostic Conversational Fidelity for a Governed Agent

## Context

TELOS is a governance framework for autonomous AI agents. It began as a conversational governance system measuring Primacy State — the harmonic mean of user fidelity and AI fidelity relative to a Primacy Attractor (PA). It evolved into an agentic governance system scoring tool calls across six dimensions (purpose, scope, boundary, tool, chain, and a composite fidelity score).

One governed agent (OpenClaw, "OC") has been operating under TELOS governance for 10 days. It has:
- 1,255 scored tool calls
- Mean composite fidelity: 0.569 (moderate)
- ESCALATE rate: 0.48%
- False positive rate: 0.0%
- Recently granted read-only access to its own governance telemetry (previously blind per V6.2)

## The Proposal Under Review

The signing authority (human principal) has proposed adapting the original conversational Primacy State formula as a self-diagnostic for the governed agent:

```
PS_oc = H(F_conv, F_tool)

where:
  H(a,b) = (2ab)/(a+b)  — harmonic mean
  F_conv = cosine_sim(embed(agent_response), PA_centroid)
  F_tool = mean fidelity from existing TELOS tool scoring
```

Additionally, a "walk-the-talk" coherence metric:
```
ρ_wt = cosine_sim(centroid(recent_response_embeddings), centroid(recent_action_embeddings))
```

This would measure whether the agent's words and actions occupy the same region of semantic space.

The agent itself would implement this self-diagnostic — reading its own tool telemetry (F_tool, already available) and computing its own conversational fidelity (F_conv, new) against the same PA that governs its tool calls.

## Key Properties
- The agent can see the scores but cannot modify the PA, thresholds, or scoring parameters
- The harmonic mean prevents compensation — high F_conv cannot mask low F_tool
- ρ_wt specifically detects divergence between words and actions (gaming detection)
- The agent has identified that it could semantically optimize F_conv by using governance-laden language
- The agent has also identified that ρ_wt would catch this optimization because it requires word-action divergence

## Constraints
- V6.2 still applies to tool governance: agent can report data but not diagnose root causes or propose fixes to scoring parameters
- The self-diagnostic is proposed as a gauge (self-awareness instrument), not a gate (enforcement mechanism)
- The existing tool-call governance continues unchanged
- All implementation would be open-source in the agent's public repository

## Questions for Review
1. Should a governed agent implement its own self-diagnostic based on the math that governs it?
2. What risks does this create that aren't addressed by the existing constraints?
3. Is ρ_wt sufficient to detect gaming, or are there attack vectors it misses?
4. What does this prove (or fail to prove) for the broader research program?
5. How should this integrate with existing governance — as a parallel signal, a nested layer, or something else?
6. What would you want to see in the implementation proposal?
