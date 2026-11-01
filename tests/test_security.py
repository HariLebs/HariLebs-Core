import pytest

from harilebs_core.security import (
    generate_token,
    hash_secret,
    verify_secret,
)


def test_generate_token():
    token = generate_token()

    assert isinstance(token, str)
    assert len(token) > 0


def test_generate_token_minimum_length():
    with pytest.raises(ValueError):
        generate_token(length=15)


def test_verify_secret_correct():
    assert verify_secret("secret123", "secret123") is True


def test_verify_secret_incorrect():
    assert verify_secret("secret123", "wrong123") is False


def test_hash_secret():
    result = hash_secret("secret123")

    assert isinstance(result, str)
    assert len(result) == 64


def test_hash_secret_empty():
    with pytest.raises(ValueError):
        hash_secret("")


def test_verify_secret_invalid_provided_secret():
    assert verify_secret(None, "secret123") is False


def test_verify_secret_invalid_stored_secret():
    assert verify_secret("secret123", None) is False
