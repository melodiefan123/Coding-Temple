# Fetches the 3 most-starred repositories for the user "google" (hint: use sort and per_page parameters)
# For each repo, prints the name, description, star count, and primary language
# Prints the remaining rate limit after the request

import requests
responses = requests.get("https://api.github.com/search/repositories", params={"q": "user:google", "sort": "stars","order": "desc", "per_page": 3}, headers={"Accept": "application/vnd.github+json"})
data = responses.json()
for repo in data['items']:
    print(f"Name: {repo['name']}")
    print(f"Description: {repo['description']}")
    print(f"Stars: {repo['stargazers_count']}")
    print(f"Language: {repo['language']}")
    print("-" * 40)

print(f"Remaining rate limit: {responses.headers.get('X-RateLimit-Remaining')}")