# Competitive Landscape Update -- March 17, 2026

*Updated from March 4, 2026 baseline. Sources: Google Search, company websites, press releases.*

---

## Major Movements Since Last Sweep (March 4)

### 1. Fiddler AI -- $30M Series C (Jan 27, 2026)
- **Led by:** RPS Ventures. Existing: Lightspeed, Lux Capital, Insight Partners, Capgemini, Mozilla Ventures. New: LG Technology Ventures, Benhamou Global Ventures.
- **Positioning:** "First control plane for compound AI systems" -- standardized telemetry, evaluation, continuous monitoring, enforceable policy, auditable governance across AI lifecycle.
- **Revenue:** 4x growth in 18 months.
- **Distribution:** AWS Pattern Partner status. #1 in AI Agent Security & Risk Management (unnamed ranking).
- **Key quote (RPS):** "A single agentic workflow can involve dozens of handoffs between models, tools, and APIs -- each one a potential point of failure."
- **TELOS implication:** **Direct competitor in positioning language.** "Control plane" and "enforceable policy" overlap with our messaging. Key difference: Fiddler is observability-first (monitor then govern). TELOS is governance-first (score before execute). Fiddler does post-hoc; TELOS does pre-action.

### 2. Lakera -- Acquired by Check Point Software (Sep 2025)
- **Status:** Now part of Check Point's GenAI Protect offering. No longer an independent startup.
- **Product:** Lakera Guard (prompt injection, content safety, LLM backend security benchmark).
- **Last independent funding:** $20M Series A (Jul 2024).
- **Open source:** b3 benchmark for LLM backend security in AI agents (Oct 2025).
- **TELOS implication:** Lakera was input/output security (what LLMs say). Check Point integration makes it a network security play. Still not action-level governance. Acquisition validates the market but removes an independent competitor.

### 3. Arthur AI -- Agent Discovery & Governance (ADG) Platform
- **Jan 7, 2026:** Launched ADG on Google Cloud Marketplace.
- **Jan 29, 2026:** New toolkit for building reliable agents (model experimentation, eval monitoring, drift detection).
- **Mar 3, 2026:** Blog post on "Shadow Agent Crisis" -- enterprises deploying agents without visibility or governance.
- **Mar 5, 2026:** Webinar on agent explosion and ADG principles.
- **Positioning:** "Ship Reliable AI Agents Fast" -- discover, govern, monitor, evaluate.
- **TELOS implication:** **Most direct competitor in the agent governance space.** Arthur's ADG is discovery + monitoring + evaluation. Still observability-focused. They see agents AFTER deployment. TELOS governs DURING execution. Arthur's GCP marketplace distribution is a commercial advantage we don't have yet.

### 4. Patronus AI -- LLM Evaluation & Testing
- **Funding:** $17M Series A (May 2024, Notable Capital). $20M total.
- **Dec 2025:** VentureBeat coverage: "AI agents fail 63% of the time on complex tasks" -- Patronus building eval tools for agent reliability.
- **Products:** Multimodal LLM-as-a-Judge, automated evaluation platform, FinanceBench.
- **Partnerships:** MongoDB, CARIAD (Volkswagen).
- **TELOS implication:** Evaluation and testing, not runtime governance. Complementary, not competitive. They measure quality; we enforce policy.

### 5. Cisco AI Defense (NEW -- GTC 2026, March 16)
- **Just announced (yesterday):** Purpose-built guardrails for AI agents as part of Cisco AI Defense.
- **Context:** Cisco Secure AI Factory with NVIDIA. Model security, automated vulnerability testing, agent guardrails.
- **TELOS implication:** Big tech entering agent guardrails. Cisco is network-layer, perimeter security. Not the same as PA-based purpose governance. But enterprise buyers may default to "one vendor" solutions.

### 6. NVIDIA Open Agent Development Platform (March 16)
- **GTC 2026 announcement:** Open platform for agent development with enterprise partners.
- **TELOS implication:** Infrastructure play, not governance. But NVIDIA's ecosystem influence means governance tools that integrate with their platform get distribution.

---

## NEW Entrants & Adjacent Players

| Player | What | TELOS Differentiation |
|--------|------|----------------------|
| **Fiddler AI** ($30M) | Control plane for compound AI -- telemetry, eval, monitoring, policy | Post-hoc observability vs TELOS pre-action scoring |
| **OneTrust** | AI governance module (privacy/compliance-first) | Policy documents + risk registers. No real-time action scoring. |
| **Collibra** | AI Governance 2026.03 -- operating model changes (data governance extends to AI) | Data catalog approach. No agent action enforcement. |
| **Openlayer** | AI guardrails guide -- input validation, output checks | Request/response validation. Same tier as Guardrails AI. |
| **Sonar** | Building guardrails for AI coding systems (Sonar Summit 2026) | Code quality focus. Not agent governance. |

---

## Landscape Summary

### What's Changed
1. **Money is flowing:** Fiddler $30M, Lakera acquired by Check Point. The market is real and heating up.
2. **"Agent governance" is now a category name.** Arthur coined "Agent Discovery & Governance" (ADG). Fiddler uses "control plane." Everyone is converging on the same problem statement.
3. **Big tech is entering:** Cisco AI Defense with agent guardrails. NVIDIA with open agent platform. Google Cloud distributing Arthur.
4. **The gap TELOS fills is still open:** Nobody does pre-action mathematical scoring against a human-defined purpose attractor. Everyone else is post-hoc (observe, evaluate, monitor). TELOS is the only system that scores BEFORE execution.

### Competitive Threats (ranked)
1. **Arthur AI** -- closest to our positioning. Agent-specific governance. GCP distribution. Well-funded.
2. **Fiddler AI** -- "control plane" language overlaps ours. $30M fresh capital. AWS distribution.
3. **Cisco AI Defense** -- enterprise trust, bundled with existing security. Agent guardrails.
4. **Guardrails AI** -- still request-level, not action-level. But 10.8K GitHub stars = community.
5. **Patronus AI** -- evaluation-focused. Complementary but could expand scope.

### TELOS Advantages
- **Pre-action vs post-hoc**: Only system scoring before execution
- **Mathematical PA**: Purpose defined as embedding-space attractor, not rule lists
- **Sub-30ms latency**: Real-time enforcement feasible in production
- **Cryptographic audit**: Ed25519 + HMAC-SHA512 receipts
- **Self-governed proof**: OpenClaw is production evidence, not a demo
- **Local-first**: No cloud dependency for scoring (Metal 4 / MLX)

### Strategic Implications
- Arthur and Fiddler both have cloud marketplace distribution. TELOS needs a distribution strategy.
- "Control plane for AI" is becoming a crowded pitch. Need to sharpen differentiation: **purpose governance** vs **observability with guardrails**.
- The regulatory tailwind is accelerating (California AI laws Jan 2026, EU AI Act, Colorado SB 24-205). Every competitor references it. We need to be louder.
- Insurance vertical (Nearmap use case) is underserved -- AXA, Travelers building agentic systems but no governance vendor owns this vertical yet.

---

*Next update: 2 weeks or upon major competitor announcement.*
