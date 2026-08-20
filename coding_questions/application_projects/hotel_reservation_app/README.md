# Hotel Reservation Availability Application

## Exercise

Given hotel room inventory and existing reservations, build a Flask API that
retrieves reservations and reports room availability during a selected stay.
Check-in is 3:00 PM on the arrival date and check-out is noon after the booked
number of nights.

The key algorithm must calculate **peak concurrent demand**. Summing every
reservation that overlaps any portion of a multi-day window is incorrect because
those stays may occur at different times. This implementation clips overlapping
half-open intervals and processes their check-in/check-out events with a sweep
line.

## Structure

```text
hotel_reservation_app/
├── app/
│   ├── __init__.py       # Application factory
│   ├── data_loader.py    # JSON and CSV parsing
│   ├── errors.py         # Domain errors and HTTP handlers
│   ├── models.py         # Reservation and report models
│   ├── reservation.py    # Availability service and sweep-line algorithm
│   ├── routes.py         # Flask blueprint
│   └── utils.py          # Dataset-level validation helpers
├── data/
│   ├── hotel_information.json
│   └── reservations.csv  # Complete submitted reservation dataset
├── tests/
│   ├── test_api.py
│   └── test_reservation.py
├── requirements.txt
└── run.py
```

The submitted data files are retained without reducing the inventory or row
count. The CSV contains 5,139 reservations and includes the original
`guest_name` field. The loader preserves that field and the reservation endpoint
returns it, matching the source exercise. Before publishing this repository,
confirm that the dataset is approved for public distribution.

The availability implementation corrects two issues in the submitted logic:

- Check-in is set to 3:00 PM instead of adding 15 hours to an arrival timestamp
  that may already contain a time.
- Capacity is compared with peak concurrent demand. Summing every reservation
  that overlaps any portion of a multi-day stay can overcount stays that occur
  at different times.

## HTTP Contract

| Method |               Path                |                      Result                       |
| ------ | --------------------------------- | ------------------------------------------------- |
| `GET`  | `/health`                         | Service health                                    |
| `GET`  | `/inventory`                      | Hotel inventory                                   |
| `GET`  | `/reservations/<id>`              | One reservation or `404`                          |
| `GET`  | `/reservations/<id>/availability` | Peak demand, remaining rooms, and conflict status |
| `GET`  | `/reservation/<id>`               | Original reservation-route compatibility alias    |
| `GET`  | `/availability/<id>`              | Original availability-route compatibility alias   |

## Run and Test

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python run.py
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. Try:

```bash
curl http://127.0.0.1:5001/reservations/3baf3d03-ce98-429e-a692-17dcbec4f3dd/availability
```

For `r` reservations and `t` room types, this readable in-memory solution is
`O(t × r log r)` time and `O(r + t)` auxiliary space. A production design would
query indexed reservation ranges and protect allocation with transactions.
