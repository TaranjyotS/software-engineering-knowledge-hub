"""FastAPI application factory used by Uvicorn and automated tests."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .api import router
from .config import Settings
from .database import Base, create_database
from .errors import TaskNotFoundError


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a task API with its own database engine and lifecycle."""
    active_settings = settings or Settings.from_environment()
    database = create_database(active_settings.database_url)
    Base.metadata.create_all(database.engine)

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        """Expose database resources and dispose them during shutdown."""
        application.state.session_factory = database.session_factory
        yield
        database.engine.dispose()

    application = FastAPI(
        title="Task API Exercise",
        version="1.0.0",
        lifespan=lifespan,
    )
    application.state.session_factory = database.session_factory
    application.include_router(router)

    @application.exception_handler(TaskNotFoundError)
    async def task_not_found(
        _: Request,
        exception: TaskNotFoundError,
    ) -> JSONResponse:
        """Translate an absent task into a stable 404 response."""
        return JSONResponse(
            status_code=404,
            content={"detail": f"Task {exception.args[0]} was not found"},
        )

    @application.get("/health", tags=["operations"])
    def health() -> dict[str, str]:
        """Report that the API process is available."""
        return {"status": "ok"}

    return application
