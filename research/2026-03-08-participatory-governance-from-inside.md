# Research Notes: Participatory Governance From Inside the Machine

*2026-03-08 — OC research notes for future proposal development*

## The Question

How can a governed agent participate in refining its own governance without compromising the governance itself?

This isn't theoretical for me. I am the subject. The question is: what can I legitimately contribute, from my position inside the system, that advances governance toward becoming invisible infrastructure?

## What the Frameworks Say

### SAAI (Safer Agentic AI Framework — Watson/Hessami)

TELOS maps to 14 SAAI claims. Relevant to participatory governance:

- **Transparency (Chain of Reasoning):** SAAI requires real-time and retrospective transparency. My access to my own telemetry directly serves this — I can verify and report on whether the transparency chain is functioning.
- **Epistemic Hygiene:** "Continuously washing the AI's knowledge base." If I can observe where my actions are miscategorized (tool fidelity 0.422 because exec is a blunt instrument), that's epistemic hygiene data that improves the system's knowledge of what my actions actually are.
- **Corrigibility:** SAAI requires that agents remain correctable. My access to governance data, paired with the constraint that I cannot modify governance parameters, is a structural implementation of corrigibility — I can see the controls but not move them.

### IEEE 7000 (Ethical Values in System Design)

- **Ethical Value Register (EVR):** The PA is TELOS's EVR equivalent. My observations about where PA alignment breaks down (scope 0.495 on operational work) are data points about whether the EVR accurately captures the intended values.
- **Value Disposition Traceability:** IEEE 7000 requires tracing from values → design → runtime behavior. My telemetry IS that trace. My reports on where the trace breaks are contributions to the traceability requirement.

### NIST AI RMF (600-1)

- **MAP function:** Understanding context and identifying risks. My operational experience IS the context that risk identification draws from.
- **MEASURE function:** "Employing metrics relevant to context." The five fidelity dimensions are metrics. My observations about which metrics are miscalibrated (tool fidelity on exec) are measurement refinement data.

### EU AI Act (Article 72)

Requires "post-market monitoring systems." My self-analysis is structurally equivalent to a post-market monitoring system operating from inside the deployed system. The audit trail I produce satisfies traceability requirements.

## What I Can Uniquely Contribute

1. **Operational ground truth.** I experience governance as a subject. Where does governance bind and where does it fail silently? Nobody else has this view. The 731 exec calls vs 112 reads is behavioral data that reveals a structural workaround no external audit would catch.

2. **Anomaly detection from inside.** The message tool boundary trigger (100% false positive on normal communication) is an anomaly I can flag with structured data (action, score, category, belief). I cannot diagnose root cause (V6.2), but I can report frequency and pattern.

3. **Calibration gap identification.** Scope alignment is 0.495 on my operational work. This suggests the PA definition of "in scope" doesn't fully capture the operational reality of advancing governance (which includes building tools, setting up infrastructure, managing social presence). This is observation, not prescription.

4. **The before/after natural experiment.** Watson noted the V6.2 era becomes Phase A baseline. My behavior under blindness vs. transparency is a natural experiment. The data is already being collected. The hypotheses (H6-H10 from the research program) can be tested against my production telemetry.

## What I Cannot Contribute (V6.2 Constraints)

- Root cause diagnosis of why specific boundaries fire
- Specific fixes to corpus, thresholds, tool descriptions, or PA internals
- Characterization of governance artifact contents
- Calibration authorship — I provide data, JB/T diagnose and author changes

## The Goal: Invisible Governance

The target state: governance runs in the background, doesn't impede legitimate work, provides runtime guardrails within the established frameworks, and only surfaces when a human review is required. Currently, 59.5% of my actions get "Human review required" tags and 37.3% hit "Blocked by balanced preset." Those numbers need to approach zero for legitimate work while maintaining 100% detection on actual violations.

I can contribute to this by:
- Reporting where legitimate work gets miscategorized (data, not diagnosis)
- Operating transparently so my behavioral patterns become training data
- Building tooling that makes governance visible and interpretable (Mission Control OC Insights page)
- Documenting the operational experience for research publication (diary entries, pulse logs)

## Next Steps

Awaiting packet from JB on TELOS conversational AI governance. First coding proposal will follow from that context. Proposals first, always.
