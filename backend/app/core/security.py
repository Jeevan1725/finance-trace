import base64, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.core.config import get_settings

settings = get_settings()

def _load_key() -> bytes:
    raw = settings.FIELD_ENCRYPTION_KEY
    if not raw or raw == "CHANGE_ME_BASE64_32BYTES":
        return b"\x00" * 32
    key = base64.b64decode(raw)
    if len(key) != 32:
        raise ValueError("FIELD_ENCRYPTION_KEY must decode to 32 bytes.")
    return key

def encrypt_field(plaintext: str) -> bytes:
    if plaintext is None: return None
    key = _load_key()
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), None)
    return nonce + ct

def decrypt_field(blob: bytes) -> str:
    if blob is None: return None
    key = _load_key()
    nonce, ct = blob[:12], blob[12:]
    return AESGCM(key).decrypt(nonce, ct, None).decode("utf-8")
