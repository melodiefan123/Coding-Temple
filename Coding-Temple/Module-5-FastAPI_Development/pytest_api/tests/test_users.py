from sqlalchemy.orm import Session
from app.database import get_db

def test_get_db_returns_session():
    db_generator = get_db()

    db = next(db_generator)

    assert isinstance(db, Session)

    db_generator.close()

class TestAuth:
    def test_register_success(self, auth_headers):
        # auth_headers already registers a user, just verify the token came back
        assert "Authorization" in auth_headers[0]

    def test_login_success(self, auth_headers):
        client = auth_headers[1]
        response = client.post("/auth/login", json={
            "email": "student1@email.com",
            "password": "testpassword"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, auth_headers):
        client = auth_headers[1]
        response = client.post("/auth/login", json={
            "email": "student1@email.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401

    def test_protected_endpoint_without_token(self, auth_headers):
        client = auth_headers[1]
        response = client.get("/students")
        assert response.status_code == 401
        

class TestCreateStudent:
    """Tests for POST /students"""

    def test_create_student_success(self, auth_headers):
        client = auth_headers[1]
        response = client.post("/students", headers = auth_headers[0], json={
            "name": "student3",
            "email": "student3@email.com",
            "grade_level": 7, 
            "gpa": 3.2, 
            "is_enrolled": True
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "student3"
        assert data["email"] == "student3@email.com"
        assert data["is_enrolled"] is True

    def test_invalid_grade_level(self, auth_headers):
        client = auth_headers[1]
        response = client.post("/students",headers = auth_headers[0], json={
            "name": "student3",
            "email": "student3@email.com",
            "grade_level": 20, 
            "gpa": 3.2, 
            "is_enrolled": True})
        assert response.status_code == 422

    def test_invalid_email(self, auth_headers):
        client = auth_headers[1]
        response = client.post("/students",headers = auth_headers[0], json={"name": "student3",
            "email": "student3email",
            "grade_level": 20, 
            "gpa": 3.2, 
            "is_enrolled": True})
        assert response.status_code == 422


class TestReadStudents:
    """Tests for GET /books and GET /books/{id}"""

    def test_list_students_empty(self, auth_headers):
        client = auth_headers[1]
        response = client.get("/students", headers = auth_headers[0])
        assert response.status_code == 200
        assert response.json() == []

    def test_list_students_with_data(self, auth_headers, sample_student):
        client = auth_headers[1]
        response = client.get("/students", headers = auth_headers[0])
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_student_by_id(self, auth_headers, sample_student):
        client = auth_headers[1]
        response = client.get(f"/students/{sample_student['id']}", headers = auth_headers[0])
        assert response.status_code == 200
        assert response.json()["name"] == "student2"

    def test_get_student_not_found(self, auth_headers):
        client = auth_headers[1]
        response = client.get("/students/9999", headers = auth_headers[0])
        assert response.status_code == 404

class TestUpdateStudent:
    """Tests for PATCH /students/{id}"""

    def test_patch_student_name(self, auth_headers, sample_student):
        client = auth_headers[1]
        response = client.patch(f"/students/{sample_student['id']}", headers = auth_headers[0], json={"name": "student4"})
        assert response.status_code == 200
        assert response.json()["name"] == "student4"
        assert response.json()["email"] == "student2@email.com"  # Unchanged

    def test_patch_nonexistent_student(self, auth_headers):
        client = auth_headers[1]
        response = client.patch("/students/9999", headers = auth_headers[0], json={"name": "student10"})
        assert response.status_code == 404

class TestDeleteStudent:
    """Tests for DELETE /students/{id}"""

    def test_delete_student(self, auth_headers, sample_student):
        client = auth_headers[1]

        response = client.delete(f"/students/{sample_student['id']}", headers = auth_headers[0])
        assert response.status_code == 204
        # Verify it's gone
        response = client.get(f"/students/{sample_student['id']}", headers = auth_headers[0])
        assert response.status_code == 404

    def test_delete_nonexistent_student(self, auth_headers):
        client = auth_headers[1]
        response = client.delete("/students/9999",headers = auth_headers[0] )
        assert response.status_code == 404