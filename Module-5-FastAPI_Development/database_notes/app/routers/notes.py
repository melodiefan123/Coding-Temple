from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.note import Note 
from app.schemas.note import NoteCreate, NoteResponse
from typing import Optional

router = APIRouter(prefix="/notes", tags=["notes"])

# POST /notes — Create a note (persists to database)
@router.post("/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(
        title=note.title,
        content=note.content,
        category=note.category,
        is_pinned=note.is_pinned
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# GET /notes — List notes with optional category filter and is_pinned filter
@router.get("/", response_model=list[NoteResponse])
def list_notes(
    category: Optional[str] = None,
    is_pinned: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Note)
    if category:
        query = query.filter(Note.category == category)
    if is_pinned is not None:
        query = query.filter(Note.is_pinned == is_pinned)
    return query.all()
# GET /notes/{note_id} — Get a specific note
@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
# DELETE /notes/{note_id} — Delete a note
@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()