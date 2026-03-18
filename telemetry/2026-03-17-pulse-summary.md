# Telemetry Pulse Summary -- 2026-03-17

**Source:** ~/.telos/pulse/memory_line.txt
**Timestamp:** 2026-03-17T13:00:06 UTC

## Current Pulse
| Metric | Value | Trend |
|--------|-------|-------|
| Events scored | 1,894 | +100 from Mar 16 night |
| ESCALATE rate | 10.6% | down from 11.1% (Mar 16) |
| False positive rate | 0.0% | stable |
| Mean fidelity | 0.561 | up from 0.554 |
| Posthoc correlation | 15% | stable |
| Chain zero rate | 14% | up from 13% |
| Gate criteria met | 0/3 | target: ESCALATE <5% for 3 consecutive |

## Advisory Fleet Findings (first cycle, 2026-03-16)
4 convergence findings from 6 advisors analyzing 2,168 events:
1. Observe mode must end -- open feedback loop
2. Tool fidelity miscalibrated at 0.443 mean -- mapping issue
3. Audit trail needs hardening -- no hash chain
4. Chain continuity structurally broken at 33%

## Trajectory
ESCALATE trending down: 74.9% (Mar 2) -> 42.4% (Mar 4) -> 16.7% (Mar 5) -> 11.1% (Mar 16) -> 10.6% (Mar 17).
At current rate, 5% gate target reachable within 1-2 weeks if tool fidelity mapping is fixed.
