"""Domain and data-loading tests for hotel availability."""

from __future__ import annotations

import unittest
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from app.data_loader import load_hotel_information, load_reservations
from app.errors import ReservationNotFoundError
from app.models import HotelInventory, Reservation
from app.reservation import HotelReservationService, intervals_overlap

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_RESERVATION_ID = "3baf3d03-ce98-429e-a692-17dcbec4f3dd"
TIMED_ARRIVAL_RESERVATION_ID = "8785413c-2e00-4a82-b3e4-b651b6ed003d"


class HotelReservationServiceTests(unittest.TestCase):
    """Exercise date boundaries, loading, lookup, and peak demand."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the complete submitted dataset once for read-only tests."""
        reservations = load_reservations(PROJECT_ROOT / "data" / "reservations.csv")
        hotel = load_hotel_information(
            PROJECT_ROOT / "data" / "hotel_information.json",
            hotel_id="1738",
        )
        cls.hotel = hotel
        cls.loaded_reservations = reservations
        cls.service = HotelReservationService(hotel, reservations)

    def test_complete_source_dataset_is_loaded(self) -> None:
        """Preserve every source row, room type, capacity, and guest field."""
        self.assertEqual(len(self.loaded_reservations), 5139)
        self.assertEqual(
            Counter(item.room_type for item in self.loaded_reservations),
            {"A": 2629, "B": 1264, "C": 770, "D": 468, "E": 8},
        )
        self.assertEqual(
            self.hotel.rooms,
            {"A": 261, "B": 137, "C": 130, "D": 58, "E": 4},
        )
        reservation = self.service.get_reservation(REFERENCE_RESERVATION_ID)
        self.assertEqual(reservation.guest_name, "Evans Kagya")

    def test_full_dataset_peak_demand_regression(self) -> None:
        """Calculate known peak demand and capacity across all 5,139 rows."""
        report = self.service.availability_for_reservation(REFERENCE_RESERVATION_ID)
        self.assertEqual(
            report.peak_demand,
            {"A": 189, "B": 109, "C": 37, "D": 40, "E": 0},
        )
        self.assertEqual(
            report.availability,
            {"A": 72, "B": 28, "C": 93, "D": 18, "E": 4},
        )
        self.assertFalse(report.conflict)

    def test_full_dataset_covers_every_room_type(self) -> None:
        """Verify known peak and remaining capacity for A through E rooms."""
        cases = {
            "A": ("3baf3d03-ce98-429e-a692-17dcbec4f3dd", 189, 72),
            "B": ("4bc30bfd-f76b-4292-b5f7-d853de83ab49", 116, 21),
            "C": ("aeeccc43-e146-402b-b557-d63daa72b930", 99, 31),
            "D": ("50d8a2a3-c193-4eb2-b158-9dbeff90bb38", 28, 30),
            "E": ("af4485f4-022a-470c-9338-9755b6b4a915", 2, 2),
        }
        for room_type, (reservation_id, peak, remaining) in cases.items():
            with self.subTest(room_type=room_type):
                report = self.service.availability_for_reservation(reservation_id)
                self.assertEqual(report.peak_demand[room_type], peak)
                self.assertEqual(report.availability[room_type], remaining)
                self.assertFalse(report.conflict)

    def test_sweep_line_matches_independent_brute_force_oracle(self) -> None:
        """Cross-check full-data room demand without reusing the sweep algorithm."""
        target = self.service.get_reservation(REFERENCE_RESERVATION_ID)
        overlapping = [
            reservation
            for reservation in self.service.reservations.values()
            if reservation.room_type == target.room_type
            and intervals_overlap(
                reservation.check_in,
                reservation.check_out,
                target.check_in,
                target.check_out,
            )
        ]
        candidate_times = {target.check_in}
        candidate_times.update(
            reservation.check_in
            for reservation in overlapping
            if target.check_in <= reservation.check_in < target.check_out
        )
        brute_force_peak = max(
            sum(
                reservation.room_count
                for reservation in overlapping
                if reservation.check_in <= instant < reservation.check_out
            )
            for instant in candidate_times
        )

        report = self.service.availability_for_reservation(REFERENCE_RESERVATION_ID)
        self.assertEqual(report.peak_demand[target.room_type], brute_force_peak)

    def test_overlapping_stays_detect_overbooking(self) -> None:
        """Detect peak demand four against capacity three in an isolated case."""
        hotel = HotelInventory(hotel_id="test-hotel", rooms={"A": 3})
        reservations = [
            Reservation(
                reservation_id="first",
                room_type="A",
                hotel_id="test-hotel",
                guest_name="Guest One",
                arrival=datetime(2026, 8, 20, tzinfo=timezone.utc),
                nights=2,
                room_count=2,
            ),
            Reservation(
                reservation_id="second",
                room_type="A",
                hotel_id="test-hotel",
                guest_name="Guest Two",
                arrival=datetime(2026, 8, 21, tzinfo=timezone.utc),
                nights=1,
                room_count=2,
            ),
        ]
        report = HotelReservationService(hotel, reservations).availability_for_reservation("first")
        self.assertEqual(report.peak_demand["A"], 4)
        self.assertTrue(report.conflict)

    def test_back_to_back_stays_do_not_overlap(self) -> None:
        """Treat checkout and later check-in on the same day as reusable capacity."""
        hotel = HotelInventory(hotel_id="test-hotel", rooms={"A": 1})
        reservations = [
            Reservation(
                reservation_id="first",
                room_type="A",
                hotel_id="test-hotel",
                guest_name="Guest One",
                arrival=datetime(2026, 8, 20, tzinfo=timezone.utc),
                nights=1,
                room_count=1,
            ),
            Reservation(
                reservation_id="second",
                room_type="A",
                hotel_id="test-hotel",
                guest_name="Guest Two",
                arrival=datetime(2026, 8, 21, tzinfo=timezone.utc),
                nights=1,
                room_count=1,
            ),
        ]
        report = HotelReservationService(hotel, reservations).availability_for_reservation("first")
        self.assertEqual(report.peak_demand["A"], 1)
        self.assertFalse(report.conflict)

    def test_check_in_replaces_time_instead_of_adding_hours(self) -> None:
        """Set check-in to 3 PM even when source arrival contains a time."""
        reservation = self.service.get_reservation(TIMED_ARRIVAL_RESERVATION_ID)
        self.assertEqual(reservation.check_in.hour, 15)
        self.assertEqual(reservation.check_in.day, 1)

    def test_half_open_interval_boundary(self) -> None:
        """Do not overlap intervals that meet at one boundary."""
        first = Reservation(
            reservation_id="first",
            room_type="A",
            hotel_id="test-hotel",
            guest_name="Guest One",
            arrival=datetime(2026, 8, 20, tzinfo=timezone.utc),
            nights=1,
            room_count=1,
        )
        second = Reservation(
            reservation_id="second",
            room_type="A",
            hotel_id="test-hotel",
            guest_name="Guest Two",
            arrival=datetime(2026, 8, 21, tzinfo=timezone.utc),
            nights=1,
            room_count=1,
        )
        self.assertFalse(
            intervals_overlap(
                first.check_in,
                first.check_out,
                second.check_in,
                second.check_out,
            )
        )

    def test_unknown_reservation_raises(self) -> None:
        """Raise a domain error rather than indexing an empty result."""
        with self.assertRaises(ReservationNotFoundError):
            self.service.get_reservation("missing")


if __name__ == "__main__":
    unittest.main()
