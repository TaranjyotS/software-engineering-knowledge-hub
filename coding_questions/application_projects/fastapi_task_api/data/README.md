# Runtime Data

Running the service creates `tasks.db` in this directory unless
`TASK_DATABASE_URL` selects another database. Database files are local runtime
state and are excluded by the root `.gitignore`.

Tests use temporary databases and never modify this directory.
