"""Privacy-safe JSON and CSV loaders for the hotel exercise."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import HotelInventory, Reservation, parse_datetime

REQUIRED_COLUMNS = {
    "reservation_id",
    "room_id",
    "hotel_id",
    "guest_name",
    "arrival_date",
    "nights",
    "room_count",
}


def load_hotel_information(path: str | Path, *, hotel_id: str) -> HotelInventory:
    """Load room inventory and associate it with the reservation hotel ID."""
    with Path(path).open(encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError("Hotel information must be a JSON object")

    inventory = payload.get("inventory")
    if not hotel_id.strip():
        raise ValueError("Hotel ID must be non-empty")
    if not isinstance(inventory, dict) or not inventory:
        raise ValueError("Hotel information requires a non-empty inventory object")
    return HotelInventory(
        hotel_id=hotel_id.strip(),
        rooms={str(room_type): int(count) for room_type, count in inventory.items()},
    )


def load_reservations(path: str | Path) -> list[Reservation]:
    """Load complete reservation records from the submitted CSV schema."""
    reservations: list[Reservation] = []
    with Path(path).open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - fieldnames
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Reservation CSV is missing columns: {missing}")

        for row_number, row in enumerate(reader, start=2):
            try:
                reservations.append(
                    Reservation(
                        reservation_id=row["reservation_id"].strip(),
                        room_type=row["room_id"].strip(),
                        hotel_id=row["hotel_id"].strip(),
                        guest_name=row["guest_name"].strip(),
                        arrival=parse_datetime(row["arrival_date"]),
                        nights=int(row["nights"]),
                        room_count=int(row["room_count"]),
                    )
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"Invalid reservation CSV row {row_number}") from exc
    return reservations
