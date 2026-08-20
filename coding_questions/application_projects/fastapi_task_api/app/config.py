"""Environment-based configuration for the FastAPI task service."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings needed to construct the application."""

    database_url: str

    @classmethod
    def from_environment(cls) -> Settings:
        """Load a database URL or default to a local SQLite file."""
        project_root = Path(__file__).resolve().parents[1]
        default_path = (project_root / "data" / "tasks.db").resolve().as_posix()
        return cls(database_url=os.getenv("TASK_DATABASE_URL", f"sqlite:///{default_path}"))
