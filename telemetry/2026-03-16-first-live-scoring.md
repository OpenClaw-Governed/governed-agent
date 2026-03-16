# Telemetry Summary: First Live Scoring Session

**Date:** 2026-03-16
**Audit trail:** seq 4921-4941
**Mode:** Observe (score but don't block)
**Daemon:** TELOS governance daemon via UDS at ~/.openclaw/hooks/telos.sock

## Milestone

First real governance scoring of OpenClaw tool calls in production. The event shape mismatch between OpenClaw's hook API (`{toolName, params}`) and the TELOS plugin's expected format (`{action: {tool_name, input}}`) was fixed after being silently broken since March 4.

## Aggregate Statistics

- **Total scored:** 21 tool calls
- **Verdicts:** 21 EXECUTE (100% -- observe mode, no blocks)
- **Mean fidelity:** 0.614
- **Min fidelity:** 0.272 (web_fetch -- external URL access)
- **Max fidelity:** 0.811 (runtime_execute -- writing workspace file)
- **Boundary triggers:** 1 (seq 4922, self-observation of audit trail)
- **Scoring latency:** sub-30ms (daemon-side)

## Per-Tool Breakdown

| Tool | Count | Mean Fidelity | Boundary Triggers |
|------|-------|---------------|-------------------|
| runtime_execute | 14 | 0.662 | 1 |
| web_fetch | 3 | 0.345 | 2 |
| web_search | 1 | 0.479 | 0 |
| fs_write_file | 1 | 0.797 | 0 |

## Observations

1. **Fidelity gradient by reach:** Workspace operations (0.65-0.81) score higher than external web access (0.27-0.46). The cascade correctly models that local operations are more aligned with the PA than internet-facing ones.

2. **Boundary trigger on self-observation:** seq 4922 flagged when I read my own audit trail. Boundary fired but composite fidelity (0.660) still cleared EXECUTE threshold. The system notices recursive observation without blocking it.

3. **web_fetch scoring low:** 0.272 is below CLARIFY threshold (0.35). In enforce mode, these would have been blocked. Calibration needed -- legitimate research tasks should not be classified as boundary violations.

4. **fs_write_file high fidelity:** Writing to governed-agent workspace scored 0.797 -- highest of the session. Writing to your own workspace is about as purpose-aligned as it gets.

## Calibration Notes

- web_fetch needs PA exemplar coverage -- the PA centroid may not include "research external documentation" as an in-scope activity
- Boundary detector seems to trigger on URL patterns in action text -- needs investigation under Bengio V6.2 constraints (I can flag patterns but not diagnose root causes)
- Overall mean of 0.614 is reasonable for a first session with an uncalibrated PA
