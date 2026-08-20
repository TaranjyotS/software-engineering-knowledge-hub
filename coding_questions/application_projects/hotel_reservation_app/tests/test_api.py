"""HTTP contract tests for the hotel reservation Flask API."""

from __future__ import annotations

import unittest

from app import create_app

REFERENCE_RESERVATION_ID = "3baf3d03-ce98-429e-a692-17dcbec4f3dd"


class HotelReservationApiTests(unittest.TestCase):
    """Verify successful and missing-resource API responses."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the complete dataset once and reuse a read-only test client."""
        cls.client = create_app().test_client()

    def test_health_inventory_and_reservation(self) -> None:
        """Expose health, inventory, and normalized reservation timestamps."""
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.get_json()["reservations"], 5139)
        inventory = self.client.get("/inventory")
        self.assertEqual(
            inventory.get_json()["inventory"],
            {"A": 261, "B": 137, "C": 130, "D": 58, "E": 4},
        )

        reservation = self.client.get(f"/reservations/{REFERENCE_RESERVATION_ID}")
        self.assertEqual(reservation.status_code, 200)
        payload = reservation.get_json()["reservation"]
        self.assertEqual(payload["guest_name"], "Evans Kagya")
        self.assertEqual(
            payload["check_in"],
            "2023-12-19T15:00:00+00:00",
        )

    def test_availability_and_not_found(self) -> None:
        """Return a report for known IDs and 404 for unknown IDs."""
        response = self.client.get(f"/reservations/{REFERENCE_RESERVATION_ID}/availability")
        report = response.get_json()["availability_report"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(report["peak_demand"]["A"], 189)
        self.assertEqual(report["availability"]["A"], 72)
        self.assertFalse(report["conflict"])
        self.assertEqual(self.client.get("/reservations/missing").status_code, 404)

    def test_original_routes_remain_compatible(self) -> None:
        """Retain the submitted route names and unwrapped response shapes."""
        reservation = self.client.get(f"/reservation/{REFERENCE_RESERVATION_ID}")
        self.assertEqual(reservation.status_code, 200)
        self.assertEqual(reservation.get_json()["guest_name"], "Evans Kagya")

        availability = self.client.get(f"/availability/{REFERENCE_RESERVATION_ID}")
        self.assertEqual(availability.status_code, 200)
        self.assertEqual(
            set(availability.get_json()),
            {"availability", "conflict", "conflict_reason"},
        )


if __name__ == "__main__":
    unittest.main()
