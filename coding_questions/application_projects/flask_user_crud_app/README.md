# Flask User CRUD Application

## Exercise

Build a Flask API that creates, lists, retrieves, and deletes users. Validate
untrusted JSON, normalize email addresses, reject duplicate users, persist data
in SQLite, and keep request handlers separate from business and data-access
logic.

## Structure

```text
flask_user_crud_app/
├── app/
│   ├── __init__.py       # Application factory
│   ├── errors.py         # Domain exceptions
│   ├── models.py         # User value object
│   ├── repository.py     # SQLite persistence
│   ├── routes.py         # HTTP adapter
│   └── service.py        # Validation and business rules
├── data/README.md        # Runtime database location
├── tests/test_api.py     # Service and HTTP contract tests
├── requirements.txt
└── run.py
```

The application factory accepts a database path, so each test receives an
isolated database. Route handlers do not manipulate SQL directly; they delegate
to a service that owns validation and calls the repository.

## HTTP Contract

|  Method  |       Path       | Success |               Important errors               |
| -------- | ---------------- | ------- | -------------------------------------------- |
| `GET`    | `/health`        | `200`   | —                                            |
| `POST`   | `/users`         | `201`   | `400` invalid payload, `409` duplicate email |
| `GET`    | `/users`         | `200`   | —                                            |
| `GET`    | `/users/<email>` | `200`   | `404` unknown email                          |
| `DELETE` | `/users/<email>` | `204`   | `404` unknown email                          |

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. The API
starts at `http://127.0.0.1:5000`.

```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alex Doe","email":"alex@example.com"}'
curl http://127.0.0.1:5000/users
```

## Test

```bash
python -m unittest discover -s tests -v
```

Create and lookup are `O(1)` average through SQLite's unique email index;
listing `n` users is `O(n)` in response size.
