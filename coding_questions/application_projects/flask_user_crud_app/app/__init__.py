"""Application factory for the Flask user CRUD exercise."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify

from .repository import SQLiteUserRepository
from .routes import create_users_blueprint
from .service import UserService


def create_app(database_path: str | Path | None = None) -> Flask:
    """Create an isolated Flask application and initialize its database.

    Args:
        database_path: Optional SQLite file. Tests inject a temporary path,
            while local runs use ``USER_DATABASE_PATH`` or ``data/users.db``.
    """
    project_root = Path(__file__).resolve().parents[1]
    configured_path = database_path or os.getenv(
        "USER_DATABASE_PATH",
        str(project_root / "data" / "users.db"),
    )

    repository = SQLiteUserRepository(configured_path)
    repository.initialize()
    service = UserService(repository)

    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.extensions["user_repository"] = repository
    app.register_blueprint(create_users_blueprint(service))

    @app.get("/health")
    def health() -> tuple[object, int]:
        """Report that the process and route layer are available."""
        return jsonify({"status": "ok"}), 200

    return app
