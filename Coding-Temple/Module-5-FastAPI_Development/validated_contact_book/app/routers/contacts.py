from fastapi import APIRouter, HTTPException
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse, Category
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/contacts", tags=["contacts"])
contacts_db = []
next_contact_id = 1

@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate):
    global next_contact_id
    contact_dict = contact.model_dump()
    contact_dict["category"] = contact.category.value
    contact_dict["id"] = next_contact_id
    contact_dict["created_at"] = datetime.now().isoformat()
    contacts_db.append(contact_dict)
    next_contact_id += 1
    return contact_dict

@router.get("/", response_model=list[ContactResponse])
def list_contacts(category: Optional[Category] = None):
    if category:
        return [contact for contact in contacts_db if contact["category"] == category.value]
    return contacts_db

@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    for contact in contacts_db:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")

@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact_update: ContactUpdate):
    for contact in contacts_db:
        if contact["id"] == contact_id:
            contact.update(contact_update.model_dump(exclude_unset=True))
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")