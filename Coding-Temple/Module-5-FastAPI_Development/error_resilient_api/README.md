# Student Management API (Error-Resilient)

A FastAPI application demonstrating custom exception classes, domain-level validation, and centralized exception handlers for resilient API error handling.

## Features

- **Custom Exception Classes**: Centralized domain error types (`NotFoundError`, `DuplicateError`, `AppValidationError`).
- **Standardized Error Formatting**: Consistent error response payloads across all failure scenarios.
- **Robust Database Integrity**: Gracefully catches database `IntegrityError` during creation and updates (PUT/PATCH).
- **Domain Logic Validation**: Enforces custom business logic (e.g., preventing deletion of enrolled students).

## Project Structure

```text
.
├── app/
│   ├── exceptions.py       # Custom exception classes and global handlers
│   ├── main.py             # FastAPI entry point & handler registrations
│   ├── database.py         # SQLAlchemy database connection setup
│   ├── config.py           # Application configuration settings
│   ├── models/             # SQLAlchemy ORM models
│   ├── schemas/            # Pydantic models for validation
│   └── routers/            # API endpoints (students)
├── tests/
│   └── test_students.py    # Unit & integration tests
├── requirements.txt        # Project dependencies
└── README.md
```

## Standardized Error Response Format

All custom exceptions output a consistent JSON payload format:

```json
{
  "error": "Not Found",
  "message": "Student with id 999 not found",
  "status_code": 404
}
```

### Handled Status Codes

| Exception | HTTP Status Code | Description |
| :--- | :--- | :--- |
| `NotFoundError` | `404 Not Found` | Raised when a requested resource does not exist. |
| `DuplicateError` | `409 Conflict` | Raised when unique constraint violations occur (e.g., duplicate email). |
| `AppValidationError` | `422 Unprocessable Entity` | Raised for domain-level business rule failures. |

---

## Setup & Running the Application

### 1. Install Dependencies

Ensure Python 3.10+ is installed, then run:

```bash
pip install -r requirements.txt
```

### 2. Start the Server

Start the application with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API server will be available at `http://127.0.0.1:8000`.

### 3. Interactive Documentation (Swagger UI)

Explore and test endpoints in your browser:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Running Tests

To run the full test suite verifying error responses and status codes:

```bash
pytest
```