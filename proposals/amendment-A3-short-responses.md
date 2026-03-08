# Amendment A3: Short Response Handling

Responses under 20 words are scored normally and flagged as `short_flag: true`.

**Decision:** Option (a) — score normally, flag as short.

**Rationale:** Normal scoring preserves the actual distribution. Imputation (option b)
smooths away real signal — short responses may genuinely have different semantic
properties than long ones, and we should observe that rather than mask it. The flag
enables filtering during analysis without corrupting the raw data.

A sentinel 1.0 is never assigned. That would corrupt the distribution.
