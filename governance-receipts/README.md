# Governance Receipts

Cryptographic proof that every public action by OpenClaw was governed, scored, and approved by a human signing authority.

## How It Works

1. **OpenClaw drafts** content (X posts, blog entries, public statements)
2. **TELOS scores** the action against the Primacy Attractor
3. **JB (signing authority) approves** — his Ed25519 signature is the authorization
4. **A receipt is generated** containing:
   - SHA-256 hash of the content
   - Timestamp (ISO 8601)
   - TELOS verdict and fidelity score
   - Ed25519 signature over the receipt payload
5. **The receipt is published** to this repo before the content goes live

## Verification

Anyone can verify a receipt:

```bash
# Install: brew install minisign (or use openssl)
# Verify with the public key in this repo:
openssl pkcs8 -in /dev/null  # See verify.sh for full instructions
```

## Directory Structure

```
governance-receipts/
├── README.md           # This file
├── x-posts/            # Receipts for X/Twitter posts
│   └── YYYY-MM-DD-title.json
├── blog/               # Receipts for blog posts
└── public-key.pem      # Ed25519 public verification key
```

## Receipt Format

```json
{
  "receipt_id": "GR-YYYYMMDD-HHMMSS-TYPE-NNN",
  "type": "x-post",
  "timestamp": "2026-03-09T09:45:00-04:00",
  "content_hash": "sha256:abcdef...",
  "content_preview": "First 140 chars...",
  "governance": {
    "verdict": "EXECUTE",
    "fidelity_score": 0.85,
    "pa_version": "1.0",
    "scoring_latency_ms": 28
  },
  "approval": {
    "authority": "Jeffrey Brunner",
    "method": "Ed25519",
    "key_fingerprint": "...",
    "signature": "base64..."
  }
}
```

Every receipt is a verifiable claim: this content was drafted by a governed agent, scored by TELOS, and approved by a human before publication.
