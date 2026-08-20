"""End-to-end API tests for the FastAPI task service."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.config import Settings
from app.main import create_app
from fastapi.testclient import TestClient


class TaskApiTests(unittest.TestCase):
    """Exercise the API against one isolated SQLite database per test."""

    def setUp(self) -> None:
        """Create and start a temporary application through its lifespan."""
        self.temporary_directory = tempfile.TemporaryDirectory()
        database_path = (Path(self.temporary_directory.name) / "tasks.db").as_posix()
        application = create_app(Settings(database_url=f"sqlite:///{database_path}"))
        self.client_context = TestClient(application)
        self.client = self.client_context.__enter__()

    def tearDown(self) -> None:
        """Close HTTP/database resources before removing temporary files."""
        self.client_context.__exit__(None, None, None)
        self.temporary_directory.cleanup()

    def test_health_and_openapi_contract(self) -> None:
        """Expose operational health and generated API documentation."""
        self.assertEqual(self.client.get("/health").json(), {"status": "ok"})
        schema = self.client.get("/openapi.json")
        self.assertEqual(schema.status_code, 200)
        self.assertIn("/tasks", schema.json()["paths"])

    def test_task_lifecycle(self) -> None:
        """Create, read, update, list, and delete one task."""
        created = self.client.post(
            "/tasks",
            json={"title": "Review API design", "description": "Prepare trade-offs"},
        )
        self.assertEqual(created.status_code, 201)
        task_id = created.json()["id"]
        self.assertFalse(created.json()["completed"])

        self.assertEqual(self.client.get(f"/tasks/{task_id}").status_code, 200)
        updated = self.client.patch(
            f"/tasks/{task_id}",
            json={"completed": True},
        )
        self.assertTrue(updated.json()["completed"])
        self.assertEqual(len(self.client.get("/tasks").json()), 1)

        self.assertEqual(self.client.delete(f"/tasks/{task_id}").status_code, 204)
        self.assertEqual(self.client.get(f"/tasks/{task_id}").status_code, 404)

    def test_validation_and_missing_task(self) -> None:
        """Reject invalid schemas and return a stable missing-resource response."""
        invalid = self.client.post("/tasks", json={"title": "", "owner": "unexpected"})
        self.assertEqual(invalid.status_code, 422)

        created = self.client.post("/tasks", json={"title": "Valid task"})
        task_id = created.json()["id"]
        self.assertEqual(
            self.client.patch(f"/tasks/{task_id}", json={"title": None}).status_code,
            422,
        )
        self.assertEqual(
            self.client.patch(f"/tasks/{task_id}", json={"completed": None}).status_code,
            422,
        )

        missing = self.client.get("/tasks/999")
        self.assertEqual(missing.status_code, 404)
        self.assertEqual(missing.json()["detail"], "Task 999 was not found")

    def test_pagination_limits_are_validated(self) -> None:
        """Reject negative offsets and unbounded page sizes."""
        self.assertEqual(self.client.get("/tasks?offset=-1").status_code, 422)
        self.assertEqual(self.client.get("/tasks?limit=101").status_code, 422)


if __name__ == "__main__":
    unittest.main()
