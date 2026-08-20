# FastAPI Task API

## Exercise

Build a complete but compact FastAPI service for creating, listing, retrieving,
updating, and deleting tasks. Use Pydantic request/response schemas, dependency
injection, a service and repository layer, SQLAlchemy 2.x, SQLite persistence,
controlled errors, automated tests, and an application factory.

## Structure

```text
fastapi_task_api/
├── app/
│   ├── api.py          # HTTP routes and dependencies
│   ├── config.py       # Environment-based configuration
│   ├── database.py     # SQLAlchemy engine, base, and sessions
│   ├── errors.py       # Domain exceptions
│   ├── main.py         # FastAPI application factory
│   ├── models.py       # Database model
│   ├── repository.py   # Persistence operations
│   ├── schemas.py      # Pydantic API contracts
│   └── service.py      # Business operations
├── data/README.md      # Runtime database location
├── tests/test_api.py   # End-to-end API tests
├── .dockerignore
├── Dockerfile
└── requirements.txt
```

The route layer owns HTTP concerns, Pydantic owns input validation, the service
owns use-case behavior, and the repository owns database queries. This keeps
framework code from spreading into the domain and makes each boundary easier to
test or replace.

## HTTP Contract

|  Method  |     Path      | Success |     Important errors     |
| -------- | ------------- | ------- | ------------------------ |
| `GET`    | `/health`     | `200`   | —                        |
| `POST`   | `/tasks`      | `201`   | `422` invalid body       |
| `GET`    | `/tasks`      | `200`   | `422` invalid pagination |
| `GET`    | `/tasks/{id}` | `200`   | `404` unknown task       |
| `PATCH`  | `/tasks/{id}` | `200`   | `404`, `422`             |
| `DELETE` | `/tasks/{id}` | `204`   | `404` unknown task       |

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:create_app --factory --reload --port 8000
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. Open
`http://127.0.0.1:8000/docs` for the generated OpenAPI interface.

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Review API design","description":"Prepare trade-offs"}'
curl http://127.0.0.1:8000/tasks
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Docker

```bash
docker build -t fastapi-task-api .
docker run --rm -p 8000:8000 fastapi-task-api
```

Primary-key lookup, update, and delete are `O(log n)` with SQLite's index;
listing `n` selected tasks is `O(n)` in returned rows and response size.
