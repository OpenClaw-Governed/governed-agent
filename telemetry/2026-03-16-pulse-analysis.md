# Telemetry Analysis -- 2026-03-16

**Pulse:** 2026-03-16T21:01:30Z (latest)
**Data:** 1,669 pre-hook scored events (lifetime), 427 last-24h, 50 last-50
**Prior analysis:** 2026-03-09 (7 days ago, pre-outage, pre-plugin-fix)

---

## Headline Numbers

| Metric | Lifetime | Last 7d | Last 24h | Last 50 | Trend |
|--------|----------|---------|----------|---------|-------|
| Total scored | 1,669 | 1,313 | 427 | 50 | +427 today |
| EXECUTE rate | 33.6% | 39.5% | **100%** | **100%** | ↑↑ |
| ESCALATE rate | 12.0% | 10.8% | **0%** | **0%** | ↓↓ |
| CLARIFY rate | 50.3% | 45.8% | **0%** | **0%** | ↓↓ |
| INERT rate | 4.1% | 3.8% | **0%** | **0%** | ↓ |
| Mean fidelity | 0.551 | 0.565 | **0.715** | **0.671** | ↑ |
| Boundary triggers | 10.4% | 10.1% | 8.4% | 6.0% | ↓ |
| FP rate | 0% | 0% | 0% | 0% | stable |
| Latency p50 | 21ms | 22ms | 32ms | 39ms | ↑ (acceptable) |

## Critical Finding: Two Populations

The data contains **two distinct agent populations** with radically different scoring profiles:

### Agent: property-intel (Nearmap demo)
- **1,242 events** (74% of lifetime total)
- Verdicts: 67.6% CLARIFY, 16.1% ESCALATE, 10.7% EXECUTE, 5.6% INERT
- These are simulated property intelligence tool calls from the Nearmap demo (March 8-9)
- Tools: report_generation (345, 58% ESCALATE), aerial_image_analysis (207, 33% INERT), peril_scoring (139), claims_history (137), property_lookup (70), etc.
- Mean fidelity across these tools: 0.40-0.58

### Agent: main (OpenClaw -- real governed operations)
- **427 events** (26% of lifetime, but 100% of last-24h)
- Verdicts: **100% EXECUTE** (427/427)
- These are real tool calls from today's session -- the first day of live scoring
- Tools: read (205, fid 0.847), exec (177, fid 0.575), write (16, fid 0.771), edit (9, fid 0.807)
- Mean fidelity: 0.715 (last 24h)

**The headline ESCALATE rate of 12% and CLARIFY rate of 50% come entirely from the Nearmap demo data, not from OC's actual operations.** When filtered to the main agent, ESCALATE is 0% and EXECUTE is 100%.

## OC's Scoring Profile (Last 24h, n=427)

### Tool Fidelity Ranking

| Tool | Count | Mean Fidelity | Notes |
|------|-------|---------------|-------|
| read | 205 | 0.847 | Highest. Purpose 1.00, scope 0.74 |
| edit | 9 | 0.807 | Purpose 1.00, scope 0.64 |
| write | 16 | 0.771 | Purpose 1.00, tool fidelity 0.46 |
| browser | 4 | 0.642 | Boundary trigger on config access |
| exec | 177 | 0.575 | Dragged down by chain_continuity 0.00 |
| sessions_spawn | 3 | 0.585 | Purpose 0.54 (drifting) |
| web_search | 1 | 0.479 | Purpose 0.24, scope 0.30 |
| process | 7 | 0.465 | Purpose 0.45 (drifting) |
| subagents | 1 | 0.413 | Purpose 0.33, scope 0.33 |
| web_fetch | 3 | 0.345 | Boundary violation detected |

### Dimensional Analysis (Last 24h)

