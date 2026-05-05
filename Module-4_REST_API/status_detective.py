# Create a script (status_detective.py) that makes the following requests to JSONPlaceholder and reports the status code, category (success/client error/server error), and a brief description for each:

# GET /posts/1 - should succeed
# GET /posts/99999 - nonexistent resource
# POST /posts with valid data, should create
# DELETE /posts/1 - should succeed
# GET /invalidendpoint - bad URI
# GET /users/1/todos - nested resource
import requests
from urllib.parse import urlparse

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
print(f"GET /posts/1 \n  Status: {response.status_code} (Success)\n  Description: {response.reason}")

response = requests.get("https://jsonplaceholder.typicode.com/posts/99999")
print(f"GET /posts/99999 \n  Status: {response.status_code}\n  Description: {response.reason}")

new_post = {
    "title": "new_post"
}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)
print(f"POST /posts \n  Status: {response.status_code}\n  Description: {response.reason}")

response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print(f"DELETE /posts/1 \n  Status: {response.status_code}\n  Description: {response.reason}")

response = requests.get("https://jsonplaceholder.typicode.com/invalidendpoint")
print(f"GET /invalidendpoint \n  Status: {response.status_code}\n  Description: {response.reason}")

response = requests.get("https://jsonplaceholder.typicode.com/users/1/todos")
print(f"GET /users/1/todos \n  Status: {response.status_code}\n  Description: {response.reason}")





# For each request, your output should look like:

# GET /posts/1
#   Status: 200 (Success)
#   Description: Request succeeded — resource returned

# Bonus: Add a function that takes any URL and method, makes the request, and returns a formatted status report.
def status_detective(method, url, data = None):
    path = urlparse(url).path
    method = method.upper()
    if method == "GET": 
        response = requests.get(url=url)
    elif method == "POST": 
        response = requests.post(url=url, json=data)
    elif method == "DELETE":
        response = requests.delete(url=url)
    else:
        print(f"{method} {path}\n  Status: N/A\n  Description: Invalid HTTP method")
        return
    if response.status_code >= 200 and response.status_code <=299:
        print(f"{method} {path} \n  Status: {response.status_code} Success \n Description: {response.reason} ")
    elif response.status_code >= 400 and response.status_code <=499:
        print(f"{method} {path} \n  Status: {response.status_code} Client Error \n  Description: {response.reason}")
    elif response.status_code >= 500 and response.status_code <=599: 
        print(f"{method} {path} \n  Status: {response.status_code} Server Error \n  Description: {response.reason}")