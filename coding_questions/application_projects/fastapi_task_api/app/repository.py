"""Database queries for the FastAPI task service."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from .errors import TaskNotFoundError
from .models import TaskRecord


class TaskRepository:
    """Persist and retrieve tasks through one request-scoped session."""

    def __init__(self, session: Session) -> None:
        """Store the injected SQLAlchemy session."""
        self.session = session

    def create(self, *, title: str, description: str | None) -> TaskRecord:
        """Insert a task and refresh generated fields before returning it."""
        task = TaskRecord(title=title, description=description, completed=False)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def list_all(self, *, offset: int, limit: int) -> Sequence[TaskRecord]:
        """Return a deterministic, bounded page of tasks."""
        statement = select(TaskRecord).order_by(TaskRecord.id).offset(offset).limit(limit)
        return self.session.scalars(statement).all()

    def get(self, task_id: int) -> TaskRecord:
        """Return a task by primary key or raise ``TaskNotFoundError``."""
        task = self.session.get(TaskRecord, task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def update(self, task: TaskRecord, changes: Mapping[str, Any]) -> TaskRecord:
        """Apply validated fields, commit the transaction, and refresh the row."""
        for field, value in changes.items():
            setattr(task, field, value)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: TaskRecord) -> None:
        """Delete and commit one persistent task."""
        self.session.delete(task)
        self.session.commit()
