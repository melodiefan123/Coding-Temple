# Use the requests library to fetch data from the PokéAPI (https://pokeapi.co/api/v2/)
# Fetch data for 3 different Pokémon by name (e.g., pikachu, charizard, bulbasaur). The endpoint pattern is: https://pokeapi.co/api/v2/pokemon/{name}
# For each Pokémon, extract and print:
# Name
# Height
# Weight
# Types (a Pokémon can have multiple types — look in the types field of the response)
# Handle a 404 error gracefully: also try fetching a Pokémon that doesn't exist (e.g., "pikacu" - a common misspelling). Your code should check the status code and print a helpful error message instead of crashing.
import requests
import json


def fetch_pokemon(name: str):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if response.status_code==200:
       result = response.json()
       print(f"---{name}---\nHeight:{result['height']}\nWeight:{result['weight']}\nTypes:{','.join([item['type']['name'] for item in result['types']])}")
    else:
        print(f"---{name}---\nError: Pokémon '{name}' not found (Status 404). Check your spelling!")


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