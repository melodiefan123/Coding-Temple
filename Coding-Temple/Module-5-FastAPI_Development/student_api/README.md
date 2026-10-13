# FastAPI JWT Authentication & Student Management API

A standalone, secure FastAPI application implementing JWT-based authentication along with public and protected RESTful endpoints for student management.

---

## 🚀 Features

- **JWT Authentication System**:
  - `POST /auth/register`: User registration with duplicate email checks and password hashing.
  - `POST /auth/login`: Issue signed Bearer JWTs upon credential verification.
  - `GET /users/me`: Protected user profile endpoint.
- **Student Management API**:
  - **Public Endpoints**: `GET /students`, `GET /students/{id}`
  - **Protected Endpoints**: `POST /students`, `PUT /students/{id}`, `PATCH /students/{id}`, `DELETE /students/{id}`
- **Security & Best Practices**:
  - Pinned `bcrypt` versioning compatible with `passlib`.
  - Secret key configuration pulled dynamically from `.env`.
  - Swagger UI integrated with HTTPBearer for testing auth lock icons directly in interactive docs.

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

> **Note:** Ensure `.env` is listed in your `.gitignore` file so secret keys are never committed to version control.

---

## 🏃 Running the Application

Start the local Uvicorn development server:

```bash
uvicorn app.main:app --reload
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

The test suite uses an isolated in-memory SQLite database (`StaticPool`) to ensure your development database (`test.db`) remains untouched.

Run all unit and integration tests with `pytest`:

```bash
pytest
```