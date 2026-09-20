Part 1 — API Design Document (2 Minutes)

Hi everyone, my project is a REST API design for a Study Tracker application.

The goal of this API is to help students manage their academic workload by tracking courses, logging daily study sessions, and setting weekly study goals to measure their progress.

The main resources in my system are:
- Users
- Courses
- StudySessions
- Goals

One key relationship in my design is between Courses and StudySessions. One course can have many study sessions logged under it, but each study session belongs to a single course. I structured it this way so students can easily track time spent per subject.

Another core relationship is between Courses and Goals. A course can have multiple weekly target goals over time, which allows students to assess if they hit their intended target hours.

For endpoints, I designed complete CRUD operations across resources and included a filtering endpoint:
GET /sessions?course_id=4&start_date=2026-05-01

This allows students to retrieve logs specific to a subject or date window without fetching unnecessary data.

For authentication, I chose JWT Bearer tokens. Standard user actions—like viewing courses or logging study hours—require a token so that students can only access and modify their own study records.

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

For example, the response included abilities like static and lightning-rod.

One interesting thing about this API response was how deeply nested the JSON data was. Some values were inside multiple dictionaries and lists, which required careful navigation in Python.

--------------------------------------------------

Reflection (1 Minute)

The most surprising thing I learned about APIs was how different API response structures can be. Some APIs return simple JSON lists, while others return deeply nested objects containing navigational links to related resources.

The hardest design decision for my API was deciding how to structure relationships between resources, especially determining access permissions and filtering parameters for endpoints.

Overall, this project helped me better understand REST APIs, HTTP methods, authorization boundaries, and how schema choices shape user experience.