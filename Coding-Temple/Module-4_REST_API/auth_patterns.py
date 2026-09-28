import requests

def response_status(url: str) -> None:
    """Makes a GET request to an endpoint and prints its status code."""
    # GitHub API strongly recommends including a User-Agent header
    headers = {"User-Agent": "Auth-Patterns-Script"}
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code} {response.reason}")


def create_auth_headers(api_key: str, auth_type: str, header_name: str = None) -> dict:
    """Generates authentication headers for HTTP requests.
    
    Supports 'bearer' and 'api-key' authorization types.
    """
    if not api_key: 
        raise ValueError("API key is required")
    
    auth_type = auth_type.lower()
    if auth_type == "bearer":
        return {"Authorization": f"Bearer {api_key}"}
    elif auth_type == "api-key":
        header = header_name if header_name else "X-API-Key"
        return {header: api_key}
    else:
        raise ValueError("Invalid auth type. Use 'bearer' or 'api-key'.")


if __name__ == "__main__":
    # 1. Unauthenticated request to protected endpoint (Expected: 401 Unauthorized)
    response_status("https://api.github.com/user")

    # 2. Unauthenticated request to public endpoint (Expected: 200 OK)
    response_status("https://api.github.com/users/octocat")