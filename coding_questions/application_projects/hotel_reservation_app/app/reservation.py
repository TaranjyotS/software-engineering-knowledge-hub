"""Reservation lookup and peak-demand availability calculations."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

from .errors import (
    DuplicateReservationError,
    InvalidReservationError,
    ReservationNotFoundError,
)
from .models import AvailabilityReport, HotelInventory, Reservation


def intervals_overlap(
    first_start: datetime,
    first_end: datetime,
    second_start: datetime,
    second_end: datetime,
) -> bool:
    """Return whether two half-open intervals overlap."""
    return first_start < second_end and second_start < first_end


class HotelReservationService:
    """Index reservations and evaluate them against fixed room capacity."""

    def __init__(
        self,
        hotel: HotelInventory,
        reservations: Iterable[Reservation],
    ) -> None:
        """Validate and index one immutable reservation snapshot."""
        self.hotel = hotel
        self.reservations: dict[str, Reservation] = {}
        timezone_awareness: set[bool] = set()

        for reservation in reservations:
            if reservation.reservation_id in self.reservations:
                raise DuplicateReservationError(reservation.reservation_id)
            if reservation.hotel_id != hotel.hotel_id:
                raise InvalidReservationError(
                    f"Reservation {reservation.reservation_id} belongs to another hotel"
                )
            if reservation.room_type not in hotel.rooms:
                raise InvalidReservationError(f"Unknown room type: {reservation.room_type}")
            self.reservations[reservation.reservation_id] = reservation
            timezone_awareness.add(reservation.arrival.utcoffset() is not None)

        if len(timezone_awareness) > 1:
            raise InvalidReservationError(
                "Reservation datetimes must be consistently timezone-aware or naive"
            )

    def get_reservation(self, reservation_id: str) -> Reservation:
        """Return one reservation or raise a controlled lookup error."""
        try:
            return self.reservations[reservation_id]
        except KeyError as exc:
            raise ReservationNotFoundError(reservation_id) from exc

    def availability_for_reservation(self, reservation_id: str) -> AvailabilityReport:
        """Calculate peak concurrent room demand during the selected stay."""
        target = self.get_reservation(reservation_id)
        peak_demand = {
            room_type: self._peak_demand(
                room_type,
                window_start=target.check_in,
                window_end=target.check_out,
            )
            for room_type in self.hotel.rooms
        }
        availability = {
            room_type: max(self.hotel.rooms[room_type] - demand, 0)
            for room_type, demand in peak_demand.items()
        }

        target_demand = peak_demand[target.room_type]
        target_capacity = self.hotel.rooms[target.room_type]
        conflict = target_demand > target_capacity
        reason = None
        if conflict:
            reason = (
                f"Room type {target.room_type} is overbooked: peak demand "
                f"{target_demand}, capacity {target_capacity}"
            )

        return AvailabilityReport(
            reservation_id=target.reservation_id,
            peak_demand=peak_demand,
            availability=availability,
            conflict=conflict,
            conflict_reason=reason,
        )

    def _peak_demand(
        self,
        room_type: str,
        *,
        window_start: datetime,
        window_end: datetime,
    ) -> int:
        """Return peak occupied rooms of one type inside a target interval."""
        events: list[tuple[datetime, int]] = []
        for reservation in self.reservations.values():
            if reservation.room_type != room_type:
                continue
            if not intervals_overlap(
                reservation.check_in,
                reservation.check_out,
                window_start,
                window_end,
            ):
                continue

            events.append((max(reservation.check_in, window_start), reservation.room_count))
            events.append((min(reservation.check_out, window_end), -reservation.room_count))

        current = 0
        peak = 0
        for _, delta in sorted(events, key=lambda event: (event[0], event[1])):
            current += delta
            peak = max(peak, current)
        return peak
