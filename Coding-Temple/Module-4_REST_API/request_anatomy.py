import requests
import json
# makes three different requests and prints the full anatomy of each:
    # A GET request for a specific user from JSONPlaceholder
    # A POST request creating a new post
    # A PATCH request updating a post's title
    # For each request, display:

    # The method and URL
    # All request headers (what your script sent)
    # The request body (if any)
    # The status code and reason
    # Key response headers (at minimum: Content-Type, Content-Length)
    # The response body
    # The elapsed time in milliseconds
    # Format the output clearly with separators between each request.

def separator(title):
    print("-"*60)
    print(f" {title} ")
    print("-"*60)

base_url = "https://jsonplaceholder.typicode.com"

def display_anatomy(response, label):
    request = response.request

    print(f"\n------Request-------")
    print(f"Method + URL: {request.method} {request.url}")
    print(f"\nRequest Headers:")
    for key, value in request.headers.items(): 
        print(f"{key}: {value}")
    
    body = request.body
    if body:
        try: 
            parsed = json.loads(body)
            print(f"\n Request Body (JSON):")
            print(f"\n. {json.dumps(parsed, indent=4)}")
        except Exception: 
            print(f"     Request body: {body}")
    else:
        print(f"     Request body: None")

    print(f"\n------Response-------")
    print(f"Status Code: {response.status_code} {response.reason}")
    print(f"Elapsed: {response.elapsed.total_seconds()*1000:.0f} ms")
    print(f"\n Key Response Headers:")
    for key in ["Content-Type", "Content-Length", "X-powered-by", "Cache-Control", "ETag"]:
        val = response.headers.get(key, "Not specified")
        print(f"      {key}: {val}")

    print(f"\n Response Body:")
    try:
        body_data = response.json()
        body_str = json.dumps(body_data, indent=4)
        if len(body_str) > 500:
            body_str = body_str[:500] + "\n... (truncated)"
        for line in body_str.split('\n'):
            print(f"      {line}")
    except Exception:
        print(f"    {response.text[:300]}")

# ============================================================
# REQUEST 1: GET a specific user
# ============================================================

separator("Request 1: GET /users/1")
r = requests.get(f"{base_url}/users/1")
display_anatomy(r, "GET User")

# ============================================================
# REQUEST 2: POST — create a new post
# ============================================================

separator("Request 2: POST /posts")
r = requests.post(f"{base_url}/posts", json={"title": "foo", "body": "bar", "userId": 1})
display_anatomy(r, "POST Create Post")

# ============================================================
# REQUEST 3: PATCH — partial update
# ============================================================
separator("Request 3: PATCH /posts/1")
r = requests.patch(f"{base_url}/posts/1", json={"title": "Updated Title"})
display_anatomy(r, "PATCH Update Post")