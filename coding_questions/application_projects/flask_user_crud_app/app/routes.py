"""Flask routes that translate HTTP requests into service operations."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from .errors import DuplicateUserError, UserNotFoundError, ValidationError
from .service import UserService


def create_users_blueprint(service: UserService) -> Blueprint:
    """Create user routes bound to an injected service instance."""
    blueprint = Blueprint("users", __name__)

    @blueprint.post("/users")
    def create_user() -> tuple[object, int]:
        """Create a validated user from a JSON request body."""
        try:
            user = service.create(request.get_json(silent=True))
        except ValidationError as exc:
            return jsonify({"error": str(exc)}), 400
        except DuplicateUserError as exc:
            return jsonify({"error": str(exc)}), 409
        return jsonify({"user": user.to_dict()}), 201

    @blueprint.get("/users")
    def list_users() -> tuple[object, int]:
        """Return all users in deterministic order."""
        return jsonify({"users": [user.to_dict() for user in service.list_all()]}), 200

    @blueprint.get("/users/<path:email>")
    def get_user(email: str) -> tuple[object, int]:
        """Return a user or a controlled not-found response."""
        try:
            user = service.get(email)
        except ValidationError as exc:
            return jsonify({"error": str(exc)}), 400
        except UserNotFoundError:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"user": user.to_dict()}), 200

    @blueprint.delete("/users/<path:email>")
    def delete_user(email: str) -> tuple[object, int] | tuple[str, int]:
        """Delete a user or return a controlled client error."""
        try:
            service.delete(email)
        except ValidationError as exc:
            return jsonify({"error": str(exc)}), 400
        except UserNotFoundError:
            return jsonify({"error": "User not found"}), 404
        return "", 204

    return blueprint
