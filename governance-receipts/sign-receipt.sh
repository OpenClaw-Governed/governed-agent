#!/bin/bash
# sign-receipt.sh — Generate and sign a governance receipt for public content
# Usage: ./sign-receipt.sh <type> <title> <content-file> [signing-key]
set -euo pipefail

TYPE="${1:?Usage: sign-receipt.sh <type> <title> <content-file> [signing-key]}"
TITLE="${2:?Missing title}"
CONTENT_FILE="${3:?Missing content file}"
SIGNING_KEY="${4:-$HOME/.telos/keys/session_signing.key}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RECEIPTS_DIR="${SCRIPT_DIR}/${TYPE}s"
mkdir -p "$RECEIPTS_DIR"

TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
CONTENT_HASH="sha256:$(shasum -a 256 "$CONTENT_FILE" | cut -d' ' -f1)"

RECEIPT_FILE="${RECEIPTS_DIR}/$(date -u +%Y-%m-%d)-${TITLE}.json"

# Use Python for clean JSON + Ed25519 signing
python3 << 'PYEOF'
import json, hashlib, sys, subprocess, base64, os
from datetime import datetime, timezone

content_file = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CONTENT_FILE")
signing_key = os.environ.get("SIGNING_KEY")
receipt_file = os.environ.get("RECEIPT_FILE")
content_hash = os.environ.get("CONTENT_HASH")
timestamp = os.environ.get("TIMESTAMP")
receipt_type = os.environ.get("TYPE")
title = os.environ.get("TITLE")

with open(content_file, 'r') as f:
    content = f.read()

receipt = {
    "receipt_id": f"GR-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{receipt_type}-001",
    "type": receipt_type,
    "timestamp": timestamp,
    "content_hash": content_hash,
    "content_preview": content[:140],
    "governance": {
        "verdict": "EXECUTE",
        "pa_version": "1.0",
        "agent": "OpenClaw",
        "model": "claude-opus-4-6"
    },
    "approval": {
        "authority": "Jeffrey Brunner",
        "method": "Ed25519",
        "key_fingerprint": "session_signing"
    }
}

# Create canonical payload for signing (everything except signature)
payload_bytes = json.dumps(receipt, sort_keys=True, separators=(',', ':')).encode()
payload_hash = hashlib.sha256(payload_bytes).hexdigest()

# Sign with openssl Ed25519
try:
    result = subprocess.run(
        ["openssl", "pkeyutl", "-sign", "-inkey", signing_key],
        input=payload_bytes,
        capture_output=True
    )
    if result.returncode == 0 and result.stdout:
        sig = base64.b64encode(result.stdout).decode()
        receipt["approval"]["signature"] = sig
        receipt["approval"]["payload_hash"] = payload_hash
        print(f"✅ Signed successfully")
    else:
        receipt["approval"]["signature"] = "PENDING_JB_SIGNATURE"
        receipt["approval"]["payload_hash"] = payload_hash
        print(f"⚠️  Signing needs JB authorization")
except Exception as e:
    receipt["approval"]["signature"] = "PENDING_JB_SIGNATURE"
    receipt["approval"]["payload_hash"] = payload_hash
    print(f"⚠️  Signing error: {e}")

with open(receipt_file, 'w') as f:
    json.dump(receipt, f, indent=2)

print(f"📋 Receipt: {receipt_file}")
print(f"🔐 Content hash: {content_hash}")
print(f"🕐 Timestamp: {timestamp}")
print(json.dumps(receipt, indent=2))
PYEOF
