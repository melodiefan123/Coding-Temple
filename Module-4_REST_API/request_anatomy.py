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
responses = [
    requests.get("https://jsonplaceholder.typicode.com/users/1"), requests.post("https://jsonplaceholder.typicode.com/posts", json={"title": "Demo", "body": "Test", "userId": 1}), 
    requests.patch("https://jsonplaceholder.typicode.com/posts/1", json={"title": "Updated Title"})]

for response in responses: 
    print("="*50)
    print(f"Method: {response.request.method}")
    print(f"URL: {response.request.url}")
    print(f"\nRequest Headers:")
    for key, value in response.request.headers.items(): 
        print(f"{key}: {value}")
    print(f"\nRequest Body:")
    print(response.request.body or "None")
    print(f"\nStatus Code:{response.status_code}   Reason: {response.reason}")

    print(f"\nKey Response Headers:")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    print(f"Content-Length: {response.headers.get('Content-Length')}")

    print(f"\nResponse Body:")
    try: 
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

    print(f"\nElapsed Time: {response.elapsed.total_seconds()*1000:.3f} ms")

