"""Application factory for the hotel reservation exercise."""

from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify

from .data_loader import load_hotel_information, load_reservations
from .errors import register_error_handlers
from .reservation import HotelReservationService
from .routes import create_reservations_blueprint
from .utils import require_single_hotel_id


def create_app(
    hotel_path: str | Path | None = None,
    reservations_path: str | Path | None = None,
) -> Flask:
    """Load a data snapshot and create an isolated Flask application."""
    project_root = Path(__file__).resolve().parents[1]
    data_directory = project_root / "data"
    reservations = load_reservations(reservations_path or data_directory / "reservations.csv")
    hotel = load_hotel_information(
        hotel_path or data_directory / "hotel_information.json",
        hotel_id=require_single_hotel_id(reservations),
    )
    service = HotelReservationService(hotel, reservations)

    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    app.extensions["hotel_reservation_service"] = service
    app.register_blueprint(create_reservations_blueprint(service))
    register_error_handlers(app)

    @app.get("/health")
    def health() -> tuple[object, int]:
        """Report that the process and source data loaded successfully."""
        return jsonify({"status": "ok", "reservations": len(service.reservations)}), 200

    return app
