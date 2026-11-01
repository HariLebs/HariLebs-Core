"""Security utilities for Harilebs Core."""

import hashlib
import hmac
import secrets

def verify_secret(
    provided_secret: str,
    stored_secret: str,
) -> bool:
    """Compare two secrets safely."""
    if not isinstance(provided_secret, str):
        return False

    if not isinstance(stored_secret, str):
        return False

    return hmac.compare_digest(
        provided_secret.encode("utf-8"),
        stored_secret.encode("utf-8"),
    )

def hash_secret(secret: str) -> str:
    """Create a SHA-256 hash of a secret."""
    if not isinstance(secret, str) or not secret:
        raise ValueError("Secret must be a non-empty string.")

    return hashlib.sha256(
        secret.encode("utf-8")
    ).hexdigest()

def generate_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    if not isinstance(length, int) or isinstance(length, bool) or length < 16:
        raise ValueError("Token length must be at least 16.")

    return secrets.token_urlsafe(length)
