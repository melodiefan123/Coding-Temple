import requests
# GET all users and print each user's name and email
response_users = requests.get("https://jsonplaceholder.typicode.com/users")
users = response_users.json()
for user in users: 
    print(f"Name: {user['name']} \n Email: {user['email']}")
print(f"{len(users)} users")
print(f"Status Code: {response_users.status_code}")

# GET all posts by user #3 (use query parameters)
response_posts = requests.get("https://jsonplaceholder.typicode.com/posts", params={"userId": 3})
posts = response_posts.json()

print(f"Posts by user 3: {len(posts)}")
print(f"Status Code: {response_posts.status_code}")

# GET all comments on post #1 (endpoint: /posts/1/comments)
response_comments = requests.get("https://jsonplaceholder.typicode.com/posts/1/comments")
comments = response_comments.json()
print(f"Comments on post #1: {len(comments)}")
print(f"Status Code: {response_comments.status_code}")

# POST a new post (simulated) and print the response
new_post = {
    "title": "new post", 
    "body": "This is created by sending a post request",
    "userId": 11
}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)

print(f"Created Status: {response.status_code}")

created = response.json()
print(f"Created post with id: {created['id']}")
print(f"Title: {created['title']}")
print(f"Post: {created['body']}")