# Module 4 Project — Part 2: Study Tracker

**Melodie Fan**  
**Date: 05/07/2026**

---

## The App: Study Tracker

Study Tracker is an academic productivity application designed to help students manage their coursework, log daily study sessions, set target weekly goals, and analyze their overall learning progress. Students can organize study time by course, track time spent on specific tasks, and evaluate goal completion over time.

---

# API Information

| Field | Value |
|---|---|
| API Name | Study Tracker API |
| Version | v1 |
| Base URL | `https://api.studytracker.com/v1` |
| Authentication | Bearer Token (JWT) |
| Rate Limit | 60 requests per minute |

---

## Section 1 — Resources

| Resource | Key Attributes |
|----------|---------------|
| Users | id, username, email, password_hash, created_at |
| Courses | id, user_id, course_code, course_name, color_code, created_at |
| StudySessions | id, user_id, course_id, duration_minutes, notes, session_date, created_at |
| Goals | id, user_id, course_id, target_hours, start_date, end_date, is_completed |

---

## Section 2 — Relationships

Describe how your resources relate to each other:

- **User ↔ Courses**  
  A user can create and manage multiple courses (one-to-many). One course belongs to exactly one user.

- **Course ↔ StudySessions**  
  A course can have many study sessions logged under it over time (one-to-many). One study session belongs to one specific course.

- **User ↔ StudySessions**  
  A user can log many study sessions (one-to-many).

- **Course ↔ Goals**  
  A course can have multiple target goals set across different weeks (one-to-many). One goal belongs to one specific course.

- **User ↔ Goals**  
  A user can establish many weekly or monthly study goals (one-to-many).

---

## Section 3 — Endpoints

| Method | URI | Description | Auth Required? |
|--------|-----|-------------|----------------|
| POST | /auth/register | Register a new student account | No |
| POST | /auth/login | Authenticate user and receive JWT token | No |
| GET | /users/me | Get current user profile details | Yes |
| GET | /courses | List all courses for the authenticated user | Yes |
| POST | /courses | Create a new course | Yes |
| GET | /courses/{id} | Get specific course details | Yes |
| PUT | /courses/{id} | Update an existing course | Yes |
| DELETE | /courses/{id} | Delete a course | Yes |
| GET | /sessions | List all logged study sessions | Yes |
| POST | /sessions | Log a new study session | Yes |
| GET | /sessions/{id} | Get details of a specific study session | Yes |
| PUT | /sessions/{id} | Update a study session entry | Yes |
| DELETE | /sessions/{id} | Remove a study session entry | Yes |
| GET | /sessions?course_id={id}&start_date={date} | Filter study sessions by course or date range | Yes |
| GET | /goals | List all study goals | Yes |
| POST | /goals | Set a new study goal | Yes |
| GET | /goals/{id} | Get details for a specific goal | Yes |
| PUT | /goals/{id} | Update goal target or status | Yes |
| DELETE | /goals/{id} | Delete a goal | Yes |

---

## Section 4 — Request/Response Schemas

### 1. POST /sessions — Log a New Study Session

**Request Body:**
```json
{
  "course_id": "integer (required) - ID of the associated course",
  "duration_minutes": "integer (required) - Duration of the study session in minutes",
  "notes": "string (optional) - Summary or topics covered during the session",
  "session_date": "datetime (required) - Date and time session occurred (ISO 8601 standard, e.g. '2026-05-07T14:30:00Z')"
}
```

**Example Request**
```json
{
  "course_id": 4,
  "duration_minutes": 90,
  "notes": "Reviewed REST API design patterns and HTTP status codes",
  "session_date": "2026-05-07T14:30:00Z"
}
```

**Success Response (201 Created):**
```json
{
  "id": "integer - Auto-generated unique session ID",
  "user_id": "integer - ID of the student who logged the session",
  "course_id": "integer - ID of the course",
  "duration_minutes": "integer - Duration of study session",
  "notes": "string - Notes recorded",
  "session_date": "datetime - Date session occurred",
  "created_at": "datetime - Timestamp record was generated"
}
```

**Example Response**
```json
{
  "id": 101,
  "user_id": 12,
  "course_id": 4,
  "duration_minutes": 90,
  "notes": "Reviewed REST API design patterns and HTTP status codes",
  "session_date": "2026-05-07T14:30:00Z",
  "created_at": "2026-05-07T16:00:00Z"
}
```

