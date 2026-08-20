"""Flask routes for hotel inventory and reservation availability."""

from __future__ import annotations

from flask import Blueprint, jsonify

from .reservation import HotelReservationService


def create_reservations_blueprint(service: HotelReservationService) -> Blueprint:
    """Create routes bound to a validated reservation service."""
    blueprint = Blueprint("reservations", __name__)

    @blueprint.get("/inventory")
    def get_inventory() -> tuple[object, int]:
        """Return configured capacity for every room type."""
        return jsonify(service.hotel.to_dict()), 200

    @blueprint.get("/reservations/<string:reservation_id>")
    def get_reservation(reservation_id: str) -> tuple[object, int]:
        """Return every source field for one reservation."""
        reservation = service.get_reservation(reservation_id)
        return jsonify({"reservation": reservation.to_dict()}), 200

    @blueprint.get("/reservation/<string:reservation_id>")
    def get_reservation_compatibility(reservation_id: str) -> tuple[object, int]:
        """Preserve the original route and unwrapped response contract."""
        return jsonify(service.get_reservation(reservation_id).to_dict()), 200

    @blueprint.get("/reservations/<string:reservation_id>/availability")
    def get_availability(reservation_id: str) -> tuple[object, int]:
        """Return peak demand and remaining inventory for a selected stay."""
        report = service.availability_for_reservation(reservation_id)
        return jsonify({"availability_report": report.to_dict()}), 200

    @blueprint.get("/availability/<string:reservation_id>")
    def get_availability_compatibility(reservation_id: str) -> tuple[object, int]:
        """Preserve the original availability route and response fields."""
        report = service.availability_for_reservation(reservation_id)
        return (
            jsonify(
                {
                    "availability": report.availability,
                    "conflict": report.conflict,
                    "conflict_reason": report.conflict_reason,
                }
            ),
            200,
        )

    return blueprint
