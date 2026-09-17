# Module 4 Project — API Exploration Notes

---

# API 1: JSONPlaceholder

## Base URL
https://jsonplaceholder.typicode.com

## Authentication Method
None

## Endpoints Tested

| Method | Path | Description | Example Response Shape |
|---|---|---|---|
| GET | /users | Gets a list of users | `[{"id":1,"name":"Leanne Graham","email":"Sincere@april.biz"}]` |
| GET | /posts?userId=3 | Gets posts from a specific user | `[{"userId":3,"id":21,"title":"...", "body":"..."}]` |
| POST | /posts | Creates a new post | `{"title":"new post","body":"...","userId":11,"id":101}` |

## Rate Limits Observed
No rate limit headers were returned in the response.

## One Thing That Surprised Me
The POST request appeared to create a new resource and returned an ID, even though JSONPlaceholder is a fake testing API and does not permanently save data.

---

# API 2: PokeAPI

## Base URL
https://pokeapi.co/api/v2

## Authentication Method
None

## Endpoints Tested

| Method | Path | Description | Example Response Shape |
|---|---|---|---|
| GET | /pokemon/25 | Gets information about Pikachu | `{"name":"pikachu","height":4,"weight":60}` |
| GET | /type/13 | Gets electric-type Pokémon | `{"pokemon":[{"pokemon":{"name":"pikachu"}}]}` |
| GET | /pokemon/1 | Gets information about Bulbasaur | `{"name":"bulbasaur","abilities":[...]}` |

## Rate Limits Observed
No standard rate limit headers were returned.

## One Thing That Surprised Me
The Pokémon response objects were much larger and more deeply nested than expected. Many objects contained URLs to related resources that could be queried separately.

---

# API 3: REST Countries

## Base URL
https://restcountries.com/v3.1

## Authentication Method
None

## Endpoints Tested

| Method | Path | Description | Example Response Shape |
|---|---|---|---|
| GET | /name/japan | Gets information about Japan | `[{"name":{"official":"Japan"},"capital":["Tokyo"]}]` |
| GET | /region/europe | Gets all countries in Europe | `[{"name":{"official":"France"}},{"name":{"official":"Germany"}}]` |
| GET | /name/InvalidCountry | Tests error handling for invalid country names | `{"status":404,"message":"Not Found"}` |

## Rate Limits Observed
No rate limit headers were provided by the API.

## One Thing That Surprised Me
The API returned data as a list even when searching for a single country by name, so the first result had to be accessed with `[0]`.

---

# Overall Observations

- All three APIs were public and easy to test with Python requests.
- JSONPlaceholder was useful for testing HTTP methods like GET and POST.
- PokeAPI had the most detailed and nested JSON structure.
- REST Countries had simple and readable responses.
- None of the APIs exposed standard rate limit headers in their responses.