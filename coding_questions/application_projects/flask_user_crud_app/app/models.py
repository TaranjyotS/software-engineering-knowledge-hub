"""Domain models for the Flask user CRUD exercise."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    """A normalized user returned by the service and repository layers."""

    name: str
    email: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-compatible public representation."""
        return {"name": self.name, "email": self.email}
