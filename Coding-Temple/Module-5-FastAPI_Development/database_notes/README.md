# Database-Backed Notes API

A FastAPI application featuring persistent SQLite storage using SQLAlchemy models and data validation via Pydantic.

## Features
- **Persistent Storage**: Data is persisted locally to an SQLite database (`test.db`).
- **RESTful Endpoints**: Perform full CRUD operations on notes with proper HTTP status codes.
- **Filtering**: Filter notes list by optional `category` and `is_pinned` state.
- **Database Integrity**: Proper ORM column constraints (`nullable=False`) mirroring schema validation.

---

## Installation & Setup

1. **Clone the repository and navigate to project root**:
   ```bash
   cd database_notes
   ```

2. **Create and activate a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Interactive Documentation**:
   Open `http://127.0.0.1:8000/docs` in your browser to test endpoints interactively via Swagger UI.

---

## API Endpoints

| Method | Endpoint | Status Code | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/notes` | `201 Created` | Create a new note |
| `GET` | `/notes` | `200 OK` | List notes (Query params: `category`, `is_pinned`) |
| `GET` | `/notes/{note_id}` | `200 OK` | Retrieve a specific note by ID |
| `DELETE` | `/notes/{note_id}` | `204 No Content` | Delete a note by ID |

---

## Data Model & Schema Details

### Note Model (`notes` table)
- `id` (Integer, Primary Key)
- `title` (String 200, Required, Indexed)
- `content` (Text/String, Required)
- `category` (String 50, Optional, Indexed)
- `is_pinned` (Boolean, Default `False`)
- `created_at` (DateTime, Default Server Timestamp)

---

## Verification of Persistence

To verify SQLite database persistence across application restarts, perform the following steps:

### 1. Start the Server
```bash
uvicorn main:app --reload
```

### 2. Create a Note (`POST /notes`)
**Request**:
`POST http://127.0.0.1:8000/notes`

**Headers**:
`Content-Type: application/json`

**Body**:
```json
{
  "title": "Persistent Note Test",
  "content": "Verifying that this note survives a server restart.",
  "category": "Testing",
  "is_pinned": true
}
```

**Response (`201 Created`)**:
```json
{
  "id": 1,
  "title": "Persistent Note Test",
  "content": "Verifying that this note survives a server restart.",
  "category": "Testing",
  "is_pinned": true,
  "created_at": "2026-09-27T22:00:00"
}
```

### 3. Verify Initial State (`GET /notes`)
**Request**:
`GET http://127.0.0.1:8000/notes`

**Response (`200 OK`)**:
```json
[
  {
    "id": 1,
    "title": "Persistent Note Test",
    "content": "Verifying that this note survives a server restart.",
    "category": "Testing",
    "is_pinned": true,
    "created_at": "2026-09-27T22:00:00"
  }
]
```

### 4. Restart the Application
1. Stop the Uvicorn process using `CTRL + C` in the terminal.
2. Verify that `test.db` exists in the project root directory.
3. Relaunch the server:
   ```bash
   uvicorn main:app --reload
   ```

### 5. Confirm Persistence (`GET /notes`)
**Request**:
`GET http://127.0.0.1:8000/notes`

**Response (`200 OK`)**:
```json
[
  {
    "id": 1,
    "title": "Persistent Note Test",
    "content": "Verifying that this note survives a server restart.",
    "category": "Testing",
    "is_pinned": true,
    "created_at": "2026-09-27T22:00:00"
  }
]
```

**Observation**: Note ID `1` remains intact in the SQLite database after stopping and restarting the Uvicorn server, confirming persistent storage functioning as designed.