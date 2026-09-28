# Library Search API

A lightweight FastAPI application built for searching, filtering, and retrieving books from a library database.

## Features

- **Query Parameters Filtering**: Filter by genre, publication year range (`min_year` / `max_year`), and search by title or author keywords.
- **Sorting & Pagination**: Configurable page offset (`skip`), capped limits (`limit` <= 25), and flexible ordering.
- **Strict Validation**: Automatic parameter type checking, enum matching, and range validations powered by Pydantic and FastAPI.

## Endpoints

### `GET /books`
Lists all books in the library. Supports filtering, sorting, and pagination.
- **Query Parameters**:
  - `genre`: `fiction` | `nonfiction` | `science` | `history`
  - `min_year`: `integer` (> 0)
  - `max_year`: `integer`
  - `search`: `string` (searches title or author, min 1 character)
  - `sort_by`: `title` | `author` | `year`
  - `skip`: `integer` (>= 0, default: 0)
  - `limit`: `integer` (1 to 25, default: 10)

### `GET /books/genre/{genre}`
Lists all books within a specific genre with optional sorting.
- **Path Parameter**: `genre` (`fiction`, `nonfiction`, `science`, `history`)
- **Query Parameter**: `sort_by` (`title` or `year`)

### `GET /books/{book_id}`
Retrieves a specific book by its unique ID.
- **Path Parameter**: `book_id` (`integer` > 0)

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt