"""SQLite repository used by the Flask user CRUD application."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .errors import DuplicateUserError, UserNotFoundError
from .models import User


class SQLiteUserRepository:
    """Persist users in SQLite behind a small repository interface."""

    def __init__(self, database_path: str | Path) -> None:
        """Store the database path without opening a long-lived connection."""
        self.database_path = Path(database_path)

    def _connect(self) -> sqlite3.Connection:
        """Open a configured connection whose rows support named access."""
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        """Create the parent directory and users table when absent."""
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def create(self, user: User) -> User:
        """Insert a user or raise a domain-specific duplicate error."""
        try:
            with self._connect() as connection:
                connection.execute(
                    "INSERT INTO users (email, name) VALUES (?, ?)",
                    (user.email, user.name),
                )
        except sqlite3.IntegrityError as exc:
            raise DuplicateUserError(f"User already exists: {user.email}") from exc
        return user

    def get(self, email: str) -> User:
        """Return a user by normalized email or raise ``UserNotFoundError``."""
        with self._connect() as connection:
            row = connection.execute(
                "SELECT name, email FROM users WHERE email = ?",
                (email,),
            ).fetchone()
        if row is None:
            raise UserNotFoundError(email)
        return User(name=row["name"], email=row["email"])

    def list_all(self) -> list[User]:
        """Return every user in deterministic creation order."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT name, email FROM users ORDER BY created_at, email"
            ).fetchall()
        return [User(name=row["name"], email=row["email"]) for row in rows]

    def delete(self, email: str) -> None:
        """Delete one user or raise ``UserNotFoundError``."""
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM users WHERE email = ?", (email,))
        if cursor.rowcount == 0:
            raise UserNotFoundError(email)
