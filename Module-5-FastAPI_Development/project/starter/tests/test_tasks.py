# project/starter/tests/test_tasks.py
# Module 5 Project — Example test (starter)

def test_health_check(client):
    """Health check returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# TODO: Add more tests:
# - test_register_user
# - test_login
# - test_create_task_authenticated
# - test_list_tasks_scoped_to_user
# - test_get_task_suggest