### 2. POST /goals — Set a New Study Goal
**Request Body:**
```json
{
  "course_id": "integer (required) - ID of the associated course",
  "target_hours": "float (required) - Target study hours targeted for period",
  "start_date": "string (required) - Start date formatted YYYY-MM-DD",
  "end_date": "string (required) - End date formatted YYYY-MM-DD"
}
```

**Example Request**
```json
{
  "course_id": 4,
  "target_hours": 10.5,
  "start_date": "2026-05-10",
  "end_date": "2026-05-17"
}
```

**Success Response (201 Created):**
```json
{
  "id": "integer - Unique goal ID",
  "user_id": "integer - User ID of owner",
  "course_id": "integer - Associated course ID",
  "target_hours": "float - Target study hours",
  "start_date": "string - Period start date",
  "end_date": "string - Period end date",
  "is_completed": "boolean - Status indicator whether target hours were hit"
}
```

### 3. GET /sessions/{id} — Retrieve Specific Study Session Details

**Success Response(200 OK)**
```json
{
  "id": "integer - Session ID",
  "user_id": "integer - Owner user ID",
  "course_id": "integer - Associated course ID",
  "duration_minutes": "integer - Session length in minutes",
  "notes": "string - Session notes",
  "session_date": "datetime - ISO 8601 timestamp",
  "created_at": "datetime - Creation timestamp"
}
```

### 4. GET /goals/{id} — Retrieve Specific Goal Details

**Success Response(200 OK)**
```json
{
  "id": "integer - Goal ID",
  "user_id": "integer - Owner user ID",
  "course_id": "integer - Associated course ID",
  "target_hours": "float - Target hours required",
  "start_date": "string - Target period start date",
  "end_date": "string - Target period end date",
  "is_completed": "boolean - Completion flag"
}
```

---

## Section 5 — Authentication

| Endpoint | Auth Required | Access / Ownership Rule |
| --- | --- | --- |
| POST /auth/register | No | Public endpoint for creating account |
| POST /auth/login | No | Public endpoint to retrieve token |
| GET /courses | Yes | Only retrieves courses owned by authenticated user |
| POST /courses | Yes | Any authenticated user |
| GET /courses/{id} | Yes | Authenticated user (must own resource) |
| PUT /courses/{id} | Yes | Authenticated user (must own resource) |
| DELETE /courses/{id} | Yes | Authenticated user (must own resource) |
| GET /sessions | Yes | Authenticated user (returns user's sessions) |
| POST /sessions | Yes | Authenticated user |
| GET /sessions/{id} | Yes | Authenticated user (must own session) |
| PUT /sessions/{id} | Yes | Authenticated user (must own session) |
| DELETE /sessions/{id} | Yes | Authenticated user (must own session) |
| GET /goals | Yes | Authenticated user |
| POST /goals | Yes | Authenticated user |

**Auth Method and Rationale:**  
This API utilizes **JWT (JSON Web Tokens)** carried within the `Authorization: Bearer <token>` header. This ensures stateless session handling, which allows the server to scale efficiently without storing session states in memory. Public endpoints (`/auth/register`, `/auth/login`) do not require tokens, whereas all resource operations verify the JWT claim to guarantee students can only access or modify their own courses, sessions, and goals.

---


## Section 6 — Error Responses for POST /sessions

| Status Code | Reason / Meaning | Trigger Scenario |
| ----------- | ---------------- | ---------------- |
| 201 Created | Created | Session was successfully created and logged. |
| 400 Bad Request | Bad Request | Request payload missing required fields (e.g., `duration_minutes` or `course_id`). |
| 401 Unauthorized | Unauthorized | Request is missing an `Authorization` header or the JWT token is expired/invalid. |
| 403 Forbidden | Forbidden | Authenticated user attempted to log a session for a course owned by another user. |
| 404 Not Found | Not Found | The specified `course_id` in the request body does not exist in the database. |
| 409 Conflict | Conflict | A duplicate session entry already exists for the exact same timestamp and course. |
| 422 Unprocessable Entity | Unprocessable Content | Invalid data types or semantically invalid values provided (e.g., negative duration, or a future timestamp). |
| 500 Internal Server Error | Internal Server Error | An unexpected server failure occurred while saving the session record. |