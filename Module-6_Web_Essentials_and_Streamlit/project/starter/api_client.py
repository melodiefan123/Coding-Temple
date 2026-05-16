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
    return None, "Not implemented yet"


def get_tasks(token: str):
    """
    GET /tasks with Bearer token.
    Returns (list_of_tasks, None) or (None, error_message).

    TODO: Implement this function.
    Include the header: {"Authorization": f"Bearer {token}"}
    """
    # TODO: implement
    return None, "Not implemented yet"


def create_task(token: str, title: str):
    """
    POST /tasks with Bearer token and JSON body {"title": title}.
    Returns (new_task_dict, None) or (None, error_message).

    TODO: Implement this function.
    """
    # TODO: implement
    return None, "Not implemented yet"


def complete_task(token: str, task_id: int):
    """
    PATCH /tasks/{task_id}/complete with Bearer token.
    Returns (updated_task_dict, None) or (None, error_message).

    TODO: Implement this function.
    """
    # TODO: implement
    return None, "Not implemented yet"
