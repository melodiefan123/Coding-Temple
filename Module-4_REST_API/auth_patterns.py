
import requests

def response_status(url):
    response = requests.get(url)
    print(f"Status Code: {response.status_code} {response.reason}")
# Making an unauthenticated request to https://api.github.com/user and printing the status code (you should get 401)

response_status("https://api.github.com/user")

# Making an unauthenticated request to https://api.github.com/users/octocat and printing the status code (this public endpoint should return 200)

response_status("https://api.github.com/users/octocat")

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
    
#For edge cases when for custom headers instead of hard-coding
def create_auth_headers(api_key, auth_type, header_name=None):
    auth_type = auth_type.lower()
    if not api_key:
        raise ValueError("API key is required")
    if auth_type == "bearer":
        return {"Authorization": f"Bearer {api_key}"}
    elif header_name:
        return {f"{header_name}": api_key}
    else:
        raise ValueError("Invalid auth type. Use 'bearer' or the custom header name.")