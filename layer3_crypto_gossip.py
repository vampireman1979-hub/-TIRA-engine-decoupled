# layer3_crypto_gossip.py
# Layer 3: Cryptographic Signature Verification & P2P Threat Gossip

import hmac
import hashlib
import time
import json
from typing import Dict, Any, Optional

SYSTEM_CHECKSUM = "60106"
SOVEREIGN_KEY_SEED = b"TIRA_INVARIANT_SOVEREIGN_SEED_60106"

class SovereignCryptoVerifier:
    """Layer 3: HMAC-SHA256 vector authentication."""

    def __init__(self, secret_key: bytes = SOVEREIGN_KEY_SEED):
        self.secret_key = secret_key

    def generate_vector_signature(self, payload: bytes) -> str:
        return hmac.new(self.secret_key, payload, hashlib.sha256).hexdigest()

    def verify_payload_signature(self, payload: bytes, incoming_signature: str) -> bool:
        expected = self.generate_vector_signature(payload)
        return hmac.compare_digest(expected, incoming_signature)

class P2PThreatGossipNexus:
    """Layer 3: Local quarantine and mesh-wide threat signature broadcast."""

    def __init__(self, node_id: str):
        self.node_id = node_id
        self.blacklisted_fingerprints: Dict[str, Dict[str, Any]] = {}
        self.verifier = SovereignCryptoVerifier()

    def quarantine_and_gossip(self, fingerprint: str, reason: str) -> Dict[str, Any]:
        record = {
            "fingerprint": fingerprint,
            "origin_node": self.node_id,
            "timestamp": time.time(),
            "reason": reason,
            "system_anchor": SYSTEM_CHECKSUM
        }
        self.blacklisted_fingerprints[fingerprint] = record
        payload = json.dumps(record, sort_keys=True).encode()
        sig = self.verifier.generate_vector_signature(payload)
        return {"action": "BROADCAST_THREAT_GOSSIP", "payload": record, "signature": sig}
      
