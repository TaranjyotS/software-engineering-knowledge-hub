"""FastAPI routes and request-scoped database dependencies."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.orm import Session, sessionmaker

from .repository import TaskRepository
from .schemas import TaskCreate, TaskResponse, TaskUpdate
from .service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_session(request: Request) -> Iterator[Session]:
    """Yield one SQLAlchemy session and always release it after the request."""
    session_factory: sessionmaker[Session] = request.app.state.session_factory
    with session_factory() as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]


def build_service(session: Session) -> TaskService:
    """Construct a request-scoped service around the current session."""
    return TaskService(TaskRepository(session))


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, session: SessionDependency) -> object:
    """Create and return one validated task."""
    return build_service(session).create(payload)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    session: SessionDependency,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
) -> list[object]:
    """Return a bounded page of tasks in creation order."""
    return list(build_service(session).list_all(offset=offset, limit=limit))


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: SessionDependency) -> object:
    """Return a task or raise a controlled domain error."""
    return build_service(session).get(task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    session: SessionDependency,
) -> object:
    """Apply only fields explicitly supplied by the client."""
    return build_service(session).update(task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: SessionDependency) -> Response:
    """Delete one task and return an empty successful response."""
    build_service(session).delete(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
