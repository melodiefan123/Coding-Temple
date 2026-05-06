# Create a script (status_detective.py) that makes the following requests to JSONPlaceholder and reports the status code, category (success/client error/server error), and a brief description for each:

# GET /posts/1 - should succeed
# GET /posts/99999 - nonexistent resource
# POST /posts with valid data, should create
# DELETE /posts/1 - should succeed
# GET /invalidendpoint - bad URI
# GET /users/1/todos - nested resource
import requests
from urllib.parse import urlparse

# For each request, your output should look like:

# GET /posts/1
#   Status: 200 (Success)
#   Description: Request succeeded — resource returned

# Bonus: Add a function that takes any URL and method, makes the request, and returns a formatted status report.
def status_detective(method, url, data = None):
    path = urlparse(url).path
    method = method.upper()
    if method == "GET": 
        response = requests.get(url)
    elif method == "POST": 
        response = requests.post(url, json=data)
    elif method == "DELETE":
        response = requests.delete(url)
    else:
        print(f"{method} {path}")
        print(f" Status: N/A")
        print(" Description: Invalid HTTP method")
        return
    code = response.status_code
    if 200 <= code < 300:
        category = "Success"
        if code == 201:
            description = "Resource created successfully"
        else:
            description = "Request succeeded — resource returned"
    elif 400 <= code < 500:
        category = "Client Error"
        if code == 404: 
            description = "Resource not found or endpoint does not exist"
        else: 
            description = "Client error occurred"
    elif 500 <= code < 600: 
        category = "Server Error"
        description = "Server encountered an error"
    else:
        category = "Unknown"
        description = "Unexpected status code"

    print(f"{method} {path}")
    print(f" Status: {code} ({category})")
    print(f" Description: {description}")

base = "https://jsonplaceholder.typicode.com"

status_detective("GET", f"{base}/posts/1")
status_detective("GET", f"{base}/posts/99999")
status_detective("POST", f"{base}/posts", {"title": "new_post"})
status_detective("DELETE", f"{base}/posts/1")
status_detective("GET", f"{base}/invalidendpoint")
status_detective("GET", f"{base}/users/1/todos")