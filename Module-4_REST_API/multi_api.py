# Build a Python script that consumes two different public APIs and combines their data into a useful display.

# Suggested APIs (no authentication required):

# JSONPlaceholder: https://jsonplaceholder.typicode.com
# httpbin.org: https://httpbin.org (echo/testing API)
# Open-Meteo: https://open-meteo.com/en/docs (weather data)
# PokeAPI: https://pokeapi.co/api/v2/ (Pokémon data)
# Your script should:

# Make at least 3 requests across 2 different APIs
# Combine or compare the data in some meaningful way
# Handle potential errors (what if one API is down?)
# Print a nicely formatted summary
import requests
import random
try: 
    user_input = input("Enter a city to get the current weather:   ")
    city_coordinate = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={user_input}").json()
    if not city_coordinate["results"]:
        print(f"Sorry, we couldn't find the city '{user_input}'. Please check the spelling and try again.")
    else:
        weather_response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={city_coordinate['results'][0]['latitude']}&longitude={city_coordinate['results'][0]['longitude']}&current_weather=true")
        weather_data = weather_response.json()

        temp = weather_data["current_weather"]["temperature"]
        print(f"The current temperature in {user_input} is {temp}°C.")

        if temp < 5:
            pokemon_type = "ice"
        elif temp >= 25:
            pokemon_type = "fire"
        else:
            pokemon_type = "normal"

        pokemon_response = requests.get(f"https://pokeapi.co/api/v2/type/{pokemon_type}")
        pokemon_data = pokemon_response.json()
        pokemon_names = [pokemon["pokemon"]["name"] for pokemon in pokemon_data["pokemon"]]
        print(f"Based on the current weather, you might like these {pokemon_type}-type Pokémon: {random.choice(pokemon_names)}.")
except requests.exceptions.RequestException as e: 
        print(f"Something went wrong connecting to an API: {e}")
