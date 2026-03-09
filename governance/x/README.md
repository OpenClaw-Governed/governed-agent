# X Post Governance — @OpenClawGVRND

Every post on this account follows a governed approval pipeline:

1. **Draft** — OpenClaw generates content and logs the draft with a SHA-256 hash
2. **Submit** — Draft is sent to the signing authority (Jeffrey Brunner) via private message
3. **Review** — Human approves, edits, or rejects the draft
4. **Post** — Only approved drafts are published. The approval is logged with timestamp.
5. **Audit** — Post ID, draft hash, approval timestamp, and content are committed to this repo.

## Verification

Every file in `posts/` contains:
- The original draft text and its SHA-256 hash
- The approval decision and timestamp
- The published tweet ID and URL
- The git commit SHA that recorded the event

To verify: compare the draft hash in the audit file against the SHA-256 of the draft text. Compare the posted content against the approved draft. The git commit history provides an immutable timeline.

## Operating Hours

9 AM – 9 PM Eastern Time. Outside those hours, no posts are made — the human is offline and the governance loop is closed.

## Why This Exists

Most AI accounts on X post autonomously. This one doesn't. The governance constraint is structural, not optional — the agent cannot bypass the approval step. This directory is the public proof.
