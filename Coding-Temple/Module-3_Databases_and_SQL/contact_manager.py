from sqlalchemy import create_engine, String, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional

engine = create_engine("sqlite:///product_catalog.db", echo = True)

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__= "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column()
    favorite: Mapped[bool] = mapped_column(default=False)
    def __repr__(self) -> str: 
        return f"Contact(id={self.id}, first_name = '{self.first_name}', last_name='{self.last_name}', email = '{self.email}', phone ={self.phone}, favorite ={self.favorite})"

Base.metadata.create_all(engine)

def add_contact(first_name, last_name, email, phone = None): 
    with Session(engine) as session: 
        contact = Contact(first_name = first_name, last_name = last_name, email = email, phone = phone)
        session.add(contact)
        session.commit()
        session.refresh(contact)
        print(f" Added {contact} {contact.id}")

def list_contacts():
    with Session(engine) as session: 
        return session.query(Contact).order_by(Contact.last_name).all()

def find_contact(email): 
    with Session(engine) as session: 
        return session.query(Contact).filter_by(email = email).first()
    
def update_phone(email, new_phone):
    with Session(engine) as session: 
        contact = session.query(Contact).filter_by(email = email).first()
        if contact: 
            contact.phone = new_phone
            session.commit()

def toggle_favorite(email): 
    with Session(engine) as session: 
        contact = session.query(Contact).filter_by(email = email).first()
        if contact: 
             contact.favorite = not contact.favorite
             session.commit()

def delete_contact(email): 
    with Session(engine) as session: 
        contact = session.query(Contact).filter_by(email = email).first()
        if contact is None: 
            print(f" Contact not found.")
            return
        session.delete(contact)
        session.commit()


add_contact("Alice", "Morgan", "alice@email.com", "555-1234")
add_contact("Ben", "Carter", "ben@email.com", "555-5678")
add_contact("Clara", "Diaz", "clara@email.com", None)
add_contact("David", "Kim", "david@email.com", "555-9012")
add_contact("Elena", "Russo", "elena@email.com", "555-3456")
list_contacts()
update_phone("david@email.com", "555-777")
toggle_favorite("elena@email.com")
delete_contact("ben@email.com")
list_contacts()