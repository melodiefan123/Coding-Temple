"""
Module 3 Project: Library Management System
library_system.py — Database models and query functions
"""

from datetime import date, timedelta
from typing import Optional
from sqlalchemy import (
    create_engine, String, Integer, Boolean, ForeignKey, 
    Table, Column, Date, func
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, 
    relationship, Session, joinedload
)

engine = create_engine("sqlite:///library.db", echo=False)

class Base(DeclarativeBase):
    pass

# Association table for Book <-> Genre (many-to-many)
book_genres = Table(
    "book_genres", Base.metadata,
    Column("book_id",  Integer, ForeignKey("books.id"),  primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

# Association table for Book <-> Author (many-to-many)
book_authors = Table(
    "book_authors", Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
)

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    books: Mapped[list["Book"]] = relationship(secondary=book_authors, back_populates="authors")

class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    books: Mapped[list["Book"]] = relationship(secondary=book_genres, back_populates="genres")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    year_published: Mapped[Optional[int]] = mapped_column()
    available: Mapped[bool] = mapped_column(default=True)
    available_copies: Mapped[int] = mapped_column(default=1)
    
    authors: Mapped[list["Author"]] = relationship(secondary=book_authors, back_populates="books")
    genres: Mapped[list["Genre"]] = relationship(secondary=book_genres, back_populates="books")
    check_outs: Mapped[list["Checkout"]] = relationship(back_populates="books")

class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    membership_date: Mapped[date] = mapped_column(default=date.today)
    check_outs: Mapped[list["Checkout"]] = relationship(back_populates="members")

class Checkout(Base):
    __tablename__ = "checkouts"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    checkout_date: Mapped[date] = mapped_column()
    return_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    due_date: Mapped[date] = mapped_column()
    
    books: Mapped["Book"] = relationship(back_populates="check_outs")
    members: Mapped["Member"] = relationship(back_populates="check_outs")

def init_db():
    """Create all database tables."""
    Base.metadata.create_all(engine)

# ============================================================
# CRUD FUNCTIONS
# ============================================================

def add_author(name: str, bio: str = None):
    """Add a new author. Returns the created Author object."""
    with Session(engine) as session: 
        new_author = Author(name=name, bio=bio)
        session.add(new_author)
        session.commit()
        session.refresh(new_author)
        session.expunge(new_author)
        return new_author

def add_book(title: str, isbn: str, author_ids: list[int] | int, year_published: int = None, genre_names: list = None):
    """Add a new book. Assigns authors and genres."""
    with Session(engine) as session: 
        genres = []
        if genre_names: 
            for name in genre_names: 
                genre = session.query(Genre).filter(Genre.name == name).first()
                if not genre: 
                    genre = Genre(name=name)  
                    session.add(genre)
                genres.append(genre)

        if isinstance(author_ids, int):
            author_ids = [author_ids]

        authors = session.query(Author).filter(Author.id.in_(author_ids)).all()

        new_book = Book(
            title=title, 
            isbn=isbn, 
            authors=authors, 
            year_published=year_published, 
            genres=genres
        )
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        session.expunge_all()
        return new_book

def add_member(name: str, email: str, phone: str = None):
    """Register a new borrower. Returns the created Member object."""
    with Session(engine) as session: 
        new_member = Member(name=name, email=email, phone=phone)
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        session.expunge(new_member)
        return new_member

def checkout_book(book_id: int, member_id: int, days: int = 14):
    """Check out a book. Sets book.available = False."""
    with Session(engine) as session: 
        book = session.query(Book).filter(Book.id == book_id).first()
        
        if book and book.available: 
            checkout_object = Checkout(
                book_id=book.id, 
                checkout_date=date.today(),
                due_date=date.today() + timedelta(days=days), 
                member_id=member_id
            )
            book.available = False
            session.add(checkout_object)
            session.commit()
            result = session.query(Checkout).options(joinedload(Checkout.books)).filter(Checkout.id == checkout_object.id).first()
            session.expunge_all()
            return result
        else: 
            raise ValueError("Book not available")

def search_books_by_title(title: str) -> list:
    """Return all books whose title contains the search string."""
    with Session(engine) as session:
        books = session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()
        return [book.title for book in books]

def return_book(checkout_id: int):
    """Return a book. Sets book.available = True, sets return_date = today."""
    with Session(engine) as session: 
        checkout = session.query(Checkout).options(joinedload(Checkout.books)).filter(Checkout.id == checkout_id).first()
        if not checkout: 
            raise ValueError(f"No checkout record found with ID {checkout_id}.")
        checkout.return_date = date.today()
        checkout.books.available = True
        session.commit()
        session.expunge_all()
        return checkout

# ============================================================
# QUERY FUNCTIONS
# ============================================================

def find_books_by_author(author_name: str) -> list:
    """Return all books whose author name contains author_name."""
    with Session(engine) as session: 
        books = session.query(Book).join(Book.authors).filter(Author.name.ilike(f"%{author_name}%")).options(joinedload(Book.authors)).all()
        session.expunge_all()
        return books

def get_overdue_books() -> list:
    """Return all Checkout objects where due_date < today and return_date is None."""
    with Session(engine) as session: 
        overdue = session.query(Checkout).options(
            joinedload(Checkout.books),
            joinedload(Checkout.members)
        ).filter(
            Checkout.return_date == None,
            Checkout.due_date < date.today()
        ).all()
        session.expunge_all()
        return overdue

def get_popular_genres(limit: int = 3) -> list:
    """Return the top `limit` genres by checkout count."""
    with Session(engine) as session: 
        results = (
            session.query(Genre)
            .join(book_genres)
            .join(Book)
            .join(Checkout)
            .group_by(Genre.id, Genre.name)
            .order_by(func.count(Checkout.id).desc())
            .limit(limit)
            .all()
        )
        session.expunge_all()
        return results

def get_available_books() -> list:
    """Return all Book objects where available == True."""
    with Session(engine) as session:
        books = session.query(Book).filter_by(available=True).all()
        return [{"id": b.id, "title": b.title} for b in books]

def list_all_books() -> list:
    """Return all Book objects in the database."""  
    with Session(engine) as session: 
        books = session.query(Book).all()
        session.expunge_all()
        return books

def list_member_borrowings(member_id: int) -> list:
    """Return all Checkout objects for a given member_id."""
    with Session(engine) as session: 
        borrowings = session.query(Checkout).options(joinedload(Checkout.books)).filter(Checkout.member_id == member_id, Checkout.return_date == None).all()
        session.expunge_all()
        return borrowings

def update_member_email(member_id: int, new_email: str):
    """Update a member's email address."""
    with Session(engine) as session: 
        member = session.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise ValueError("Member not found")
        member.email = new_email
        session.commit()
        session.refresh(member)
        session.expunge(member)
        return member

def delete_book(book_id: int):
    """Delete a book from the database."""
    with Session(engine) as session: 
        book = session.query(Book).filter(Book.id == book_id).first()
        checkouts = session.query(Checkout).filter(Checkout.return_date == None, Checkout.book_id == book_id).all()
        all_checkouts = session.query(Checkout).filter(Checkout.book_id == book_id).all()
        if book: 
            if checkouts: 
                return False
            for checkout in all_checkouts: 
                session.delete(checkout)
            session.delete(book)
            session.commit()
            return True
        return False

def delete_member(member_id: int):
    """Delete a member from the database."""
    with Session(engine) as session: 
        member = session.query(Member).filter(Member.id == member_id).first()
        checkouts = session.query(Checkout).filter(Checkout.return_date == None, Checkout.member_id == member_id).all()
        
        if member: 
            if checkouts: 
                return False
            session.delete(member)
            session.commit()
            return True
        return False