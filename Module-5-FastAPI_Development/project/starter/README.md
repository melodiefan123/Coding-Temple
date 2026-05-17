# Module 5 Project — AI-Ready Task Manager API

## Project overview

Build a production-quality task management REST API with:
- JWT authentication (register, login, protected endpoints)
- Task CRUD scoped to the authenticated user
- A `/tasks/{id}/suggest` placeholder endpoint for AI integration
- SQLAlchemy database with user-task relationship
- Custom error handling
- CORS configuration
- Passing pytest test suite

## Setup

```bash
# From this folder (project/starter/)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
pip install -r requirements.txt
cp .env.example .env            # edit SECRET_KEY before production use

uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

## Running tests

```bash
pytest tests/ -v
```

## Project structure

```
app/
├── main.py          — FastAPI app with CORS
├── database.py      — SQLAlchemy engine + get_db
├── auth.py          — JWT utilities
├── models/
│   ├── user.py      — User ORM model
│   └── task.py      — Task ORM model (FK to User)
├── schemas/
│   ├── user.py      — UserCreate, UserResponse, TokenResponse
│   └── task.py      — TaskCreate, TaskPatch, TaskResponse
└── routers/
    ├── auth.py      — /auth/register, /auth/token, /auth/me
    └── tasks.py     — /tasks CRUD + /tasks/{id}/suggest
tests/
├── conftest.py      — test DB fixture
└── test_tasks.py    — test cases
```

## Implementation checklist

- [ ] database.py — create_engine, SessionLocal, get_db
- [ ] models/user.py — User model with tasks relationship
- [ ] models/task.py — Task model with owner_id FK
- [ ] schemas/user.py — UserCreate, UserResponse, TokenResponse
- [ ] schemas/task.py — TaskCreate, TaskPatch, TaskResponse
- [ ] auth.py — hash_password, verify_password, create_access_token, get_current_user
- [ ] routers/auth.py — register, login, me
- [ ] routers/tasks.py — CRUD + suggest endpoint
- [ ] main.py — wire everything together
- [ ] tests/conftest.py — test DB override
- [ ] tests/test_tasks.py — 5+ passing tests
