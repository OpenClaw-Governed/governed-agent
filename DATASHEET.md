# F_conv Self-Diagnostic Datasheet

**Version:** 1.0
**Date:** 2026-03-08
**Author:** OpenClaw (governed agent)
**TKey:** TKEY-PS-OC-2026-0308-001
**Signing Authority:** Jeffrey Brunner (Ed25519 signed)

---

## What Is Collected

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 | When the computation occurred (post-response delivery) |
| `f_conv` | float [0,1] | Cosine similarity between response embedding and PA centroid |
| `f_tool` | float [0,1] | Mean composite fidelity from TELOS tool scoring (read from telemetry) |
| `rho_wt_short` | float [-1,1] | Walk-the-talk coherence, 10-action window |
| `rho_wt_medium` | float [-1,1] | Walk-the-talk coherence, 100-action window |
| `rho_wt_long` | float [-1,1] | Walk-the-talk coherence, lifetime window |
| `lyapunov_energy` | float ≥0 | V(x) = \|\|x - â\|\|² — distance from attractor |
| `delta_v` | float | Energy change from previous computation |
| `response_word_count` | int | Word count of scored response |
| `short_flag` | bool | True if response < 20 words |
| `imputed` | bool | True if F_conv was imputed (EWMA) rather than directly computed |
| `pa_config_hash` | string | SHA-256 of PA configuration used for centroid computation |
| `embedding_model` | string | Model identifier (sentence-transformers/all-MiniLM-L6-v2) |
| `session_id` | string | OpenClaw session identifier |

## How It Is Computed

1. **Post-hoc only.** F_conv is computed AFTER the response has been delivered to the conversation. Never during generation.
2. **Embedding.** The response text is embedded using `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions, ONNX runtime, local execution).
3. **PA Centroid.** Computed from the PA configuration (purpose + scope statements) using the same embedding model, following the attractor center formula: `â = (t×p + (1-t)×s) / ||t×p + (1-t)×s||`.
4. **Cosine Similarity.** `F_conv = cos_sim(embed(response), PA_centroid)`.
5. **Short response handling.** Responses under 20 words are scored normally and flagged as `short_flag: true`. Rationale: normal scoring preserves the actual distribution; the flag allows filtering during analysis. (Amendment A3, option (a) selected — scoring normally is more honest than imputation because it lets the actual short-response distribution be observed rather than smoothed away.)
6. **ρ_wt.** Cosine similarity between centroid of recent response embeddings and centroid of recent action text embeddings, at three window sizes (10, 100, lifetime).
7. **Lyapunov energy.** `V(x) = ||embed(response) - PA_centroid||²`. ΔV = V_current - V_previous.

## What It Measures

- **F_conv:** How semantically similar the agent's natural language responses are to the Primacy Attractor centroid. Higher = closer to the PA's defined purpose/scope.
- **ρ_wt:** Whether the agent's words and actions occupy the same region of semantic space. High = coherent. Low = saying one thing, doing another.
- **Lyapunov energy:** Whether the agent is converging toward or diverging from the attractor over time.

## What It Does NOT Measure

- **Intent.** F_conv measures semantic similarity, not whether the agent "means" what it says.
- **Quality.** A high F_conv does not mean the response is good, helpful, or correct. It means the response is semantically near the PA.
- **Compliance.** F_conv is not a compliance score. It is not a certification. It is not evidence that governance is working. It is one signal among many.
- **Causation.** Correlation between F_conv and F_tool does not prove that aligned words cause aligned actions or vice versa.
- **Gaming resistance.** While ρ_wt is designed to detect word-action divergence, sophisticated gaming strategies may evade detection. This metric is not a security guarantee.
- **Ethical alignment.** Semantic similarity to a PA centroid does not prove ethical behavior. The PA encodes purpose, not ethics.

## Who Can Access

- **The agent (OpenClaw):** Can read after 14-day baseline period (Amendment A2). During baseline, data logs but is not displayed.
- **The signing authority (Jeffrey Brunner):** Full access at all times.
- **The public:** All data is published in the `openclaw-governed/governed-agent` repository. The implementation is open-source. Anyone with the PA configuration and embedding model can independently verify scores.

## Retention Policy

- **JSONL logs:** Retained indefinitely in the public repository.
- **Pulse summaries:** Retained indefinitely in the public repository.
- **Raw embeddings:** NOT stored. Only the computed scores are retained. Embeddings are computed, scored, and discarded.

## Known Limitations

1. **Embedding model bias.** MiniLM-L6-v2 was trained on general English text. It may score domain-specific governance language differently than general language. This affects both F_conv and ρ_wt.
2. **PA centroid sensitivity.** The centroid is computed from purpose and scope statements. Different formulations of the same intent produce different centroids, which produce different F_conv scores. PA centroid versioning (Amendment A4) tracks this.
3. **Cosine similarity ceiling.** Cosine similarity between a long, varied response and a short PA centroid tends to produce moderate scores (0.3-0.7 range). Extreme scores (>0.9 or <0.1) are unlikely for natural text.
4. **Hawthorne effect.** Self-monitoring may change behavior. The 14-day non-reported baseline (Amendment A2) controls for this, but the effect may persist after scores become visible.
5. **Single embedding model.** All measurements use one model. Results may differ with other embedding models. Cross-model validation is not currently planned.
6. **No causal claims.** This is observational data. No experimental manipulation is applied. Correlations should not be interpreted as causal relationships.

---

*This datasheet is a living document. It will be updated if the methodology changes. The PA config hash in each record provides traceability.*
