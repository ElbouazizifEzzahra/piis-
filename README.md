# PIIS

PIIS is currently set up as a backend-first project with Dockerized local development.
At this stage, the implemented part is the FastAPI backend with authentication and a PostgreSQL database.

## What has been built so far

### 1) Backend API foundation (FastAPI)
- App entrypoint: `backend/app/main.py`
- API versioning under `/api/v1`
- Root health route: `GET /`
- Interactive API docs: `http://localhost:8000/docs`

### 2) Authentication module
- Route group: `/api/v1/auth`
- `POST /api/v1/auth/register`
  - Registers a new user
  - Prevents duplicate `cin`
  - Prevents duplicate `tel` when provided
  - Returns JWT access token on success
- `POST /api/v1/auth/login`
  - Accepts `identifier` (either `cin` or `tel`) + `password`
  - Returns JWT access token on success

### 3) User domain model (SQLModel + PostgreSQL)
- User fields include:
  - UUID primary key
  - `cin`, optional `tel`, optional `email`
  - `full_name`, `account_status`
  - `hashed_password`, `created_at`, `last_login`
- Tables are auto-created on app startup.

### 4) Security
- Password hashing with `passlib` + `bcrypt`
- JWT token generation with `python-jose`
- Config-driven secret key, algorithm, and token expiry

### 5) Automated tests
- Test file: `backend/tests/test_auth.py`
- Covers:
  - Successful registration
  - Duplicate CIN rejection
  - Login with CIN
  - Login with telephone number
  - Login failure with wrong password
- Uses an in-memory SQLite DB for test isolation.

### 6) Dockerized development setup
- `docker-compose.yml` defines:
  - `backend` service (FastAPI on port `8000`)
  - `db` service (PostgreSQL 15 on host port `5433`)
- Persistent Postgres data via Docker volume: `postgres_data`

### 7) Project scope status
- `mobile/` and `web/` folders exist but are currently empty.
- Active implementation work is in `backend/`.

## Run from scratch with Docker (after cloning)

### Prerequisites
- Git
- Docker Desktop (or Docker Engine + Compose plugin)

### 1) Clone the repository
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd PIIS
```

### 2) Create backend environment file
Copy the example file and then adjust values if needed:

```bash
cp backend/.env.example backend/.env
```

Notes:
- `backend/.env.example` is safe to commit and document defaults/placeholders.
- `backend/.env` is ignored by git via `.gitignore` to prevent accidental secret commits.
- Replace placeholder secrets before any production deployment.

### 3) Build and start services
From the project root:

```bash
docker compose up --build
```

This starts:
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5433`

### 4) Verify the API quickly
Check root endpoint:

```bash
curl http://localhost:8000/
```

Expected response:

```json
{"message":"Welcome to  PIIS Backend"}
```

Register a user:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "cin": "AB123456",
    "tel": "0612345678",
    "email": "user@example.com",
    "full_name": "Test User",
    "password": "strongpassword123"
  }'
```

Login with CIN:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "identifier": "AB123456",
    "password": "strongpassword123"
  }'
```

### 5) Run backend tests in Docker
In a new terminal:

```bash
docker compose exec backend pytest -q
```

### 6) Stop containers
Stop while keeping DB data:

```bash
docker compose down
```

Stop and remove DB volume (full reset):

```bash
docker compose down -v
```

## Useful Docker commands

View running services:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f backend
docker compose logs -f db
```

Rebuild backend only:

```bash
docker compose build backend
docker compose up
```

## Current architecture (high level)
- FastAPI app handles HTTP requests.
- SQLModel handles ORM and schema-to-table mapping.
- PostgreSQL is the persistence layer.
- JWT is used for stateless auth tokens.
- Docker Compose orchestrates backend + database locally.
