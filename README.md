# TestWarden

An agent that generates unit tests for Python repositories. It parses code into functions, mines git history for risk signals, measures coverage, then loops: generate a test, run it in a Docker sandbox, repair on failure (capped attempts), and record results in PostgreSQL.

## Structure

- `backend/app/ingestion` parse source into functions (tree-sitter)
- `backend/app/mining` git history and risk signals
- `backend/app/coverage` coverage.py integration
- `backend/app/agent` LLM generate/repair loop
- `backend/app/sandbox` Docker execution (no network, non-root, 512 MB, 60 s)
- `backend/app/db` PostgreSQL models and sessions
- `docker/sandbox.Dockerfile` image the generated tests run in
- `frontend/` dashboard placeholder

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d db
```

Run the backend from `backend/` in a separate terminal:

```bash
cd backend
uvicorn app.main:app --reload
```

Run the tests from `backend/`:

```bash
cd backend
pytest
```

Run Ruff from the repository root, matching CI:

```bash
ruff check backend
```

The PostgreSQL credentials in `docker-compose.yml` are development defaults for local use only. Do not use them with real data. The database port is bound to `127.0.0.1` and is intended to be accessible only from the local machine.

## Workflow

- `main` is protected: work on `feature/*` branches and open a pull request.
- CI runs ruff and pytest on every PR.
- Use only public or synthetic repos and sanitized snippets with free-tier LLM APIs. Never send private code or secrets.
