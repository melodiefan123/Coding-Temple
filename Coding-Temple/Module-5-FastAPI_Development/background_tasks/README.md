# FastAPI JWT Authentication & Student Management API

A standalone, secure FastAPI application implementing JWT-based authentication along with background task processing for reports, student notifications, and activity logging.

---

## 🚀 Features

- **JWT Authentication System**:
  - `POST /auth/register`: User registration with duplicate email checks and password hashing.
  - `POST /auth/login`: Issue signed Bearer JWTs upon credential verification.
  - `GET /users/me`: Protected user profile endpoint.
- **Student Management API**:
  - **Public Endpoints**: `GET /students`, `GET /students/{id}`
  - **Protected Endpoints**: `POST /students`, `PUT /students/{id}`, `PATCH /students/{id}`, `DELETE /students/{id}`
- **Background Tasks**:
  - Asynchronous report generation (`POST /reports`) with state tracking (`pending` -> `processing` -> `complete`).
  - Offloaded student creation/deletion notifications and activity logging via FastAPI's `BackgroundTasks`.

---

## ⚡ Background Tasks & Response Timing

Starlette's `TestClient` intentionally waits for background tasks to complete before returning responses during unit tests. To measure real-world endpoint latency, test requests directly against a live Uvicorn server using `curl`:

### 1. Immediate Response (`POST /reports`)
```bash
curl -w "\nTime Total: %{time_total}s\n" -X POST "http://127.0.0.1:8000/reports" \
     -H "Content-Type: application/json" \
     -d '{"report_type": "sales", "rows": 100}'
```
**Output:**
```json
{"report_id": "8f3b2a1c-93a8-42f1-bc8d-0e42a98e3b5e", "status": "pending"}
Time Total: 0.015s
```
*(The endpoint returns in ~15ms while background processing runs asynchronously for 2 seconds)*

### 2. Polling Status (`GET /reports/{report_id}`)
- **Immediate check** (t = 0.2s): `{"id": "...", "status": "processing", "result": null}`
- **After background work completes** (t = 2.1s): `{"id": "...", "status": "complete", "result": {"summary": "Generated sales report with 100 rows."}}`

---

## 🛠️ Setup & Installation

### 1. Clone & Setup Environment
```bash
git clone <your-repository-url>
cd <your-repository-folder>
python -m venv venv
```

Activate the virtual environment:
- **macOS/Linux**: `source venv/bin/activate`
- **Windows**: `venv\Scripts\activate`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a `.env` file in the project root directory:

```env
SECRET_KEY=super_secret_jwt_key_for_development_123456
APP_NAME="Student Management API"
DEBUG=True
```

---

## 🏃 Running the Application

Start the local Uvicorn development server:

```bash
uvicorn main:app --reload
```

- **API Root**: `http://127.0.0.1:8000/`
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`

---

## 🔒 Authentication Workflow

1. **Register**: Send a `POST` request to `/auth/register` with an `email` and `password`.
2. **Log In**: Send a `POST` request to `/auth/login` with your credentials to retrieve an `access_token`.
3. **Authorize in Swagger**:
   - Click the **Authorize 🔓** button at the top right of the `/docs` page.
   - Paste your token into the **Value** box and authorize.
4. **Access Protected Endpoints**: Test endpoints like `GET /users/me` or `POST /students` with valid Bearer authorization.

---

## 🧪 Running Tests

The test suite uses an isolated in-memory SQLite database (`StaticPool`) via `conftest.py` so your development database (`test.db`) remains completely untouched.

Run all unit and integration tests with `pytest`:

```bash
pytest
```