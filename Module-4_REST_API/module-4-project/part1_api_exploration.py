"""
Module 4 Project — Part 1: API Exploration
Explore 3 public APIs and document what you find.

Instructions:
- Fill in each TODO section
- Run the script to verify your code works
- Document your findings in comments and print statements
"""

import requests

BASE_URLS = {
    "jsonplaceholder": "https://jsonplaceholder.typicode.com",
    "pokeapi": "https://pokeapi.co/api/v2",
    "restcountries": "https://restcountries.com/v3.1",
}

# ============================================================
# API 1: JSONPlaceholder
# Documentation: https://jsonplaceholder.typicode.com/guide/
# ============================================================

def explore_jsonplaceholder():
    print("\n=== API 1: JSONPlaceholder ===")

    # TODO 1: GET all users
    # Endpoint: GET /users
    # Print each user's name and email
    # Expected: 200 OK, list of 10 users
    print("\n--- GET /users ---")
    try:
        all_users = requests.get(f"{BASE_URLS['jsonplaceholder']}/users")
        for user in all_users.json():
            print(f"Name: {user['name']} \nEmail: {user['email']}")
        print(f"Method: {all_users.request.method} URL: {all_users.url}")
        print(f"Status Code: {all_users.status_code}")
        print(f"Reason: {all_users.reason}")
        print(f"Key Headers: {all_users.headers['Content-Type']}")
    except requests.RequestException as e:
        print(f"Error fetching users: {e}")

    # TODO 2: GET posts by a specific user
    # Endpoint: GET /posts?userId=<number>
    # Print the count and first post title
    print("\n--- GET /posts?userId=3 ---")
    try: 
        user_3_posts = requests.get(f"{BASE_URLS['jsonplaceholder']}/posts", params={"userId": 3})
        posts = user_3_posts.json()
        print(f"Posts by user 3: {len(posts)}")
        if posts:
            print(f"First post title: {posts[0]['title']}")
        print(f"Method: {user_3_posts.request.method} URL: {user_3_posts.url}")
        print(f"Status Code: {user_3_posts.status_code}")
        print(f"Reason: {user_3_posts.reason}")
        print(f"Key Headers: {user_3_posts.headers['Content-Type']}")
    except requests.RequestException as e:
        print(f"Error fetching posts: {e}")

    # TODO 3: POST a new post
    # Endpoint: POST /posts
    # Body: {"title": "...", "body": "...", "userId": 1}
    # Print the status code and returned id
    print("\n--- POST /posts ---")
    try:
        new_post = {
            "title": "new post", 
            "body": "This is created by sending a post request",
            "userId": 11
        }
        response = requests.post(f"{BASE_URLS['jsonplaceholder']}/posts", json=new_post)
        print(f"Created Status: {response.status_code}")
        #201 Created is the expected status code for a successful POST that creates a resource
        print(f"Created post with id: {response.json().get('id')}")
        print(f"Method: {response.request.method} URL: {response.request.url}")
        print(f"Key Headers: {response.headers['Content-Type']}")
    except requests.RequestException as e:
        print(f"Error creating post: {e}")

# ============================================================
# API 2: PokeAPI
# Documentation: https://pokeapi.co/docs/v2
# ============================================================

