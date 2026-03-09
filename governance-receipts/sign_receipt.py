#!/Users/jb/Desktop/StewartBot/.venv/bin/python3
"""Generate and Ed25519-sign a governance receipt for public content."""
import json, hashlib, subprocess, base64, sys, os
from datetime import datetime, timezone

def main():
    if len(sys.argv) < 4:
        print("Usage: sign_receipt.py <type> <title> <content-file> [signing-key]")
        sys.exit(1)

    receipt_type = sys.argv[1]
    title = sys.argv[2]
    content_file = sys.argv[3]
    signing_key = sys.argv[4] if len(sys.argv) > 4 else os.path.expanduser("~/.telos/keys/session_signing.key")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    receipts_dir = os.path.join(script_dir, f"{receipt_type}s")
    os.makedirs(receipts_dir, exist_ok=True)

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(content_file, 'r') as f:
        content = f.read()

    content_hash = f"sha256:{hashlib.sha256(content.encode()).hexdigest()}"

    receipt_file = os.path.join(receipts_dir, f"{now.strftime('%Y-%m-%d')}-{title}.json")

    receipt = {
        "receipt_id": f"GR-{now.strftime('%Y%m%d-%H%M%S')}-{receipt_type}-001",
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

    # Canonical payload for signing
    payload_bytes = json.dumps(receipt, sort_keys=True, separators=(',', ':')).encode()
    payload_hash = hashlib.sha256(payload_bytes).hexdigest()

    # Sign with Ed25519 via cryptography library
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        with open(signing_key, 'rb') as kf:
            private_key = load_pem_private_key(kf.read(), password=None)
        sig_bytes = private_key.sign(payload_bytes)
        sig = base64.b64encode(sig_bytes).decode()
        receipt["approval"]["signature"] = sig
        receipt["approval"]["payload_hash"] = payload_hash
        print("✅ Signed successfully")
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

if __name__ == "__main__":
    main()
