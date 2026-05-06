# Making an unauthenticated request to https://api.github.com/user and printing the status code (you should get 401)

import requests
response = requests.get("https://api.github.com/user")
print(f"Status Code: {response.status_code} {response.reason}")
# Making an unauthenticated request to https://api.github.com/users/octocat and printing the status code (this public endpoint should return 200)
response = requests.get("https://api.github.com/users/octocat")
print("-"*40)
print(f"Status Code: {response.status_code} {response.reason}")
# A function called create_auth_headers() that takes an API key and an auth type ("bearer" or "api-key") and returns the correct headers dictionary

def create_auth_headers(api_key, auth_type):
    auth_type = auth_type.lower()
    if not api_key:
        raise ValueError("API key is required")
    if auth_type == "bearer":
        return {"Authorization": f"Bearer {api_key}"}
    elif auth_type == "api-key":
        return {"X-API-Key": api_key}
    else:
        raise ValueError("Invalid auth type. Use 'bearer' or 'api-key'.")