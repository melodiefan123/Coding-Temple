"""
Module 6 Project — AI Dashboard  (STARTER)
API Client
============
Centralised functions for all backend communication.

All API calls should go through these functions so that:
    • The Authorization header is added in one place
    • Error handling is consistent
    • The rest of the app stays clean

Functions to implement:
    login(username, password)   → (token: str | None, error: str | None)
    get_tasks(token)            → (tasks: list | None, error: str | None)
    create_task(token, title)   → (task: dict | None, error: str | None)
    complete_task(token, task_id) → (task: dict | None, error: str | None)
"""

import requests

API_BASE = "http://localhost:8000"


def login(username: str, password: str):
    """
    POST /auth/token with username and password.
    Returns (access_token, None) on success or (None, error_message) on failure.

    TODO: Implement this function.
    Steps:
      1. requests.post(API_BASE + "/auth/token", json={...})
      2. Check response.ok — if not, return (None, error message)
      3. Parse response.json() — return the access_token
      4. Catch requests.ConnectionError
    """
    # TODO: implement
    try:
        response = requests.post(f"{API_BASE}/auth/token", data={
            "username": username,
            "password": password
        })
        if not response.ok:
            return (None, response.json().get("detail", "Login failed"))
        token = response.json()
        return (token["access_token"], None)
    except requests.exceptions.ConnectionError:
        return (None, "Cannot connect to API")


def get_tasks(token: str):
    """
    GET /tasks with Bearer token.
    Returns (list_of_tasks, None) or (None, error_message).

    TODO: Implement this function.
    Include the header: {"Authorization": f"Bearer {token}"}
    """
    # TODO: implement
    try: 
        response = requests.get(f"{API_BASE}/tasks", headers={"Authorization": f"Bearer {token}"} )
        if not response.ok:
            return (None, response.json().get("detail", "Login failed"))
        data = response.json()
        return (data, None)
    except requests.exceptions.ConnectionError:
        return (None, "Cannot connect to API") 


def create_task(token: str, title: str):
    """
    POST /tasks with Bearer token and JSON body {"title": title}.
    Returns (new_task_dict, None) or (None, error_message).

    TODO: Implement this function.
    """
    # TODO: implement
    try: 
        response = requests.post(f"{API_BASE}/tasks", headers={"Authorization": f"Bearer {token}"}, json={
            "title": title
        })
        if not response.ok:
            return (None, response.json().get("detail", "Login failed"))
        data = response.json()
        return (data, None)
    except requests.exceptions.ConnectionError:
        return (None, "Cannot connect to API") 


def complete_task(token: str, task_id: int):
    """
    PATCH /tasks/{task_id} with Bearer token.
    Returns (updated_task_dict, None) or (None, error_message).

    TODO: Implement this function.
    """
    # TODO: implement
    try: 
        response = requests.patch(f"{API_BASE}/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"}, json={"completed": True})
        if not response.ok:
            return (None, response.json().get("detail", "Login failed"))
        data = response.json()
        return (data, None)
    except requests.exceptions.ConnectionError:
        return (None, "Cannot connect to API") 
