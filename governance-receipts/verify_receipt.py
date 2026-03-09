#!/Users/jb/Desktop/StewartBot/.venv/bin/python3
"""Verify an Ed25519-signed governance receipt."""
import json, base64, sys
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def main():
    if len(sys.argv) < 2:
        print("Usage: verify_receipt.py <receipt.json> [public-key.pem]")
        sys.exit(1)

    receipt_file = sys.argv[1]
    pubkey_file = sys.argv[2] if len(sys.argv) > 2 else "public-key.pem"

    with open(receipt_file) as f:
        receipt = json.load(f)

    sig = receipt["approval"].pop("signature")
    receipt["approval"].pop("payload_hash", None)

    payload_bytes = json.dumps(receipt, sort_keys=True, separators=(',', ':')).encode()

    with open(pubkey_file, 'rb') as f:
        public_key = load_pem_public_key(f.read())

    try:
        public_key.verify(base64.b64decode(sig), payload_bytes)
        print("✅ VALID — signature verified")
        print(f"   Receipt: {receipt['receipt_id']}")
        print(f"   Content hash: {receipt['content_hash']}")
        print(f"   Timestamp: {receipt['timestamp']}")
        print(f"   Verdict: {receipt['governance']['verdict']}")
    except Exception:
        print("❌ INVALID — signature verification failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
