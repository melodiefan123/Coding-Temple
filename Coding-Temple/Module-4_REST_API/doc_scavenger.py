# For each repo, prints the name, description, star count, and primary language
# Prints the remaining rate limit after the request

import requests

url = "https://api.github.com/search/repositories"

params={"q":"org:google", 
        "sort": "stars",
        "order": "desc", 
        "per_page": 3}

headers={"Accept": "application/vnd.github+json"}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200: 
    data = response.json()
    repos = data.get("items",[])
    for repo in repos:
        print(f"Name: {repo['name']}")
        print(f"Description: {repo['description'] or 'No description provided.'}")
        print(f"Stars: {repo['stargazers_count']}")
        print(f"Language: {repo['language'] or 'Not specified'}")
        print("-" * 40)
else:
    print(f"Error fetching data: HTTP {response.status_code}")

remaining_limit = response.headers.get("X-RateLimit-Remaining", "Unknown")
print(f"Remaining rate limit: {remaining_limit}")