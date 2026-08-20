"""Service and HTTP contract tests for the Flask user CRUD application."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app import create_app
from app.errors import DuplicateUserError, UserNotFoundError, ValidationError
from app.repository import SQLiteUserRepository
from app.service import UserService


class UserServiceTests(unittest.TestCase):
    """Exercise validation and persistence without the HTTP layer."""

    def setUp(self) -> None:
        """Create one temporary SQLite database per test."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        path = Path(self.temporary_directory.name) / "users.db"
        repository = SQLiteUserRepository(path)
        repository.initialize()
        self.service = UserService(repository)

    def test_create_normalizes_user_and_rejects_duplicate(self) -> None:
        """Normalize fields and enforce case-insensitive email uniqueness."""
        user = self.service.create({"name": "  Alex Doe  ", "email": "ALEX@Example.com"})
        self.assertEqual(user.email, "alex@example.com")
        with self.assertRaises(DuplicateUserError):
            self.service.create({"name": "Other", "email": "alex@example.com"})

    def test_validation_rejects_bad_payloads(self) -> None:
        """Reject malformed bodies, invalid emails, and unexpected fields."""
        invalid_payloads = (
            None,
            [],
            {"name": "", "email": "alex@example.com"},
            {"name": "Alex", "email": "invalid"},
            {"name": "Alex", "email": "alex@example.com", "role": "admin"},
        )
        for payload in invalid_payloads:
            with self.subTest(payload=payload), self.assertRaises(ValidationError):
                self.service.create(payload)

    def test_delete_unknown_user_raises(self) -> None:
        """Distinguish an absent user from a successful deletion."""
        with self.assertRaises(UserNotFoundError):
            self.service.delete("missing@example.com")


class UserApiTests(unittest.TestCase):
    """Verify status codes and response bodies through Flask's test client."""

    def setUp(self) -> None:
        """Create an isolated application and database per test."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        database_path = Path(self.temporary_directory.name) / "users.db"
        self.client = create_app(database_path).test_client()

    def test_user_lifecycle(self) -> None:
        """Create, retrieve, list, and delete a user through HTTP."""
        created = self.client.post(
            "/users",
            json={"name": "Alex Doe", "email": "alex@example.com"},
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.get_json()["user"]["email"], "alex@example.com")

        fetched = self.client.get("/users/alex@example.com")
        self.assertEqual(fetched.status_code, 200)
        self.assertEqual(len(self.client.get("/users").get_json()["users"]), 1)

        self.assertEqual(self.client.delete("/users/alex@example.com").status_code, 204)
        self.assertEqual(self.client.get("/users/alex@example.com").status_code, 404)

    def test_invalid_and_duplicate_requests(self) -> None:
        """Map validation and uniqueness failures to controlled client errors."""
        self.assertEqual(self.client.post("/users", data="not-json").status_code, 400)
        payload = {"name": "Alex Doe", "email": "alex@example.com"}
        self.assertEqual(self.client.post("/users", json=payload).status_code, 201)
        self.assertEqual(self.client.post("/users", json=payload).status_code, 409)


if __name__ == "__main__":
    unittest.main()