def explore_pokeapi():
    print("\n=== API 2: PokeAPI ===")

    # TODO 4: GET a specific Pokémon (try ID 1 = Bulbasaur, or 25 = Pikachu)
    # Endpoint: GET /pokemon/<id>
    # Print: name, height, weight, list of abilities
    print("\n--- GET /pokemon/25 ---")
    try: 
        pokemon_response = requests.get(f"{BASE_URLS['pokeapi']}/pokemon/25")
        pokemon = pokemon_response.json()
        print(f"Name: {pokemon['name']}")
        print(f"Height: {pokemon['height']}")
        print(f"Weight: {pokemon['weight']}")
        print(f"Abilities: {[ability['ability']['name'] for ability in pokemon['abilities']]}")
        print(f"Key Headers: {pokemon_response.headers['Content-Type']}")
    except requests.RequestException as e:
        print(f"Error fetching Pokémon: {e}")

    # TODO 5: Follow the first type URL from the Pokémon response
    # The URL is at pokemon["types"][0]["type"]["url"]
    # Print: type name, first 5 Pokémon of that type
    print("\n--- GET first type URL ---")
    try: 
        url = pokemon["types"][0]["type"]["url"]
        type_response = requests.get(url)
        type_pokemon = type_response.json()["pokemon"][:5]
        print("First 5 Pokémon of this type:")
        for entry in type_pokemon:
            print(f"- {entry['pokemon']['name']} (URL: {entry['pokemon']['url']})")
        print(f"Key Headers: {type_response.headers['Content-Type']}")
    except requests.RequestException as e:
        print(f"Error fetching type information: {e}")
    except NameError: 
        print("Error: Pokémon data not available. Make sure to run the previous section first.")
    # TODO 6: Document the response structure in a comment below:
    # Top-level keys in the /pokemon response:
    # ...
    #abilities: list of ability objects, each with "ability" (name and url) and "is_hidden" boolean
    #base_experience: integer
    #forms: list of form objects (name and url)
    #game_indices: list of game index objects (game_index and version info)
    #height: integer
    #held_items: list of held item objects (item info and version details)
    #id: integer
    #is_default: boolean



# ============================================================
# API 3: REST Countries
# Documentation: https://restcountries.com/#endpoints
# ============================================================

def explore_restcountries():
    print("\n=== API 3: REST Countries ===")

    # TODO 7: GET a country by name (try "Japan" or any country you like)
    # Endpoint: GET /name/<country_name>
    # Print: official name, capital, population, region
    try:
        print("\n--- GET /name/{country_name} ---")
        country_name = input("Enter a country name to get details:   ")
        country_response = requests.get(f"{BASE_URLS['restcountries']}/name/{country_name}")
        country = country_response.json()[0]  # API returns a list of matches, take the first one
        print(f"Official Name: {country['name']['official']}")
        print(f"Capital: {country['capital'][0]}")
        print(f"Population: {country['population']}")
        print(f"Region: {country['region']}")
        print(f"Key Headers: {country_response.headers['Content-Type']}")
    except requests.RequestException as e:
        print(f"Error fetching country information: {e}")
    # TODO 8: GET all countries in a region (try "Europe" or "Asia")
    # Endpoint: GET /region/<region_name>
    # Print: count, first 10 country names alphabetically
    print("\n--- GET /region/{region_name} ---")
    try: 
        region_name = input("Enter a region name to get countries:   ")
        region_response = requests.get(f"{BASE_URLS['restcountries']}/region/{region_name}")
        countries = region_response.json()
        print(f"Count: {len(countries)}")
        print("First 10 country names alphabetically:")
        sorted_countries = sorted(countries, key=lambda c: c["name"]["official"])
        for country in sorted_countries[:10]:
            print(f"- {country['name']['official']}")
    except requests.RequestException as e:
        print(f"Error fetching region information: {e}")
    # TODO 9: Handle an error
    # Try a country name that doesn't exist
    # Handle the response gracefully (don't crash)
    print("\n--- GET /name/InvalidCountry ---")
    try:
        invalid_response = requests.get(f"{BASE_URLS['restcountries']}/name/InvalidCountry")
        if invalid_response.status_code == 404: # 404 Not Found is the expected status code when a resource is not found
            print("Country not found. Please check the name and try again.")
        else:
            print(f"Unexpected error: {invalid_response.status_code} {invalid_response.reason}")
    except requests.RequestException as e:
        print(f"Error fetching invalid country information: {e}")
    


# ============================================================
# Run all explorations
# ============================================================

if __name__ == "__main__":
    explore_jsonplaceholder()
    explore_pokeapi()
    explore_restcountries()
    print("\n=== Exploration complete! ===")
