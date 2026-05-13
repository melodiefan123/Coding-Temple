from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models.student import Student
from app.models.user import User
from app.schemas.student import StudentCreate, StudentResponse, StudentUpdate, StudentPatch
from typing import Optional
from app.utils.exceptions import DuplicateException, NotFoundException, AppException
from app.utils.limiter import limiter
from app.utils.security import get_current_student

router = APIRouter(prefix="/students", tags=["students"])

def get_student_or_404(student_id: int, db: Session) -> Student:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise NotFoundException("Student", student_id)
    return student

# POST /students — with duplicate email handling (409)
@router.post("/", response_model=StudentResponse, status_code=201)
@limiter.limit("20/minute")
def create_student(request: Request, student: StudentCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_student)):
    """
    Create a new student.

    - Adds a student to the database
    - Requires authentication
    - Email must be unique
    - Returns the created student
    """
    db_student = Student(**student.model_dump())
    try: 
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise DuplicateException("User", "email", student.email)
    return db_student

# GET /students — with grade_level and is_enrolled filters
@router.get("/", response_model=list[StudentResponse], responses={
        404: {"description": "Student not found"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"},
    })
@limiter.limit("60/minute")
def list_students(
    request: Request,
    name: Optional[str] = None,
    grade_level: Optional[int] = Query(default=None, ge=1, le=12, description="Filter by grade level (1-12)"),
    gpa: Optional[float] = Query(default=None, ge=0.0, le=4.0, description="Filter by GPA (0.0-4.0)"),
    is_enrolled: Optional[bool] = Query(default=None, description="Filter by enrollment status (true/false)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_student)
):
    """
    List all students.

    - Requires authentication
    - Supports filtering by grade level
    - Supports filtering by GPA
    - Supports filtering by enrollment status
    - Returns a list of students
    """
    query = db.query(Student)
    if grade_level is not None:
        query = query.filter(Student.grade_level == grade_level)
    if is_enrolled is not None:
        query = query.filter(Student.is_enrolled == is_enrolled)
    if name is not None:
        query = query.filter(Student.name == name)
    return query.all()


# GET /students/{student_id} — Get a specific student
@router.get("/{student_id}", response_model=StudentResponse,responses={
        404: {"description": "Student not found"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"},
    }, summary="retrieve by student ID")
@limiter.limit("60/minute")
def get_student(request: Request,student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_student)):
    """
    Get specific students

    - Requires authentication
    - ID must match 
    - Returns the profile of student you are looking for
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise NotFoundException("Student", student_id)
    return student

# PUT /students/{id} — full replacement
@router.put("/{student_id}", response_model=StudentResponse, responses={
        404: {"description": "Student not found"},
        401: {"description": "Unauthorized"},
        422: {"description": "Validation error"},
    }, summary="replace a student's information")
@limiter.limit("20/minute")
def update_student(request: Request,student_id: int, student: StudentUpdate, db: Session = Depends(get_db),current_user: User = Depends(get_current_student)):
    """
    Updates all students (FULL).

    - Requires authentication
    - must match student ID 
    - Full replacement of student's profile to updated information
    """
    db_student = get_student_or_404(student_id, db)
    for field, value in student.model_dump().items():
        setattr(db_student, field, value)
    db.commit()
    db.refresh(db_student)
    return db_student

# PATCH /students/{id} — partial update
@router.patch("/{student_id}", response_model=StudentResponse)
@limiter.limit("20/minute")
def patch_student(request: Request,student_id: int, student: StudentPatch, db: Session = Depends(get_db),current_user: User = Depends(get_current_student)):
    """
    Updates students profile (PARTIAL).

    - Requires authentication
    - must match student ID 
    - Updates only provided fields
    - Does not overwrite unspecified fields
    """
    db_student = get_student_or_404(student_id, db)
    update_data = student.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    db.commit()
    db.refresh(db_student)
    return db_student

# DELETE /students/{id} — with 204 response
@router.delete("/{student_id}", status_code=204, summary="delete a student")
@limiter.limit("20/minute")
def delete_student(request: Request,student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_student)):
    """
    Deletes specific students profile.

    - Requires authentication
    - Student ID must exist
    - Prevents deletion if student is enrolled
    - Permanently removes the student record
    """
    student = get_student_or_404(student_id, db)
    if student.is_enrolled:
        raise AppException( detail="Cannot delete an enrolled student")
    db.delete(student)
    db.commit()