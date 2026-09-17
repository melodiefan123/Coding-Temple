# project/starter/tests/test_tasks.py
# Module 5 Project — Example test (starter)

def test_health_check(client):
    """Health check returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# TODO: Add more tests:

class TestAuth: 
    # - test_register_user
    
    def test_register_user(self, auth_headers):
        client = auth_headers[1]
        response = client.post("/auth/register", json={
            "username": "test1",
            "email": "test2@email.com",
            "password": "testpassword"
        })
        assert response.status_code == 201
        assert "access_token" in response.json()
# - test_login
    def test_login(self, auth_headers):
        client = auth_headers[1]
        response = client.post("auth/token", data={
            "username": "test1@email.com",
            "password": "testpassword"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
# - test_create_task_authenticated
    def test_create_task_authenticated(self,auth_headers):
        client = auth_headers[1]
        response = client.post("/tasks", headers=auth_headers[0], json={
            "title": "Get groceries",
            "description": "Garlic, potato, tomato",
            "priority": 'medium', 
            "completed":  False, 
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Get groceries"
        assert data["description"] == "Garlic, potato, tomato"
        assert data["priority"] =="medium"
        assert data["completed"] is False
# - test_list_tasks_scoped_to_user
def test_list_tasks_scoped_to_user(auth_headers, sample_task):
    client = auth_headers[1]
    response = client.get("/tasks", headers=auth_headers[0])
    assert response.status_code ==200
    data = response.json()
    assert data[0]["title"] == "task1"
    
# - test_get_task_suggest
def test_get_task_suggest(auth_headers, sample_task):
    client = auth_headers[1]
    response = client.post(f"/tasks/{sample_task['id']}/suggest", headers=auth_headers[0], json=sample_task)
    assert response.status_code == 200
    data = response.json()
    assert data["model"] =="placeholder — AI coming in Module 7"
    
    
# - test_invalid_email
def test_invalid_password(auth_headers):
        client = auth_headers[1]
        response = client.post("auth/token", data={
            "username": "test1@email.com",
            "password": "testpassword234"
        })
        assert response.status_code == 401