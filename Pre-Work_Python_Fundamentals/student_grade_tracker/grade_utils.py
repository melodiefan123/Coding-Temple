"""
Project: Student Grade Tracker
Pre-Work Section C — Python Fundamentals
Estimated time: 45-60 minutes

Objective: Build a data processing script that reads student grades from
a CSV, calculates averages, assigns letter grades, and writes a summary report.

Your job: implement all the functions marked with # TODO.
Do NOT modify the function signatures or the main() function.
"""

import csv


# ============================================================
# FUNCTION 1: Load data from CSV
# ============================================================

def load_students(filepath: str) -> list[dict]:
    """
    Read student data from a CSV file.

    Each row becomes a dictionary. The CSV has columns:
    student_name, math, science, english, history

    Some cells may be empty strings (missing grades) — that's expected.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of dicts, one per student.
        Example: [{"student_name": "Alice", "math": "92", ...}, ...]

    Raises:
        FileNotFoundError: if the CSV file doesn't exist.
    """
    # TODO: Open the file with open(), use csv.DictReader to read rows,
    #       return a list of dicts.
    #       Hint: use "with open(filepath) as f:" and a list comprehension
    #       or a for loop to collect rows.
    students = []
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader: 
                row['math'] = int(row['math']) if row['math'] else None
                row['science'] = int(row['science']) if row['science'] else None
                row['english'] = int(row['english']) if row['english'] else None
                row['history'] = int(row['history']) if row['history'] else None
                students.append(row)
    except FileNotFoundError: 
        print("File not found. Please check the filename.")
    except ValueError:
        print("Please enter a valid number for grades.")
    return students

# TEST ONLY print(load_students('data/students.csv'))
# ============================================================
# FUNCTION 2: Calculate average, handling missing values
# ============================================================

def calculate_average(grades: list) -> float | None:
#     """
#     Calculate the average of a list of grade values.

#     Grade values may be strings (from the CSV), empty strings, or numbers.
#     Ignore any value that can't be converted to a float.

#     Args:
#         grades: A list of values (e.g., ["92", "88", "", "79"]).

#     Returns:
#         The average as a float, rounded to 1 decimal place.
#         Returns None if there are no valid grades.
#     """
#     # TODO: Convert each item to float using try/except.
#     #       Skip items that raise ValueError or are empty strings.
#     #       If the resulting list is empty, return None.
#     #       Otherwise return round(sum / count, 1).
    try:
        valid_grades=[]
       
        for grade in grades: 
            if grade is not None: 
                valid_grades.append(grade)
        if not valid_grades: 
            return None
        total_sum = sum(valid_grades)
        count = len(valid_grades)
        average = total_sum / count 
        return round(average, 1)
    except ValueError:
        print("Please enter a valid number.")


# # ============================================================
# # FUNCTION 3: Assign letter grade
# # ============================================================

def get_letter_grade(average: float | None) -> str:
#     """
#     Convert a numeric average to a letter grade.

#     Scale:
#         90+  → "A"
#         80-89 → "B"
#         70-79 → "C"
#         60-69 → "D"
#         < 60  → "F"
#         None  → "N/A" (no grades available)

#     Args:
#         average: The numeric average, or None.

#     Returns:
#         The letter grade as a string.
#     """
#     # TODO: Use if/elif/else to return the correct letter grade.
#     pass
    if average is None: 
        return "N/A"
    elif average >= 90: 
        return "A"
    elif average >= 80:
        return "B"
    elif average >=70: 
        return "C"
    elif average >= 60: 
        return "D"
    else:
        return "F"


# # ============================================================
# # FUNCTION 4: Add Students With Validation
# # ============================================================

def add_student(students: list[dict]) -> list[dict]:
    """
    Prompt the user to enter a new student's name and grades, then add that student to the list.

    The function should:
        1. Ask for the student's name.
        2. For each subject (math, science, english, history), ask for a grade.
           - If the user enters an empty string, treat it as missing (None).
           - If the user enters a non-numeric value, show an error and ask again.
        3. Create a student dict and append it to the students list.

    Args:
        students: The list of student dicts to which the new student will be added. 
    """
    user_prompt = input("Would you like to add a new student? (yes/no): ").strip().lower()
    if user_prompt == 'yes' or user_prompt == 'y':
        student_name = input("Enter the student's name: ").strip()
        subjects = ['math', 'science', 'english', 'history']
        new_student = {"student_name": student_name}
        for subject in subjects:
            while True:
                try:
                    grade_input = input(f"Enter {student_name}'s grade (percentage) for {subject} (or leave blank if missing): ").strip()
                    grade_input = int(grade_input) if grade_input else None
                    if grade_input is None:
                        new_student[subject] = None
                        break
                    if grade_input >= 0 and grade_input <= 100:
                        new_student[subject] = grade_input
                        break
                    else: 
                        print("Grade must be between 0 and 100. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a numeric grade or leave blank.")
        students.append(new_student)
    else: 
        print("No new student added.")
    return students