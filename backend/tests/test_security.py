import unittest
from unittest.mock import patch
from uuid import uuid4

import jwt
from pydantic import SecretStr

from app.core import security
from app.core.config import Settings


class PasswordSecurityTests(unittest.TestCase):
    def test_password_hash_is_not_plaintext_and_verifies_correctly(self) -> None:
        password = "Correct-Horse-Battery-42"
        password_hash = security.hash_password(password)

        self.assertNotEqual(password_hash, password)
        self.assertTrue(security.verify_password(password, password_hash))
        self.assertFalse(security.verify_password("wrong-password", password_hash))


class AccessTokenTests(unittest.TestCase):
    def test_token_round_trip_preserves_user_id(self) -> None:
        settings = Settings(
            auth_secret_key=SecretStr("test-only-signing-key-with-at-least-32-bytes")
        )
        user_id = uuid4()
        with patch.object(security, "get_settings", return_value=settings):
            token = security.create_access_token(user_id)
            decoded_user_id = security.decode_access_token(token)

        self.assertEqual(decoded_user_id, user_id)

    def test_token_rejects_an_invalid_signature(self) -> None:
        settings = Settings(
            auth_secret_key=SecretStr("test-only-signing-key-with-at-least-32-bytes")
        )
        with patch.object(security, "get_settings", return_value=settings):
            token = security.create_access_token(uuid4())
            with self.assertRaises(jwt.InvalidTokenError):
                security.decode_access_token(token + "tampered")

    def test_short_signing_key_is_rejected(self) -> None:
        settings = Settings(auth_secret_key=SecretStr("too-short"))
        with patch.object(security, "get_settings", return_value=settings):
            with self.assertRaises(security.TokenConfigurationError):
                security.create_access_token(uuid4())


if __name__ == "__main__":
    unittest.main()
