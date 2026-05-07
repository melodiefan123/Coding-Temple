Part 1 — API Design Document (2 Minutes)

Hi everyone, my project is a REST API design for a Pet Adoption Service.

The goal of this API is to allow users to browse available pets, submit adoption applications, track application statuses, and manage adoption records.

The main resources in my API are:
- Pets
- Applications
- Adoptions
- Users
- StatusHistory

One important relationship in my design is between pets and applications.

A single pet can have many adoption applications, but each application only belongs to one pet. I structured it this way because multiple users may apply to adopt the same pet at the same time.

Another relationship I designed was a many-to-many relationship between users and pets. Users can save multiple pets, and a pet can be saved by multiple users. This would support a future “favorites” feature in the application.

For endpoints, I created full CRUD operations for pets:
- POST /pets
- GET /pets
- GET /pets/{id}
- PUT /pets/{id}
- DELETE /pets/{id}

I also included related endpoints for applications, adoptions, authentication, and filtering, such as:
GET /pets?availability=true

For authentication, I used JWT Bearer Token authentication. Public users can browse pets without logging in, but actions like creating applications or managing pet listings require authentication or admin access.

--------------------------------------------------

Part 2 — Real API Call From Explorer Script (2 Minutes)

For my API exploration script, one API I tested was PokeAPI.

One request I made was:

GET /pokemon/25

The full URL was:
https://pokeapi.co/api/v2/pokemon/25

This request retrieves information about the Pokémon Pikachu.

The HTTP method used was GET because I was retrieving data from the API.

The API returned a 200 OK status code, which means the request was successful.

The response came back in JSON format and included:
- the Pokémon’s name
- height
- weight
- and abilities

For example, the response included abilities like:
- static
- lightning-rod

One interesting thing about this API response was how deeply nested the JSON data was. Some values were inside multiple dictionaries and lists, which required careful navigation in Python.

--------------------------------------------------

Reflection (1 Minute)

The most surprising thing I learned about APIs was how different API response structures can be. Some APIs return very simple JSON responses, while others return deeply nested objects with links to additional resources.

The hardest design decision for my API was deciding how to structure relationships between resources, especially deciding which endpoints should require authentication and which should remain public.

Overall, this project helped me better understand REST APIs, HTTP methods, authentication, JSON responses, and how API design affects usability and security.