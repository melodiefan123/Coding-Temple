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
import json

urls = [
    "https://jsonplaceholder.typicode.com/posts/1",
    "https://jsonplaceholder.typicode.com/users/1",
    "https://httpbin.org/get"
]

def display(method, response):
    print("="*50)
    print(f"{method} {response.url}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'Not specified')}")
    print(f"Content-Length: {response.headers.get('Content-Length', 'Not specified')}")
    cache_headers = [key for key in response.headers if "cache" in key.lower()]
    print(f"Caching Headers: {', '.join(cache_headers) if cache_headers else 'None'}")
    rate_limit_headers = [key for key in response.headers if "rate" in key.lower() and "limit" in key.lower()]
    print(f"Rate-Limiting Headers: {', '.join(rate_limit_headers) if rate_limit_headers else 'None'}")
    print(f"Total Response Headers: {len(response.headers)}")

for url in urls:
    response = requests.get(url)
    display("GET", response)

post_response = requests.post("https://httpbin.org/post", json={"message": "Hello, httpbin!"}, headers={"X-Student-Name": "Melodie"})
display("POST", post_response)
