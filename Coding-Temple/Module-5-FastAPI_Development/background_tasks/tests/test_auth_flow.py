def test_full_auth_and_protected_students_flow(client):
    # 1. Test registration
    register_res = client.post(
        "/auth/register",
        json={"email": "student_admin@example.com", "password": "securepassword123"}
    )
    assert register_res.status_code == 201
    assert register_res.json()["email"] == "student_admin@example.com"

    # 2. Test duplicate registration (409)
    dup_res = client.post(
        "/auth/register",
        json={"email": "student_admin@example.com", "password": "securepassword123"}
    )
    assert dup_res.status_code == 409

    # 3. Test failed login returns 401
    invalid_login = client.post(
        "/auth/login",
        json={"email": "student_admin@example.com", "password": "wrongpassword"}
    )
    assert invalid_login.status_code == 401

    # 4. Successful login
    login_res = client.post(
        "/auth/login",
        json={"email": "student_admin@example.com", "password": "securepassword123"}
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 5. Access /users/me
    me_res = client.get("/users/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "student_admin@example.com"

    # 6. Verify public endpoint works without token
    public_res = client.get("/students/")
    assert public_res.status_code == 200

    # 7. Access protected endpoint without token (401)
    unauth_res = client.post(
        "/students/",
        json={"name": "Alex Smith", "email": "alex@example.com", "grade_level": 10, "gpa": 3.8, "is_enrolled": True}
    )
    assert unauth_res.status_code == 401

    # 8. Create a student with token
    create_res = client.post(
        "/students/",
        json={"name": "Alex Smith", "email": "alex@example.com", "grade_level": 10, "gpa": 3.8, "is_enrolled": True},
        headers=headers
    )
    assert create_res.status_code == 201
    student_id = create_res.json()["id"]

    # 9. Patch student with token
    patch_res = client.patch(
        f"/students/{student_id}",
        json={"gpa": 3.9},
        headers=headers
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["gpa"] == 3.9

    # 10. Attempt deleting enrolled student (400) and then deleteunenrolled student with token
    client.patch(f"/students/{student_id}", json={"is_enrolled": False}, headers=headers)
    delete_res = client.delete(f"/students/{student_id}", headers=headers)
    assert delete_res.status_code == 204