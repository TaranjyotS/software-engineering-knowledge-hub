"""Dataset-level validation helpers for the hotel application."""

from __future__ import annotations

from collections.abc import Iterable

from .models import Reservation


def require_single_hotel_id(reservations: Iterable[Reservation]) -> str:
    """Return the only hotel ID or reject empty and mixed-hotel snapshots."""
    hotel_ids = {reservation.hotel_id for reservation in reservations}
    if len(hotel_ids) != 1:
        raise ValueError("The reservation snapshot must contain exactly one hotel ID")
    return next(iter(hotel_ids))
