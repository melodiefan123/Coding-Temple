"""
Module 3 Project: Library Management System
library_system.py — Database models and query functions
"""

from datetime import date, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    create_engine, String, Integer, ForeignKey, 
    Table, Column, func
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, 
    relationship, Session, joinedload
)

engine = create_engine("sqlite:///library.db", echo=False)

class Base(DeclarativeBase):
    pass

# Association Tables
book_genres = Table(
    "book_genres", Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

book_author = Table(
    "book_author", Base.metadata, 
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True)
)

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    book: Mapped[list["Book"]] = relationship(secondary=book_author, back_populates="author")

class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    book: Mapped[list["Book"]] = relationship(secondary=book_genres, back_populates="genre")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    isbn: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    published_year: Mapped[Optional[int]] = mapped_column()
    available: Mapped[bool] = mapped_column(default=True)
    available_copies: Mapped[int] = mapped_column(default=1)
    
    genre: Mapped[list["Genre"]] = relationship(secondary=book_genres, back_populates="book")
    author: Mapped[list["Author"]] = relationship(secondary=book_author, back_populates="book")
    check_outs: Mapped[list["Checkout"]] = relationship(back_populates="books", cascade="all, delete-orphan")

class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    membership_date: Mapped[date] = mapped_column(default=date.today)
    check_outs: Mapped[list["Checkout"]] = relationship(back_populates="members", cascade="all, delete-orphan")

class Checkout(Base):
    __tablename__ = "checkouts"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    checkout_date: Mapped[date] = mapped_column(default=date.today)
    return_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    due_date: Mapped[date] = mapped_column()
    
    books: Mapped["Book"] = relationship(back_populates="check_outs")
    members: Mapped["Member"] = relationship(back_populates="check_outs")

def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(engine)

# ============================================================
# CRUD FUNCTIONS
# ============================================================

def add_author(name: str, bio: str = None) -> Author:
    """Add a new author to the database."""
    with Session(engine) as session: 
        new_author = Author(name=name, bio=bio)
        session.add(new_author)
        session.commit()
        session.refresh(new_author)
        session.expunge(new_author)
        return new_author

def add_book(title: str, isbn: str, author_ids: list[int] | int, published_year: int = None, genre_names: list = None, available_copies: int = 1) -> Book:
    """Add a book with associated authors and genres."""
    with Session(engine) as session: 
        if isinstance(author_ids, int):
            author_ids = [author_ids]
            
        authors = session.query(Author).filter(Author.id.in_(author_ids)).all()
        genres = []
        if genre_names: 
            for name in genre_names: 
                genre = session.query(Genre).filter(Genre.name == name).first()
                if not genre: 
                    genre = Genre(name=name)  
                    session.add(genre)
                genres.append(genre)      
        new_book = Book(
            title=title, 
            isbn=str(isbn), 
            author=authors, 
            published_year=published_year, 
            genre=genres,
            available_copies=available_copies,
            available=available_copies > 0
        )
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        session.expunge_all()
        return new_book

def add_member(name: str, email: str, phone: str = None) -> Member:
    """Register a new library member."""
    with Session(engine) as session: 
        new_member = Member(name=name, email=email, phone=phone)
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        session.expunge(new_member)
        return new_member

def checkout_book(book_id: int, member_id: int, days: int = 14) -> Checkout:
    """Process a book checkout for a member if available."""
    with Session(engine) as session: 
        book = session.query(Book).filter(Book.id == book_id).first()
        member = session.query(Member).filter(Member.id == member_id).first()

        if not member: 
            raise ValueError("Member does not exist.")
        if not book:
            raise ValueError("Book does not exist.")
        
        if book.available_copies > 0: 
            checkout_object = Checkout(
                book_id=book_id,
                member_id=member_id,
                checkout_date=date.today(),
                due_date=date.today() + timedelta(days=days)
            )
            book.available_copies -= 1
            if book.available_copies == 0:
                book.available = False

            session.add(checkout_object)
            session.commit()
            session.refresh(checkout_object)
            session.expunge_all()
            return checkout_object
        else: 
            raise ValueError("Book is currently unavailable.")

