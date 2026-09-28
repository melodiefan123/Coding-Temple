# Use the requests library to fetch data from the PokéAPI (https://pokeapi.co/api/v2/)
# Fetch data for 3 different Pokémon by name (e.g., pikachu, charizard, bulbasaur). The endpoint pattern is: https://pokeapi.co/api/v2/pokemon/{name}
# For each Pokémon, extract and print:
# Name
# Height
# Weight
# Types (a Pokémon can have multiple types — look in the types field of the response)
# Handle a 404 error gracefully: also try fetching a Pokémon that doesn't exist (e.g., "pikacu" - a common misspelling). Your code should check the status code and print a helpful error message instead of crashing.
import requests


def fetch_pokemon(name: str):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    print(f"--- {name} ---")
    if response.status_code==200:
        result = response.json()
        types = [t["type"]["name"] for t in result["types"]]
        types_str = ", ".join(types)

        # Display details with proper spacing after colons
        print(f"Height: {result['height']}")
        print(f"Weight: {result['weight']}")
        print(f"Types: {types_str}\n")
    else:
        # Dynamically include response.status_code and add a trailing newline
        print(f"Error: Pokémon '{name}' not found (Status {response.status_code}). Check your spelling!\n")


fetch_pokemon("pikachu")
fetch_pokemon("charizard")
fetch_pokemon("bulbasaur")
fetch_pokemon("pikacu")

#Result should look like the following
# --- pikachu ---
# Height: 4
# Weight: 60
# Types: electric

# --- charizard ---
# Height: 17
# Weight: 905
# Types: fire, flying

# --- bulbasaur ---
# Height: 7
# Weight: 69
# Types: grass, poison

# --- pikacu ---
# Error: Pokémon 'pikacu' not found (Status 404). Check your spelling!