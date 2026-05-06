# Makes GET requests to three different endpoints:
# https://jsonplaceholder.typicode.com/posts/1
# https://jsonplaceholder.typicode.com/users/1
# https://httpbin.org/get
# For each response, display:
# The Content-Type
# The Content-Length (or "Not specified" if missing)
# Whether caching headers are present
# Any rate-limiting headers
# The total number of response headers
# Make a POST request to https://httpbin.org/post with a JSON body and custom headers (X-Student-Name set to your name). Print the response, httpbin.org echoes back everything you sent, so you can verify your headers were received.
import requests

responses = [
    requests.get("https://jsonplaceholder.typicode.com/posts/1"), requests.get("https://jsonplaceholder.typicode.com/users/1"), requests.get("https://httpbin.org/get"),
    ]
for response in responses:
    print("="*50)
    print(f"Content-Type: {response.headers.get('Content-Type', 'Not specified')}")
    print(f"Content-Length: {response.headers.get('Content-Length', 'Not specified')}")
    cache_headers = [key for key in response.headers if "cache" in key.lower()]
    print(f"Caching Headers: {', '.join(cache_headers) if cache_headers else 'None'}")
    rate_limit_headers = [key for key in response.headers if "rate" in key.lower() and "limit" in key.lower()]
    print(f"Rate-Limiting Headers: {', '.join(rate_limit_headers) if rate_limit_headers else 'None'}")
    print(f"Total Response Headers: {len(response.headers)}")

print("="*50)
post_response = requests.post("https://httpbin.org/post", json={"message": "Hello, httpbin!"}, headers={"X-Student-Name": "Melodie"})
print(f"POST https://httpbin.org/post")
print("\nResponse Body")
print(post_response.json())
print("POST Request Headers:")
for key,value in post_response.request.headers.items(): 
    print(f"{key}: {value}")