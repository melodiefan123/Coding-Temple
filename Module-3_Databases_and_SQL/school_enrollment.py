from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import Optional

engine = create_engine("sqlite:///school_enrollment.db", echo = True)

class Base(DeclarativeBase):
    pass

student_courses = Table("student_courses", Base.metadata, Column("student_id", Integer, ForeignKey("students.id"),primary_key=True),
                        Column("course_id", Integer, ForeignKey("courses.id"),primary_key=True))

class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    teachers: Mapped[list["Teacher"]] = relationship("Teacher",back_populates="department")
    def __repr__(self):
        return f"Department(name: '{self.name}')"

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    department: Mapped["Department"] = relationship(back_populates="teachers")
    courses: Mapped[list["Course"]] = relationship(back_populates="teacher")
    def __repr__(self):
        return f"Teacher(name: '{self.name}')"
    

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    teacher_id: Mapped[str] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["Teacher"] = relationship("Teacher",back_populates="courses")
    enrolled: Mapped[list["Student"]] = relationship("Student",secondary=student_courses, back_populates="course")
    def __repr__(self):
        return f"Course(name: '{self.title}')"


class Student(Base): 
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    course: Mapped[list["Course"]] = relationship("Course",secondary= student_courses,back_populates="enrolled")
    def __repr__(self):
        return f"Student(name: '{self.name}', email:'{self.email}')"

Base.metadata.create_all(engine)
print("Tables Created!\n")
# Populate with sample data: 2+ departments, 4+ teachers, 5+ courses, 6+ students with various enrollments.
with Session(engine) as session: 
    #Departments
    history = Department(name="History")
    math = Department(name="Math")

    # Teachers
    smith =Teacher(name="Dr. Smith", department_id=1)
    jones = Teacher(name="Dr. Jones", department_id=1)
    garcia = Teacher(name="Prof. Garcia", department_id=2)
    lee = Teacher(name="Prof. Lee", department_id=2)

    # Courses
    bio = Course(title="Biology 101", teacher_id=1)
    chem = Course(title="Chemistry 101", teacher_id=2)
    algebra = Course(title="Algebra", teacher_id=3)
    calculus = Course(title="Calculus", teacher_id=4)
    stats = Course(title="Statistics", teacher_id=3)

    # Students
    alice = Student(name="Alice Brown", email="alice@school.com")
    ben = Student(name="Ben Davis", email="ben@school.com")
    clara = Student(name="Clara Evans", email="clara@school.com")
    david = Student(name="David Frank", email="david@school.com")
    elena = Student(name="Elena Green", email="elena@school.com")
    felix = Student(name="Felix Harris", email="felix@school.com")

    chem.enrolled.append(david)
    bio.enrolled.append(felix)
    calculus.enrolled.append(clara)
    stats.enrolled.append(ben)
    algebra.enrolled.append(alice)
    chem.enrolled.append(elena)
    algebra.enrolled.append(david)
    stats.enrolled.append(felix)
    algebra.enrolled.append(elena)
    algebra.enrolled.append(felix)

    session.add_all([history, math, smith, jones, garcia, lee, bio, chem, algebra, calculus, stats, alice, ben, clara, david, elena, felix])
    session.commit()
    print("Data created.\n")


with Session(engine) as session: 

    # Print each department and its teachers
    print("\nDepartment Vs Teachers")
    departments = session.query(Department).all()
    for department in departments:
        print(f"\n{department.name} - {department.teachers}")

    # Print each teacher and the courses they teach
    print("\nTeacher vs Courses")
    teachers = session.query(Teacher).all()
    for teacher in teachers: 
        print(f"\n{teacher.name} - {teacher.courses}")
    # Print each course with its enrolled students
    print("\n Courses vs Enrolled")
    courses = session.query(Course).all()
    for course in courses: 
        print(f"\n{course.title} - {course.enrolled}")
    # Print each student and the courses they're enrolled in
    print("\n Student vs Courses")
    students = session.query(Student).all()
    for student in students: 
        print(f"\n{student.name} - {student.course}")
    # Find and print any course with more than 3 students
    print("\n Popular Courses (3+)")
    courses = session.query(Course).all()
    found = False
    for course in courses: 
        if len(course.enrolled) > 3: 
            print(f"\n{course.title}")
            found = True
    if not found:
        print("There are no courses with more than 3 students.")

