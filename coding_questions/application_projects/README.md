# Application Projects

This directory contains complete, runnable backend exercises. Unlike the
single-file questions in the parent directory, each project demonstrates an
application boundary: configuration, routes, validation, domain logic, data
access, error handling, and automated tests.

## Projects

|                      Project                      | Framework |    Persistence or data    |                        Main exercise                        |
| ------------------------------------------------- | --------- | ------------------------- | ----------------------------------------------------------- |
| [`flask_user_crud_app`](flask_user_crud_app/)     | Flask     | SQLite                    | Build a validated user CRUD API with an application factory |
| [`hotel_reservation_app`](hotel_reservation_app/) | Flask     | JSON and CSV              | Calculate hotel availability across overlapping stays       |
| [`fastapi_task_api`](fastapi_task_api/)           | FastAPI   | SQLite through SQLAlchemy | Build and test a typed task CRUD service                    |

Each project has isolated dependencies and setup instructions. Create a virtual
environment inside the selected project, install its `requirements.txt`, and
run its test command before starting the API.

Generated databases, caches, virtual environments, and secrets must not be
committed. Review the provenance, licensing, and privacy requirements of any
included exercise dataset before publishing or reusing it.
