<!-- GET /books — List books with query parameter filters:
genre (optional, use an Enum: fiction, nonfiction, science, history)
min_year (optional, integer, must be > 0)
max_year (optional, integer)
search (optional, searches book titles, min 1 character)
skip and limit for pagination (limit capped at 25)
GET /books/{book_id} — Get a specific book (ID must be > 0)
GET /books/genre/{genre} — List all books in a genre, with optional sort_by query parameter (title or year) -->