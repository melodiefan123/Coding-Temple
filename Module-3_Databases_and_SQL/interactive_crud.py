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

#command line 
print("\nStudent Roster Manager")
while True: 
    choices = input("1.Add a student\n2.View all students\n3.Update a student's GPA\n4.Delete a student\n5. Quit\n Enter your choice:")

    if choices == "1": 
        name = input("Enter the student's name:")
        grade = int(input("Enter the student's grade:"))
        gpa = round(float(input("Enter the students gpa")), 1)
        if gpa > 5: 
            print(f"Please enter a GPA less than 5.")
            continue
        add_student(name, grade, gpa)
    elif choices == "2": 
        print(get_all_students())
    elif choices == "3":
        student_id = int(input("Enter the student ID:"))
        gpa = round(float(input("Enter the students new gpa")), 1)
        if gpa > 5: 
            print(f"Please enter a GPA less than 5.")
            continue
        update_student_gpa(student_id, gpa)
    elif choices == "4":
        student_id = int(input("Enter the student ID you'd like to delete:"))
        delete_student(student_id)
    else:
        print("Exiting Program")
        connection.close()
        break


