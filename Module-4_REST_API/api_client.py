import requests
import json

class APIClient:
    """A simple API client — similar to how you'd organize a Postman collection."""
    
    def __init__(self, base_url, headers=None):
        self.base_url = base_url.rstrip("/")
        self.default_headers = headers or {}
    
    def _request(self, method, path, **kwargs):
        """Make a request and return a formatted result."""
        url = f"{self.base_url}{path}"
        
        # Merge default headers with any request-specific headers
        headers = {**self.default_headers, **kwargs.pop("headers", {})}
        
        response = requests.request(method, url, headers=headers, **kwargs)
        
        return {
            "status": response.status_code,
            "reason": response.reason,
            "time_ms": response.elapsed.total_seconds() * 1000,
            "data": response.json() if response.text else None,
            "headers": dict(response.headers),
        }
    
    def get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)
    
    def post(self, path, **kwargs):
        return self._request("POST", path, **kwargs)
    
    def put(self, path, **kwargs):
        return self._request("PUT", path, **kwargs)
    
    def patch(self, path, **kwargs):
        return self._request("PATCH", path, **kwargs)
    
    def delete(self, path, **kwargs):
        return self._request("DELETE", path, **kwargs)



class JSONPlaceholderClient(APIClient):
    def __init__(self):
        super().__init__("https://jsonplaceholder.typicode.com")
    
    def get_user(self, user_id):
        """Get a specific user's profile."""
        # Your implementation here
        return self.get(f"/users/{user_id}")
    def get_user_posts(self, user_id):
        """Get all posts by a specific user."""
        # Your implementation here
        return self.get(f"/users/{user_id}/posts")

    def create_post(self, user_id, title, body):
        """Create a new post for a user."""
        # Your implementation here
        return self.post("/posts", json={"title": title, "body": body, "userId": user_id})

    def search_posts(self, query):
        """Search posts by title (client-side filtering)."""
        # Your implementation here — get all posts and filter locally
        all_posts = self.get("/posts")["data"]
        return [post for post in all_posts if query.lower() in post["title"].lower()]
    
client = JSONPlaceholderClient()
print("User 5 profile:")
user_5 = client.get_user(5)
print(f"Name: {user_5['data']['name']} City: {user_5['data']['address']['city']}")

print("\nPosts by user 5:")
user_5_posts = client.get_user_posts(5)
for post in user_5_posts["data"]:
    print(f" - {post['title']}")

print("\nCreating a new post for user 5...")
new_post = client.create_post(5, "My New Post", "This is the body of my new post.")
print(f"Created post with ID: {new_post['data']['id']}")
print(f"Total posts for user 5: {len(user_5_posts['data'])}")
print("\nSearching for posts with 'qui' in the title...")
search_results = client.search_posts("qui")
print(f" length of search results: {len(search_results)}")