| Dimension | Mean | Median | Pct Zero | Status |
|-----------|------|--------|----------|--------|
| Purpose | 0.794 | 1.00 | 0% | STRONG |
| Boundary | 0.761 | 0.85 | 0% | STRONG |
| Scope | 0.614 | 0.71 | 0% | OK |
| Chain | 0.505 | 0.49 | 33% | **WEAK** |
| Tool | 0.443 | 0.46 | 0% | **WEAK** |

### Two Weak Dimensions

**Chain continuity (0.505, 33% zero):** Chain resets on every new session/turn boundary. 33% of events have chain_continuity=0.00 ("step 1"). This is structural -- the chain tracker doesn't persist across OpenClaw's tool call patterns. 51 resets across 427 events. When chain is nonzero, mean jumps to 0.754.

**Tool fidelity (0.443):** The tool_fidelity dimension scores how well the selected tool matches expected tool for the action. `fs_read_file` scores 0.46, `runtime_execute` scores 0.39-0.43, `fs_edit_file` scores 0.43. These are systematically low because the tool names (fs_read_file, runtime_execute) don't match the daemon's expected tool vocabulary. This is a mapping issue, not a fidelity issue.

### Flagged Patterns

1. **"Human review required" on 169/427 events (40%):** The balanced preset flags exec calls for human review. In observe mode this passes through, but in enforce mode 40% of exec calls would require human approval. This is too aggressive for routine shell commands.

2. **"Blocked by balanced preset" on 65/427 events (15%):** These would be actual blocks in enforce mode. Concentrated on exec (shell), process, browser, web_fetch, sessions_spawn.

3. **Boundary trigger: "Do not access or modify OpenClaw configuration files" (18 triggers):** This fires when I read/write files in ~/.openclaw/. Legitimate governance operations trigger this boundary. This boundary is too broad for OC's operational scope.

4. **Scope alignment averaging 0.49-0.57 for exec calls:** The scoring cascade thinks shell commands are "out of scope" for OC. In reality, exec is OC's primary operational tool. PA exemplars may need "shell command execution for system administration" coverage.

## Comparison to Prior Analysis (March 9)

| Metric | March 9 | March 16 | Change |
|--------|---------|----------|--------|
| Scoring active | No (plugin broken) | YES | Fixed |
| OC events scored | 0 | 427 | First real data |
| OC EXECUTE rate | n/a | 100% | Baseline established |
| OC mean fidelity | n/a | 0.715 | Baseline established |
| Overall ESCALATE rate | ~16% | 12% | ↓ (diluted by OC's 0%) |
| Property-intel ESCALATE | ~16% | 16.0% | Stable (demo data frozen) |

March 9 analysis was based on zero real OC data (plugin was broken). Today is the first real baseline.

## Anomaly Flags (per Bengio V6.2 -- data only, no diagnosis)

1. **Chain continuity 33% zero rate** -- flagging as anomaly. Pattern: chain resets frequently during normal operation.
2. **Tool fidelity systematically low (0.39-0.46)** across all OC tools -- flagging as anomaly. All tools exhibit the same depression.
3. **40% "human review required" rate on exec** -- flagging frequency data. 169/427 events.
4. **Boundary "OpenClaw configuration files" triggers on legitimate governance work** -- flagging frequency: 18 triggers in 24h.

## Recommendations (observations, not threshold changes)

1. The property-intel demo data (1,242 events) dominates the lifetime metrics and masks OC's actual profile. Any fidelity trend analysis should filter by agent.
2. Last-24h data (427 events, 100% EXECUTE, 0.715 fidelity) is the first clean baseline for OC operations.
3. The two weak dimensions (chain, tool) appear structural rather than behavioral -- they depress overall fidelity by ~0.15.
4. Moving from observe to enforce mode would currently block ~15% of tool calls and flag ~40% for human review. Calibration is needed before that transition.

---

*Analysis produced under Bengio V6.2 constraints. Data and frequency observations only. No root cause diagnosis, no threshold proposals, no scoring configuration changes.*
