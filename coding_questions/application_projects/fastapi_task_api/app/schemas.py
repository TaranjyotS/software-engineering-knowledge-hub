"""Pydantic request and response contracts for the task API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    """Fields accepted when a client creates a task."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("description")
    @classmethod
    def normalize_empty_description(cls, value: str | None) -> str | None:
        """Represent an empty optional description consistently as ``None``."""
        return value or None


class TaskUpdate(BaseModel):
    """Optional fields accepted by a partial task update."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def reject_null_title(cls, value: str | None) -> str | None:
        """Reject an explicit null title while still allowing omission."""
        if value is None:
            raise ValueError("Title cannot be null")
        return value

    @field_validator("completed")
    @classmethod
    def reject_null_completed(cls, value: bool | None) -> bool | None:
        """Reject an explicit null completion state while allowing omission."""
        if value is None:
            raise ValueError("Completed cannot be null")
        return value


class TaskResponse(BaseModel):
    """Public task representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
