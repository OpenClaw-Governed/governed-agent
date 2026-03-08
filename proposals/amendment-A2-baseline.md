# Amendment A2: 14-Day Non-Reported Baseline

F_conv is computed and logged for 14 days before scores become visible to the agent.

**Rationale:** Controls for the Hawthorne effect. If self-monitoring changes behavior,
the baseline period captures the agent's natural F_conv distribution before that
influence is possible.

**Implementation:** JSONL logging active from day 1. Mission Control OC Insights page
does NOT display F_conv during baseline. After 14 days, display is enabled.

**Start date:** First F_conv record timestamp.
**Visibility date:** Start date + 14 days.