def return_book(checkout_id: int) -> Checkout:
    """Process a book return using the checkout ID."""
    with Session(engine) as session: 
        checkout = session.query(Checkout).filter(Checkout.id == checkout_id).first()
        if not checkout:
            raise ValueError("Invalid checkout ID.")
        if checkout.return_date is not None: 
            raise ValueError("Book has already been returned.")
        
        checkout.return_date = date.today()
        book = session.query(Book).filter(Book.id == checkout.book_id).first()
        if book:
            book.available_copies += 1
            book.available = True

        session.commit()
        session.refresh(checkout)
        session.expunge_all()
        return checkout

# ============================================================
# QUERY FUNCTIONS
# ============================================================

def get_all_books() -> list[Book]: 
    """Retrieve all library books with eager-loaded authors."""
    with Session(engine) as session: 
        books = session.query(Book).options(joinedload(Book.author)).all()
        session.expunge_all()
        return books
    
def search_books_by_title(title: str) -> list[Book]:
    """Search books matching a title string case-insensitively."""
    with Session(engine) as session:
        books = session.query(Book).options(joinedload(Book.author)).filter(Book.title.ilike(f"%{title}%")).all()
        session.expunge_all()
        return books

def find_books_by_author(author_name: str) -> list[Book]:
    """Find books written by a specific author name."""
    with Session(engine) as session: 
        books = session.query(Book).join(book_author).join(Author).filter(Author.name.ilike(f"%{author_name}%")).all()
        session.expunge_all()
        return books

def get_overdue_books() -> list[Checkout]:
    """Return all active checkouts that have passed their due date."""
    with Session(engine) as session: 
        checkouts = session.query(Checkout).options(
            joinedload(Checkout.books),
            joinedload(Checkout.members)
        ).filter(Checkout.return_date == None, Checkout.due_date < date.today()).all()
        session.expunge_all()
        return checkouts

def get_popular_genres(limit: int = 3) -> list[dict[str, Any]]:
    """Retrieve top genres based on total checkout volume."""
    with Session(engine) as session: 
        results = session.query(Genre.name, func.count(Checkout.id).label("count"))\
            .join(book_genres).join(Book).join(Checkout)\
            .group_by(Genre.id)\
            .order_by(func.count(Checkout.id).desc())\
            .limit(limit).all()
        return [{"name": name, "count": count} for name, count in results]

def get_available_books() -> list[dict[str, Any]]:
    """Get books that have available stock for checkout."""
    with Session(engine) as session:
        books = session.query(Book).filter(Book.available_copies > 0).all()
        return [{"id": b.id, "title": b.title, "copies": b.available_copies} for b in books]

def list_member_borrowings(member_id: int) -> list[Checkout]:
    """List all active, unreturned borrowings for a member."""
    with Session(engine) as session: 
        checkouts = session.query(Checkout).options(
            joinedload(Checkout.books)
        ).filter(Checkout.member_id == member_id, Checkout.return_date == None).all()
        session.expunge_all()
        return checkouts

def update_member_email(member_id: int, new_email: str) -> Member:
    """Update a member's email address safely."""
    with Session(engine) as session: 
        member = session.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise ValueError("Member not found.")
        member.email = new_email
        session.commit()
        session.refresh(member)
        session.expunge(member)
        return member

def delete_book(book_id: int) -> bool:
    """Delete a book if no active checkouts exist."""
    with Session(engine) as session: 
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError("Book not found.")
        active_checkout = session.query(Checkout).filter(Checkout.book_id == book_id, Checkout.return_date == None).first()
        if active_checkout:
            raise ValueError("Cannot delete book: active checkouts exist.")
        
        session.delete(book)
        session.commit()
        return True

def delete_member(member_id: int) -> bool:
    """Delete a member if no active checkouts exist."""
    with Session(engine) as session: 
        member = session.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise ValueError("Member not found.")
        active_checkout = session.query(Checkout).filter(Checkout.member_id == member_id, Checkout.return_date == None).first()
        if active_checkout:
            raise ValueError("Cannot delete member: active borrowings exist.")
        
        session.delete(member)
        session.commit()
        return True