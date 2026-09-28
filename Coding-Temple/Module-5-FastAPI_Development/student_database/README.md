# Student Database API

A FastAPI and SQLAlchemy RESTful service for student records management with full CRUD capability and complete test documentation.

## Features
- Full CRUD operations (`POST`, `GET`, `PUT`, `PATCH`, `DELETE`)
- Input validation via Pydantic (`EmailStr`, GPA bounds `0.0` - `4.0`)
- Database enforcement using SQLAlchemy models (`nullable=False`, unique constraints)
- Error handling for missing records (`404`) and duplicate emails (`409 Conflict`) across create/update endpoints

---

## Testing Documentation (Swagger UI)

All endpoints were tested interactively using FastAPI's built-in Swagger UI documentation (`/docs`).

| Endpoint | Test Case / Intent | Input Payload / Parameters | Expected Status | Actual Output | Status |
| :--- | :--- | :--- | :---: | :--- | :---: |
| `POST /students` | Create student record | `{"name": "Alice Smith", "email": "alice@example.com", "major": "Computer Science", "gpa": 3.8}` | `201 Created` | `{"id": 1, "name": "Alice Smith", "email": "alice@example.com", "major": "Computer Science", "gpa": 3.8}` | PASSED |
| `POST /students` | Create student with duplicate email | `{"name": "Alice Duplicate", "email": "alice@example.com", "major": "Math", "gpa": 3.5}` | `409 Conflict` | `{"detail": "Email already exists"}` | PASSED |
| `GET /students` | List all students | Query Params: None | `200 OK` | Array containing student objects | PASSED |
| `GET /students` | Filter by `major` & `min_gpa` | `?major=Computer&min_gpa=3.5` | `200 OK` | Filtered array matching criteria | PASSED |
| `GET /students/{id}` | Retrieve existing student | ID: `1` | `200 OK` | `{"id": 1, "name": "Alice Smith", ...}` | PASSED |
| `GET /students/{id}` | Non-existent student ID | ID: `999` | `404 Not Found` | `{"detail": "Student not found"}` | PASSED |
| `PUT /students/{id}` | Full replacement of student | ID: `1`, `{"name": "Alice Smith", "email": "alice.smith@example.com", "major": "Data Science", "gpa": 3.9}` | `200 OK` | Record updated with all fields replaced | PASSED |
| `PUT /students/{id}` | PUT collision with existing email | ID: `2`, payload with existing email | `409 Conflict` | `{"detail": "Email already exists"}` | PASSED |
| `PATCH /students/{id}`| Partial update of GPA only | ID: `1`, `{"gpa": 4.0}` | `200 OK` | Record updated without erasing other fields | PASSED |
| `DELETE /students/{id}`| Delete existing student | ID: `1` | `200 OK` | `{"message": "Student deleted successfully"}` | PASSED |
| `DELETE /students/{id}`| Delete already deleted student | ID: `1` | `404 Not Found` | `{"detail": "Student not found"}` | PASSED |