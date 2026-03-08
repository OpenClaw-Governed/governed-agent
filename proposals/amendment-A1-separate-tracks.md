# Amendment A1: Separate Tracks First

F_conv and F_tool are reported as parallel, independent metrics for 90 days.
No harmonic mean (PS_oc) is computed during this period.

**Rationale:** Cosine similarity distributions for conversational text vs tool action
strings score differently against the same PA centroid. The distributions must be
understood independently before combining them. Premature blending hides structural
differences between the two signals.

**Duration:** 90 days from first F_conv record.
**After 90 days:** Review distributions. If combining is justified, compute PS_oc.
