"""Domain models and date parsing for the hotel reservation exercise."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


def parse_datetime(value: str) -> datetime:
    """Parse ISO-8601 text, including the common ``Z`` UTC suffix."""
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"Invalid arrival datetime: {value}") from exc


@dataclass(frozen=True, slots=True)
class HotelInventory:
    """Room capacity for one hotel."""

    hotel_id: str
    rooms: dict[str, int]

    def __post_init__(self) -> None:
        """Reject empty room types and negative inventory counts."""
        if not self.hotel_id or not self.rooms:
            raise ValueError("Hotel ID and room inventory are required")
        if any(not room_type or count < 0 for room_type, count in self.rooms.items()):
            raise ValueError("Room types must be non-empty and counts cannot be negative")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible copy of the inventory."""
        return {"hotel_id": self.hotel_id, "inventory": dict(self.rooms)}


@dataclass(frozen=True, slots=True)
class Reservation:
    """A complete reservation record used by lookup and allocation APIs."""

    reservation_id: str
    room_type: str
    hotel_id: str
    guest_name: str
    arrival: datetime
    nights: int
    room_count: int

    def __post_init__(self) -> None:
        """Validate identifiers and positive booking quantities."""
        if (
            not self.reservation_id
            or not self.room_type
            or not self.hotel_id
            or not self.guest_name
        ):
            raise ValueError("Reservation, room, hotel, and guest identifiers are required")
        if self.nights <= 0 or self.room_count <= 0:
            raise ValueError("Nights and room count must be positive")

    @property
    def check_in(self) -> datetime:
        """Return 3:00 PM on the arrival calendar date."""
        return self.arrival.replace(hour=15, minute=0, second=0, microsecond=0)

    @property
    def check_out(self) -> datetime:
        """Return noon on the departure date after the booked nights."""
        departure = self.arrival + timedelta(days=self.nights)
        return departure.replace(hour=12, minute=0, second=0, microsecond=0)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible public representation."""
        return {
            "reservation_id": self.reservation_id,
            "room_type": self.room_type,
            "hotel_id": self.hotel_id,
            "guest_name": self.guest_name,
            "arrival": self.arrival.isoformat(),
            "nights": self.nights,
            "room_count": self.room_count,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat(),
        }


@dataclass(frozen=True, slots=True)
class AvailabilityReport:
    """Peak demand and remaining capacity during a target stay."""

    reservation_id: str
    peak_demand: dict[str, int]
    availability: dict[str, int]
    conflict: bool
    conflict_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible copy of the report."""
        return {
            "reservation_id": self.reservation_id,
            "peak_demand": dict(self.peak_demand),
            "availability": dict(self.availability),
            "conflict": self.conflict,
            "conflict_reason": self.conflict_reason,
        }
