"""
Module 3 Project: Library Management System
library_system.py — Database models and query functions
"""

from sqlalchemy import create_engine, String, Integer, Boolean, ForeignKey, Table, Column, Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from datetime import date, timedelta
from typing import Optional

engine = create_engine("sqlite:///library.db", echo=False)

class Base(DeclarativeBase):
    pass

# Association Table: Book <-> Genre (many-to-many)
book_genres = Table(
    "book_genres", Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

# Association Table: Book <-> Author (many-to-many)
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
    check_outs: Mapped[list["Checkout"]] = relationship(back_populates="books")

class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    membership_date: Mapped[date] = mapped_column(default=date.today)
    check_outs: Mapped[list["Checkout"]] = relationship(back_populates="members")

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

def init_db():
    """Create all database tables."""
    Base.metadata.create_all(engine)

# ============================================================
# CRUD FUNCTIONS
# ============================================================

def add_author(name: str, bio: str = None):
    with Session(engine) as session: 
        new_author = Author(name=name, bio=bio)
        session.add(new_author)
        session.commit()
        session.refresh(new_author)
        return new_author

def add_book(title: str, isbn: str, author_id: int, published_year: int = None, genre_names: list = None):
    with Session(engine) as session: 
        author = session.query(Author).filter(Author.id == author_id).first()
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
            author=[author] if author else [], 
            published_year=published_year, 
            genre=genres
        )
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        return new_book

def add_member(name: str, email: str, phone: str = None):
    with Session(engine) as session: 
        new_member = Member(name=name, email=email, phone=phone)
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        return new_member

def checkout_book(book_id: int, member_id: int, days: int = 14):
    with Session(engine) as session: 
        book = session.query(Book).filter(Book.id == book_id).first()
        if book and book.available: 
            checkout_object = Checkout(
                book_id=book_id,
                member_id=member_id,
                checkout_date=date.today(),
                due_date=date.today() + timedelta(days=days)
            )
            book.available = False
            session.add(checkout_object)
            session.commit()
            session.refresh(checkout_object)
            return checkout_object
        else: 
            raise ValueError("Book not available")

def return_book(checkout_id: int):
    with Session(engine) as session: 
        checkout = session.query(Checkout).filter(Checkout.id == checkout_id).first()
        if not checkout:
            raise ValueError("Invalid checkout ID")
        checkout.return_date = date.today()
        book = session.query(Book).filter(Book.id == checkout.book_id).first()
        if book:
            book.available = True
        session.commit()
        session.refresh(checkout)
        return checkout

# ============================================================
# QUERY FUNCTIONS
# ============================================================

def search_books_by_title(title: str) -> list:
    with Session(engine) as session:
        books = session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()
        return [b.title for b in books]

def find_books_by_author(author_name: str) -> list:
    with Session(engine) as session: 
        books = session.query(Book).join(book_author).join(Author).filter(Author.name.ilike(f"%{author_name}%")).all()
        return [{"id": b.id, "title": b.title} for b in books]

def get_overdue_books() -> list:
    with Session(engine) as session: 
        checkouts = session.query(Checkout).filter(Checkout.return_date == None, Checkout.due_date < date.today()).all()
        return [{"id": c.id, "book_id": c.book_id, "member_id": c.member_id, "due_date": c.due_date} for c in checkouts]

def get_popular_genres(limit: int = 3) -> list:
    with Session(engine) as session: 
        results = session.query(Genre).join(book_genres).join(Book).join(Checkout).group_by(Genre.id).order_by(func.count(Checkout.id).desc()).limit(limit).all()
        return [{"id": g.id, "name": g.name} for g in results]

def get_available_books() -> list:
    with Session(engine) as session:
        books = session.query(Book).filter_by(available=True).all()
        return [{"id": b.id, "title": b.title} for b in books]

def list_member_borrowings(member_id: int) -> list:
    with Session(engine) as session: 
        checkouts = session.query(Checkout).filter(Checkout.member_id == member_id, Checkout.return_date == None).all()
        return [{"id": c.id, "book_id": c.book_id, "due_date": c.due_date} for c in checkouts]

def update_member_email(member_id: int, new_email: str):
    with Session(engine) as session: 
        member = session.query(Member).filter(Member.id == member_id).first()
        if member:
            member.email = new_email
            session.commit()
            session.refresh(member)
        return member

def delete_book(book_id: int) -> bool:
    with Session(engine) as session: 
        book = session.query(Book).filter(Book.id == book_id).first()
        active_checkout = session.query(Checkout).filter(Checkout.book_id == book_id, Checkout.return_date == None).first()
        if book and not active_checkout: 
            session.query(Checkout).filter(Checkout.book_id == book_id).delete()
            session.delete(book)
            session.commit()
            return True
        return False

def delete_member(member_id: int) -> bool:
    with Session(engine) as session: 
        member = session.query(Member).filter(Member.id == member_id).first()
        active_checkout = session.query(Checkout).filter(Checkout.member_id == member_id, Checkout.return_date == None).first()
        if member and not active_checkout: 
            session.delete(member)
            session.commit()
            return True
        return False