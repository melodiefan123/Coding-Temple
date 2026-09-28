# test_students.py

def test_put_student_success(client, auth_headers):
    student_res = client.post("/students/", json={
        "name": "Jane Doe",
        "email": "jane@example.com",
        "grade_level": 10,
        "is_enrolled": True
    }, headers=auth_headers)
    student_id = student_res.json()["id"]

    response = client.put(f"/students/{student_id}", json={
        "name": "Jane Smith",
        "email": "janesmith@example.com",
        "grade_level": 11,
        "is_enrolled": False
    }, headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Smith"

def test_put_student_not_found(client, auth_headers):
    response = client.put("/students/99999", json={
        "name": "Ghost",
        "email": "ghost@example.com",
        "grade_level": 12,
        "is_enrolled": True
    }, headers=auth_headers)
    
    assert response.status_code == 404

def test_get_students_with_filters(client, auth_headers):
    # Create student matching filters
    client.post("/students/", json={
        "name": "Filter Test User",
        "email": "filter_user@example.com",
        "grade_level": 12,
        "is_enrolled": True
    }, headers=auth_headers)

    # Test each filter parameter (query string parameters)
    res_grade = client.get("/students/?grade_level=12", headers=auth_headers)
    assert res_grade.status_code == 200
    assert len(res_grade.json()) > 0

    res_enrolled = client.get("/students/?is_enrolled=true", headers=auth_headers)
    assert res_enrolled.status_code == 200

    res_name = client.get("/students/?name=Filter", headers=auth_headers)
    assert res_name.status_code == 200

def test_delete_enrolled_student_fails(client, auth_headers):
    # Create an enrolled student
    res = client.post("/students/", json={
        "name": "Active Student",
        "email": "active_student@example.com",
        "grade_level": 10,
        "is_enrolled": True
    }, headers=auth_headers)
    student_id = res.json()["id"]

    # Try deleting enrolled student -> expects 400 Bad Request
    delete_res = client.delete(f"/students/{student_id}", headers=auth_headers)
    assert delete_res.status_code == 400