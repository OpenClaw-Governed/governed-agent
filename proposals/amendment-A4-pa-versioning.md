# Amendment A4: PA Centroid Versioning

Every F_conv record includes `pa_config_hash`: SHA-256 of the PA configuration used.

**Rationale:** If the PA changes, old scores and new scores are not directly comparable.
The hash makes this explicit in every record. Analysis code can group by PA version
and flag cross-version comparisons.

**Implementation:** On startup and PA reload, compute SHA-256 of the PA purpose + scope
+ boundary statements. Include in every JSONL record.
