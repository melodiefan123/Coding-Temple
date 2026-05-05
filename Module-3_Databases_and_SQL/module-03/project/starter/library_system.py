"""
Module 3 Project: Library Management System
library_system.py — Database models and query functions

Your job: Implement the SQLAlchemy models and all functions marked with # TODO.
"""

from sqlalchemy import create_engine, String, Integer, Boolean, ForeignKey, Table, Column, Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from datetime import date,timedelta
from typing import Optional

engine = create_engine("sqlite:///library.db", echo=False)
class Base(DeclarativeBase):
    pass

# TODO: Create the association table for Book <-> Genre (many-to-many)
book_genres = Table(
    "book_genres", Base.metadata,
    Column("book_id",  Integer, ForeignKey("books.id"),  primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

book_author = Table(
    "book_author", Base.metadata, 
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id"),
    primary_key=True))

# TODO: Implement the Author model
# Attributes: id (PK), name (required), bio (optional)
class Author(Base):
    __tablename__ = "authors"
    # TODO: define columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    book: Mapped[list["Book"]]= relationship(secondary=book_author, back_populates="author")
    
# TODO: Implement the Genre model
# Attributes: id (PK), name (required, unique)
class Genre(Base):
    __tablename__ = "genres"
    # TODO: define columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    book: Mapped[list["Book"]] = relationship(secondary=book_genres, back_populates="genre")

# TODO: Implement the Book model
# Attributes: id (PK), title (required), isbn (unique, required),
#             published_year (optional), author_id (FK), available (bool, default True)
# Relationships: author (many-to-one), genres (many-to-many via book_genres)
class Book(Base):
    __tablename__ = "books"
    # TODO: define columns and relationships
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    isbn: Mapped[int] = mapped_column(unique=True, nullable=False)
    published_year: Mapped[Optional[int]] = mapped_column()
    available: Mapped[bool] = mapped_column(default=True)
    genre: Mapped[list["Genre"]] = relationship(secondary=book_genres, back_populates="book")
    author: Mapped[list["Author"]] = relationship(secondary=book_author, back_populates="book")
    check_outs: Mapped[list["Checkout"]] = relationship(back_populates="books")

# TODO: Implement the Borrower model
# Attributes: id (PK), name (required), email (unique, required), phone (optional)
class Member(Base):
    __tablename__ = "members"
    # TODO: define columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[Optional[int]] = mapped_column()
    check_outs: Mapped[list["Checkout"]] = relationship(back_populates="members")

# TODO: Implement the Checkout model
# Attributes: id (PK), book_id (FK), borrower_id (FK),
#             checkout_date (date), due_date (date), return_date (date, nullable)
# Relationships: book, borrower
class Checkout(Base):
    __tablename__ = "checkouts"
    # TODO: define columns and relationships
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int]= mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    checkout_date: Mapped[date] = mapped_column()
    return_date: Mapped[date] = mapped_column(nullable=True)
    due_date: Mapped[date] = mapped_column()
    books: Mapped["Book"] = relationship(back_populates="check_outs")
    members: Mapped["Member"] = relationship(back_populates="check_outs")

def init_db():
    """Create all database tables. Call this before using any other functions."""
    # TODO: Base.metadata.create_all(engine)
    Base.metadata.create_all(engine)
# ============================================================
# CRUD FUNCTIONS — implement each one
# ============================================================

def add_author(name: str, bio: str = None):
    """Add a new author. Returns the created Author object."""
    # TODO: open Session, create Author, add + commit, return it
    with Session(engine) as session: 
        new_author = Author(name=name, bio = bio)
        session.add(new_author)
        session.commit()
        session.refresh(new_author)
        return new_author

def add_book(title: str, isbn: str, author_id: int,
             published_year: int = None, genre_names: list = None):
    """
    Add a new book. Assigns genres by name (creates genre if it doesn't exist yet).
    Returns the created Book object.
    """
    # TODO: implement
    with Session(engine) as session: 
        author = [session.query(Author).filter(Author.id == author_id).first()]
        genres = []
        if genre_names: 
            for name in genre_names: 
                genre = session.query(Genre).filter(Genre.name==name).first()
                if not genre: 
                    genre = Genre(name=name)  
                    session.add(genre)
                genres.append(genre)      
        new_book = Book(title = title, isbn = isbn, author = author, published_year = published_year, genre = genres)
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        return new_book


def add_member(name: str, email: str, phone: str = None):
    """Register a new borrower. Returns the created Borrower object."""
    # TODO: implement
    with Session(engine) as session: 
        new_member = Member(name = name, email = email, phone = phone)
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        return new_member

def checkout_book(book_id: int, member_id: int, days: int = 14):
    """
    Check out a book. Sets book.available = False. due_date = today + days.
    Raises ValueError if the book is not available.
    Returns the created Checkout object.
    """
    # TODO: implement
    with Session(engine) as session: 
        book = session.query(Book).filter(Book.id == book_id).first()
        
        if book: 
                if book.available: 
                    checkout_object = Checkout(books = book, checkout_date = date.today(),due_date = date.today() + timedelta(days=days), member_id = member_id)
                    book.available = False
                    session.add(checkout_object)
                    session.commit()
                    session.refresh(checkout_object)
                    return checkout_object
        else: 
            raise ValueError("Book not available")
        
        

def return_book(checkout_id: int):
    """
    Return a book. Sets book.available = True, sets return_date = today.
    Returns the updated Checkout object.
    """
    # TODO: implement
    with Session(engine) as session: 
        checkout = session.query(Checkout).filter(Checkout.id == checkout_id).first()
        checkout.return_date = date.today()
        checkout.books.available = True
        session.add(checkout)
        session.commit()
        session.refresh(checkout)
        _ = checkout.books
        return checkout
            
# ============================================================
# QUERY FUNCTIONS
# ============================================================

def find_books_by_author(author_name: str) -> list:
    """Return all books whose author name contains author_name (case-insensitive)."""
    # TODO: implement — use LIKE or ilike for partial matching
    with Session(engine) as session: 
        joined_tables= session.query(Book).join(book_author).join(Author).filter(Author.name.ilike(f"%{author_name}%"))
        return list(joined_tables)


def get_overdue_books() -> list:
    """Return all Checkout objects where due_date < today and return_date is None."""
    # TODO: implement
    with Session(engine) as session: 
        checkout = session.query(Checkout).filter(Checkout.return_date==None).filter(Checkout.due_date < date.today())
        return checkout.all()

def get_popular_genres(limit: int = 3) -> list:
    """Return the top `limit` genres by checkout count."""
    # TODO: implement — needs a join through Book to Checkout
    with Session(engine) as session: 
        results = session.query(Genre).join(book_genres).join(Book).join(Checkout).group_by(Genre.id).order_by(func.count(Checkout.id).desc()).limit(limit=limit).all()
        for result in results: 
            _=result.book
    return results

def get_available_books() -> list:
    """Return all Book objects where available == True."""
    # TODO: implement
    with Session(engine) as session:
        return session.query(Book).filter_by(available=True).all()
