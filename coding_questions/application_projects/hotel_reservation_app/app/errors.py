"""Domain exceptions and Flask error handlers for the hotel API."""

from __future__ import annotations

from flask import Flask, jsonify


class ReservationNotFoundError(LookupError):
    """Raised when a requested reservation identifier is absent."""


class DuplicateReservationError(ValueError):
    """Raised when input data repeats a reservation identifier."""


class InvalidReservationError(ValueError):
    """Raised when reservation data conflicts with hotel configuration."""


def register_error_handlers(app: Flask) -> None:
    """Translate known application failures into stable JSON responses."""

    @app.errorhandler(ReservationNotFoundError)
    def reservation_not_found(_: ReservationNotFoundError) -> tuple[object, int]:
        """Return a controlled response for an unknown reservation."""
        return jsonify({"error": "Reservation not found"}), 404

    @app.errorhandler(404)
    def route_not_found(_: Exception) -> tuple[object, int]:
        """Return JSON instead of Flask's HTML page for an unknown route."""
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(_: Exception) -> tuple[object, int]:
        """Avoid exposing stack traces or internal details to API clients."""
        return jsonify({"error": "Internal server error"}), 500
