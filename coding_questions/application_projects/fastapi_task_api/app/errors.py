"""Domain exceptions for the FastAPI task service."""


class TaskNotFoundError(LookupError):
    """Raised when a requested task identifier does not exist."""
