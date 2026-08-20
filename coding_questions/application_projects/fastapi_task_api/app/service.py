"""Use-case operations for the FastAPI task service."""

from __future__ import annotations

from collections.abc import Sequence

from .models import TaskRecord
from .repository import TaskRepository
from .schemas import TaskCreate, TaskUpdate


class TaskService:
    """Coordinate validated schemas with repository operations."""

    def __init__(self, repository: TaskRepository) -> None:
        """Inject the request-scoped repository."""
        self.repository = repository

    def create(self, payload: TaskCreate) -> TaskRecord:
        """Create a task from a validated request schema."""
        return self.repository.create(
            title=payload.title,
            description=payload.description,
        )

    def list_all(self, *, offset: int, limit: int) -> Sequence[TaskRecord]:
        """Return a bounded task page."""
        return self.repository.list_all(offset=offset, limit=limit)

    def get(self, task_id: int) -> TaskRecord:
        """Return a task or propagate a controlled not-found error."""
        return self.repository.get(task_id)

    def update(self, task_id: int, payload: TaskUpdate) -> TaskRecord:
        """Apply fields explicitly supplied in a partial update."""
        task = self.repository.get(task_id)
        changes = payload.model_dump(exclude_unset=True)
        return self.repository.update(task, changes)

    def delete(self, task_id: int) -> None:
        """Delete an existing task."""
        self.repository.delete(self.repository.get(task_id))
