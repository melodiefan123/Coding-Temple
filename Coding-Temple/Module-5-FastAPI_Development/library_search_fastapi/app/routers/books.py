from fastapi import APIRouter, HTTPException, Query, Path
from app.schemas.book import Book, Genre
from typing import Optional

router = APIRouter(prefix="/books", tags=["Books"])

#Sample Data
books_db = [
    {"id": 1, "title": "Dune", "author": "Frank Herbert", "genre": Genre.fiction, "year": 1965},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": Genre.fiction, "year": 1949},
    {"id": 3, "title": "Brave New World", "author": "Aldous Huxley", "genre": Genre.fiction, "year": 1932},
    {"id": 4, "title": "A Brief History of Time", "author": "Stephen Hawking", "genre": Genre.science, "year": 1988},
    {"id": 5, "title": "The Selfish Gene", "author": "Richard Dawkins", "genre": Genre.science, "year": 1976},
    {"id": 6, "title": "Sapiens", "author": "Yuval Noah Harari", "genre": Genre.history, "year": 2011},
    {"id": 7, "title": "The Devil in the White City", "author": "Erik Larson", "genre": Genre.history, "year": 2003},
    {"id": 8, "title": "Educated", "author": "Tara Westover", "genre": Genre.nonfiction, "year": 2018},
    {"id": 9, "title": "The Body Keeps the Score", "author": "Bessel van der Kolk", "genre": Genre.nonfiction, "year": 2014},
]

@router.get("/", response_model=list[Book])
def search_books(
    genre: Optional[Genre] = Query(default=None, description="Filter by genre"),
    sort_by: Optional[str] = Query(default=None, pattern="^(title|author|year)$", description="Field to sort by (title, author, year)"),
    min_year: Optional[int] = Query(default=None, gt=0 , description="Minimum publication year"), 
    max_year: Optional[int] = Query(default=None, description="Maximum publication year"), 
    search: Optional[str] = Query(default=None, min_length=1, description="Search term for title or author"),
    skip: int = Query(default=0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(default=10, ge=1, le=25, description="Maximum number of records to return for pagination")):
    if min_year is not None and max_year is not None and min_year > max_year:
        raise HTTPException(status_code=400, detail="min_year cannot be greater than max_year")
    
    results = books_db.copy()

    if genre: 
        results = [book for book in results if book["genre"] == genre]
    if min_year is not None:
        results = [b for b in results if b["year"] >= min_year]
    if max_year is not None:
        results = [b for b in results if b["year"] <= max_year]
    if search: 
        search_lower = search.lower()
        results = [book for book in results if search_lower in book["title"].lower() or search_lower in book["author"].lower()]

    if sort_by:
        results = sorted(results, key=lambda b: b[sort_by])
    results = results[skip: skip + limit]
    return results

@router.get("/genre/{genre}", response_model=list[Book])
def list_books_by_genre(
    genre: Genre,
    sort_by: Optional[str] = Query(default=None, pattern="^(title|year)$", description="Sort by title or year")
):
    
    results = [book for book in books_db if book["genre"] == genre]
    if sort_by:
        results = sorted(results, key=lambda b: b[sort_by])
    return results

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int = Path(gt=0, description="The ID of the book to retrieve")):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

