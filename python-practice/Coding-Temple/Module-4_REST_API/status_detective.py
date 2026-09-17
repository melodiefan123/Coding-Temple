# Create a script (status_detective.py) that makes the following requests to JSONPlaceholder and reports the status code, category (success/client error/server error), and a brief description for each:

# GET /posts/1 - should succeed
# GET /posts/99999 - nonexistent resource
# POST /posts with valid data, should create
# DELETE /posts/1 - should succeed
# GET /invalidendpoint - bad URI
# GET /users/1/todos - nested resource
import requests

base_url = "https://jsonplaceholder.typicode.com"

def status(method, url, **kwargs):
    response = requests.request(method, url, **kwargs)
    status_code = response.status_code

    if 200 <= status_code < 300:
        category = "Success"
    elif 300<= status_code < 400:
        category = "Redirection"
    elif 400 <= status_code < 500:
        category = "Client Error"
    else:
        category = "Server Error"

    descriptions = {
        200: "OK - The request was successful.",
        201: "Created - The request was successful and a resource was created.",
        204: "No Content - The request was successful but there is no content to return.",
        400: "Bad Request - The server could not understand the request due to invalid syntax.",
        401: "Unauthorized - Authentication is required and has failed or has not yet been provided.",
        403: "Forbidden - The client does not have access rights to the content.",
        404: "Not Found - The server can not find the requested resource.",
        405: "Method Not Allowed - This method isn't supported here.",
        422: "Unprocessable Entity - request understood but semantically invalid",
        500: "Internal Server Error - The server has encountered a situation it doesn't know how to handle.",
    }
    description = descriptions.get(status_code, "No description available.")
    return {
        "method": method,
        "url": url,
        "status_code": status_code,
        "category": category,
        "description": description
    }
def print_status_report(report):
    print(f"{report['method']} {report['url']}")
    print(f"    Status: {report['status_code']} ({report['category']})")
    print(f"    Description: {report['description']}")

print("/n Status Code Detective\n")

r = status("GET", f"{base_url}/posts/1")
print("\n1. GET /posts/1 - existing resource")
print_status_report(r)

r = status("GET", f"{base_url}/posts/99999")
print("\n2. GET /posts/99999 - nonexistent resource")
print_status_report(r)

r = status("POST", f"{base_url}/posts", json={"title": "foo", "body": "bar", "userId": 1})
print("\n3. POST /posts with valid data")
print_status_report(r)

r = status("DELETE", f"{base_url}/posts/1")
print("\n4. Delete a Resource")
print_status_report(r)

r = status("GET", f"{base_url}/invalidendpoint")
print("5. GET ann invalid/unknown endpoint")
print_status_report(r)

r = status("GET", f"{base_url}/users/1/todos")
print("\n6. GET nested resource")
print_status_report(r)


# For each request, your output should look like:

# GET /posts/1
#   Status: 200 (Success)
#   Description: Request succeeded — resource returned

# Bonus: Add a function that takes any URL and method, makes the request, and returns a formatted status report.
