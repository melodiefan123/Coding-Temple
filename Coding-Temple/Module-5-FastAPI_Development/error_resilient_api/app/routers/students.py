from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional

from app.database import get_db
from app.models.student import Student
from app.schemas.student_schema import StudentCreate, StudentResponse, StudentUpdate, StudentPatch
from app.exceptions import NotFoundError, DuplicateError, AppValidationError

router = APIRouter(prefix="/students", tags=["students"])


def get_student_or_404(student_id: int, db: Session) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise NotFoundError(f"Student with id {student_id} not found")
    return student


def save_student_or_raise_duplicate(db: Session, student_obj: Student, email: str):
    try:
        db.add(student_obj)
        db.commit()
        db.refresh(student_obj)
        return student_obj
    except IntegrityError:
        db.rollback()
        raise DuplicateError(f"Student with email '{email}' already exists")


# POST /students — raise DuplicateError when email exists
@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.model_dump())
    return save_student_or_raise_duplicate(db, db_student, student.email)


# GET /students
@router.get("/", response_model=list[StudentResponse])
def list_students(
    name: Optional[str] = None,
    grade_level: Optional[int] = Query(default=None, ge=1, le=12, description="Filter by grade level (1-12)"),
    gpa: Optional[float] = Query(default=None, ge=0.0, le=4.0, description="Filter by GPA (0.0-4.0)"),
    is_enrolled: Optional[bool] = Query(default=None, description="Filter by enrollment status"),
    db: Session = Depends(get_db)
):
    query = db.query(Student)
    if grade_level is not None:
        query = query.filter(Student.grade_level == grade_level)
    if is_enrolled is not None:
        query = query.filter(Student.is_enrolled == is_enrolled)
    if name is not None:
        query = query.filter(Student.name == name)
    return query.all()


# GET /students/{student_id} — uses get_student_or_404
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return get_student_or_404(student_id, db)


# PUT /students/{student_id} — full update with duplicate error handling
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = get_student_or_404(student_id, db)
    for field, value in student.model_dump().items():
        setattr(db_student, field, value)
    return save_student_or_raise_duplicate(db, db_student, student.email)


# PATCH /students/{student_id} — partial update with duplicate error handling
@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(student_id: int, student: StudentPatch, db: Session = Depends(get_db)):
    db_student = get_student_or_404(student_id, db)
    update_data = student.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    
    email_to_check = update_data.get("email", db_student.email)
    return save_student_or_raise_duplicate(db, db_student, email_to_check)


# DELETE /students/{student_id} — raise AppValidationError if enrolled
@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)
    if student.is_enrolled:
        raise AppValidationError("Cannot delete an enrolled student")
    db.delete(student)
    db.commit()