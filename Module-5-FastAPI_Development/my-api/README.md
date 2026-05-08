<!-- Create two resources with schemas and routers:
Recipes (/recipes):
• GET /recipes — List all recipes
• GET /recipes/{id} — Get a specific recipe
• POST /recipes — Create a recipe (fields: title, cuisine, prep_time_minutes, servings)

Ingredients (/ingredients):
• GET /ingredients — List all ingredients
• POST /ingredients — Create an ingredient (fields: name, category)
Wire both routers into main.py
Use in-memory lists for storage (no database yet)
Verify that both resource groups appear as separate sections in the Swagger UI -->