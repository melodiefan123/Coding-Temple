"""
Module 6 Project — AI Dashboard
API Client
============
Centralised functions for all backend communication.
"""

import requests

API_BASE = "http://localhost:8000"


def login(username: str, password: str):
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
    try: 
        response = requests.get(f"{API_BASE}/tasks", headers={"Authorization": f"Bearer {token}"})
        if not response.ok:
            return (None, response.json().get("detail", "Failed to fetch tasks"))
        data = response.json()
        return (data, None)
    except requests.exceptions.ConnectionError:
        return (None, "Cannot connect to API") 


def create_task(token: str, title: str):
    try: 
        response = requests.post(f"{API_BASE}/tasks", headers={"Authorization": f"Bearer {token}"}, json={
            "title": title
        })
        if not response.ok:
            return (None, response.json().get("detail", "Failed to create task"))
        data = response.json()
        return (data, None)
    except requests.exceptions.ConnectionError:
        return (None, "Cannot connect to API") 


def complete_task(token: str, task_id: int):
    try: 
        response = requests.patch(f"{API_BASE}/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"}, json={"completed": True})
        if not response.ok:
            return (None, response.json().get("detail", "Failed to complete task"))
        data = response.json()
        return (data, None)
    except requests.exceptions.ConnectionError:
        return (None, "Cannot connect to API")