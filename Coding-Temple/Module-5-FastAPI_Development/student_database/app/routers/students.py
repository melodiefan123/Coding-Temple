from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.student import (
    StudentCreate,
    StudentPatch,
    StudentResponse,
    StudentUpdate,
)

router = APIRouter(prefix="/students", tags=["students"])


def get_student_or_404(student_id: int, db: Session) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# POST /students — Create student with duplicate email handling (409)
@router.post("", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.model_dump())
    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")
    return db_student


# GET /students — List students with major and min_gpa filters
@router.get("", response_model=list[StudentResponse])
def list_students(
    major: Optional[str] = Query(
        default=None, description="Filter by major (case-insensitive)"
    ),
    min_gpa: Optional[float] = Query(
        default=None, ge=0.0, le=4.0, description="Filter by minimum GPA (0.0-4.0)"
    ),
    db: Session = Depends(get_db),
):
    query = db.query(Student)
    if major is not None:
        query = query.filter(Student.major.ilike(f"%{major}%"))
    if min_gpa is not None:
        query = query.filter(Student.gpa >= min_gpa)
    return query.all()


# GET /students/{id} — Retrieve student by ID
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return get_student_or_404(student_id, db)


# PUT /students/{id} — Full replacement with duplicate email handling
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student: StudentUpdate, db: Session = Depends(get_db)
):
    db_student = get_student_or_404(student_id, db)
    for field, value in student.model_dump().items():
        setattr(db_student, field, value)

    try:
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")

    return db_student


# PATCH /students/{id} — Partial update with duplicate email handling
@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(
    student_id: int, student: StudentPatch, db: Session = Depends(get_db)
):
    db_student = get_student_or_404(student_id, db)
    update_data = student.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_student, field, value)

    try:
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")

    return db_student


# DELETE /students/{id} — Delete student and return success message dict
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}