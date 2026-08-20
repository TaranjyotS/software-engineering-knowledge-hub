"""Validation and business rules for the Flask user CRUD application."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from .errors import ValidationError
from .models import User
from .repository import SQLiteUserRepository

EMAIL_PATTERN = re.compile(
    r"^[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?"
    r"(?:\.[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?)+$",
    re.IGNORECASE,
)


class UserService:
    """Apply user rules before delegating persistence to a repository."""

    def __init__(self, repository: SQLiteUserRepository) -> None:
        """Inject the repository so tests can isolate application state."""
        self.repository = repository

    @staticmethod
    def normalize_email(email: str) -> str:
        """Normalize and validate an email address used as a stable key."""
        normalized = email.strip().casefold()
        if not EMAIL_PATTERN.fullmatch(normalized):
            raise ValidationError("Email address is invalid")
        return normalized

    @classmethod
    def parse_user(cls, payload: Any) -> User:
        """Validate an untrusted JSON value and construct a ``User``."""
        if not isinstance(payload, Mapping):
            raise ValidationError("Request body must be a JSON object")

        unexpected = set(payload) - {"name", "email"}
        if unexpected:
            fields = ", ".join(sorted(str(field) for field in unexpected))
            raise ValidationError(f"Unexpected fields: {fields}")

        name = payload.get("name")
        email = payload.get("email")
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Name must be a non-empty string")
        if not isinstance(email, str):
            raise ValidationError("Email must be a string")
        return User(name=name.strip(), email=cls.normalize_email(email))

    def create(self, payload: Any) -> User:
        """Validate and persist one user."""
        return self.repository.create(self.parse_user(payload))

    def get(self, email: str) -> User:
        """Return a user by a validated, normalized email."""
        return self.repository.get(self.normalize_email(email))

    def list_all(self) -> list[User]:
        """Return all persisted users."""
        return self.repository.list_all()

    def delete(self, email: str) -> None:
        """Delete a user by normalized email."""
        self.repository.delete(self.normalize_email(email))
