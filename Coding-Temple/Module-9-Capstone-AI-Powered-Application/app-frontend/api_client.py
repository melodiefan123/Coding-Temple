import os
import requests
import streamlit as st

class APIClient:
    def __init__(self, base_url: str = None):
        # Fix 1: Use os.getenv instead of os.env
        self.base_url = base_url or os.getenv("BACKEND_API_URL", "http://localhost:8001")

    def _get_headers(self) -> dict:
        """Dynamically builds headers with the current user token from session state."""
        token = st.session_state.get("token", "")
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def fetch_data(self, endpoint: str):
        try:
            url = f"{self.base_url}/{endpoint.strip('/')}"
            res = requests.get(url, headers=self._get_headers(), timeout=5)
            return res.json() if res.status_code == 200 else []
        except Exception as e:
            print(f"API Error ({endpoint}): {e}")
            return []

    def get_revenue_flow(self, group_by: str = "monthly"):
        """Fetches revenue flow aggregated by 'monthly' or 'weekly'."""
        try:
            url = f"{self.base_url}/metrics/revenue-flow"
            params = {"group_by": group_by}
            res = requests.get(url, params=params, headers=self._get_headers(), timeout=5)
            if res.status_code == 200:
                return res.json()
            print(f"API Error ({res.status_code}): {res.text}")
            return []
        except Exception as e:
            print(f"Connection Error (revenue-flow): {e}")
            return []

    def get_expense_breakdown(self, period: str = "This Month"):
        """Fetches expense breakdown aggregated by period."""
        try: 
            url = f"{self.base_url}/metrics/expense-breakdown"
            params = {"period": period}
            # Fix 2: Cleanly use _get_headers() and pass parameters via params
            res = requests.get(url, params=params, headers=self._get_headers(), timeout=5)
            if res.status_code == 200: 
                return res.json()
            print(f"API Error ({res.status_code}): {res.text}")
            return []
        except Exception as e: 
            print(f"Connection Error (expense-breakdown): {e}")
            return []