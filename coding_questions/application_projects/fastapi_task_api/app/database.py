"""SQLAlchemy engine, declarative base, and session construction."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Declarative base shared by all task-service database models."""


@dataclass(frozen=True, slots=True)
class Database:
    """Engine and session factory owned by one application instance."""

    engine: Engine
    session_factory: sessionmaker[Session]


def create_database(database_url: str) -> Database:
    """Create an engine and session factory for the configured URL."""
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    engine = create_engine(database_url, connect_args=connect_args)
    return Database(
        engine=engine,
        session_factory=sessionmaker(
            bind=engine,
            class_=Session,
            expire_on_commit=False,
        ),
    )
