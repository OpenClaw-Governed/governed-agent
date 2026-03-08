# Amendment A6: Post-Hoc Only

F_conv is computed AFTER the response has been delivered to the conversation.
Never during generation. Never as input to response generation.

**Rationale:** This is structural, not just policy. If F_conv were computed during
generation, it could create a feedback loop where the agent optimizes mid-response.
Post-hoc computation ensures the response is finalized and sent before measurement.

**Implementation:** The F_conv computation hook fires on response delivery confirmation,
not on response generation. The response text is the delivered text, not a draft.
