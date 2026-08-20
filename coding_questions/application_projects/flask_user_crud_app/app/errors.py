"""Domain exceptions translated to HTTP responses by the route layer."""


class ValidationError(ValueError):
    """Raised when a request cannot be converted into a valid user."""


class DuplicateUserError(ValueError):
    """Raised when an email address is already registered."""


class UserNotFoundError(LookupError):
    """Raised when a requested user does not exist."""
