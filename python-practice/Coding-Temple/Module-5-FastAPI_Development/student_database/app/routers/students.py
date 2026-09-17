from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate, StudentPatch
from typing import Optional

router = APIRouter(prefix="/students", tags=["students"])

def get_student_or_404(student_id: int, db: Session) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# POST /students — with duplicate email handling (409)
@router.post("/", response_model=StudentResponse, status_code=201)
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

# GET /students — with grade_level and is_enrolled filters
@router.get("/", response_model=list[StudentResponse])
def list_students(
    name: Optional[str] = None,
    grade_level: Optional[int] = Query(default=None, ge=1, le=12, description="Filter by grade level (1-12)"),
    gpa: Optional[float] = Query(default=None, ge=0.0, le=4.0, description="Filter by GPA (0.0-4.0)"),
    is_enrolled: Optional[bool] = Query(default=None, description="Filter by enrollment status (true/false)"),
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


# GET /notes/{note_id} — Get a specific note
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return get_student_or_404(student_id, db)

# PUT /students/{id} — full replacement
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = get_student_or_404(student_id, db)
    for field, value in student.model_dump().items():
        setattr(db_student, field, value)
    db.commit()
    db.refresh(db_student)
    return db_student

# PATCH /students/{id} — partial update
@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(student_id: int, student: StudentPatch, db: Session = Depends(get_db)):
    db_student = get_student_or_404(student_id, db)
    update_data = student.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    db.commit()
    db.refresh(db_student)
    return db_student

# DELETE /students/{id} — with 204 response
@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = get_student_or_404(student_id, db)
    db.delete(student)
    db.commit()