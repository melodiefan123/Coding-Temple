# In your main block, demonstrate each function:
# Add at least 4 students
# Print all students
# Update one student's GPA
# Delete one student
# Print all students again to confirm changes

import sqlite3

connection = sqlite3.connect("school.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""CREATE TABLE students(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               name TEXT NOT NULL, 
               grade INTEGER NOT NULL, 
               gpa REAL)""")

def add_student(name, grade, gpa): 
    cursor.execute("INSERT INTO students(name, grade, gpa) VALUES(?,?,?)", (name, grade, gpa))
    connection.commit()

def get_all_students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()

def get_student_by_id(student_id):
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    return cursor.fetchone()

def update_student_gpa(student_id, new_gpa):
    cursor.execute("UPDATE students SET gpa = ? WHERE id = ?", (new_gpa, student_id))
    connection.commit()
      
def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    connection.commit()

if __name__ == "__main__": #am I being run directly, or being imported?"
    add_student("student 1", 8, 3.5)
    add_student("student 2", 9, 4.5)
    add_student("student 3", 10, 3.0)
    add_student("student 4", 11, 2.5)
    print(get_all_students())
    update_student_gpa(1, 4.5)
    delete_student(2)
    print(get_all_students())


