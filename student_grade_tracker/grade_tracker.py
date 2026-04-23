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
    
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            students = []
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
# # FUNCTION 4: Generate summary report
# # ============================================================

def generate_report(students: list[dict]) -> dict:
#     """
#     Generate a class summary report.

#     Args:
#         students: The list of student dicts from load_students().

#     Returns:
#         A dict with these keys:
#             "total_students":   int — how many students
#             "class_average":    float — average of all valid averages
#             "highest_average":  float — the best average
#             "lowest_average":   float — the lowest average
#             "grade_distribution": dict — {"A": 3, "B": 5, ...}
#             "students":         list of dicts, each with:
#                                   name, average, grade
#     """
#     # TODO: For each student:
#     #   1. Extract grades (math, science, english, history values)
#     #   2. Call calculate_average()
#     #   3. Call get_letter_grade()
#     #   4. Build the student summary dict
#     # Then compute class-level stats from all the averages.
#     pass
    total_students = len(students)
    grade_distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0, "N/A": 0}
    student_summaries = []
    all_averages = []
    for student in students: 
        grades = [student['math'], student['science'], student['english'], student['history']]
        average = calculate_average(grades)
        letter_grade = get_letter_grade(average)
        student_summary = {
            "name": student['student_name'],
            "average": average,
            "grade": letter_grade
        }
        student_summaries.append(student_summary)
        grade_distribution[letter_grade] += 1
        if average is not None:
            all_averages.append(average)

    if not all_averages: 
        return None
    highest_average = float(max(all_averages))
    lowest_average = float(min(all_averages))
    class_average = round(sum(all_averages) / len(all_averages), 1)
    
    return {
        "total_students": total_students,
        "class_average": class_average,
        "highest_average": highest_average,
        "lowest_average": lowest_average,
        "grade_distribution": grade_distribution,
        "students": student_summaries
    }


    




# # ============================================================
# # FUNCTION 5: Write report to a file
# # ============================================================

def write_report(report: dict, filepath: str) -> None:
#     """
#     Write the summary report to a text file.

#     Format example:
#         ===========================
#         STUDENT GRADE REPORT
#         ===========================
#         Total students: 15
#         Class average:  81.3
#         Highest average: 95.0
#         Lowest average:  55.0

#         Grade Distribution:
#           A: 5
#           B: 4
#           ...

#         Individual Results:
#           Alice Johnson    Avg: 91.5  Grade: A
#           ...

#     Args:
#         report:   The dict returned by generate_report().
#         filepath: Path to write the report file.
#     """
#     # TODO: Open the file in write mode ("w").
#     #       Write each section with f-strings.
#     #       Use f.write() or print(..., file=f).
#     pass
    with open(filepath, 'w') as file:
        file.write("===========================\n")
        file.write("STUDENT GRADE REPORT\n")
        file.write("===========================\n")
        file.write(f"Total students: {report['total_students']}\n")
        file.write(f"Class average: {report['class_average']}\n")
        file.write(f"Highest average: {report['highest_average']}\n")
        file.write(f"Lowest average: {report['lowest_average']}\n\n")
        file.write("Grade Distribution:\n")
        for grade, count in report['grade_distribution'].items():
            file.write(f"  {grade}: {count}\n")
        file.write("\nIndividual Results:\n")
        for student in report['students']:
            avg_display = student['average'] if student['average'] is not None else "N/A"
            file.write(f"  {student['name']:<20} Avg: {avg_display} Grade: {student['grade']}\n")


# # ============================================================
# # MAIN — do not modify
# # ============================================================

def main():
    print("Loading student data...")
    students = load_students("data/students.csv")
    print(f"Loaded {len(students)} students.")

    print("Generating report...")
    report = generate_report(students)

    print("\n--- Summary ---")
    print(f"Total students:   {report['total_students']}")
    print(f"Class average:    {report['class_average']}")
    print(f"Highest average:  {report['highest_average']}")
    print(f"Lowest average:   {report['lowest_average']}")

    print("\nGrade Distribution:")
    for grade, count in sorted(report["grade_distribution"].items()):
        print(f"  {grade}: {count}")

    print("\nTop 5 students:")
    sorted_students = sorted(
        [s for s in report["students"] if s["average"] is not None],
        key=lambda s: s["average"],
        reverse=True
    )
    for s in sorted_students[:5]:
        print(f"  {s['name']:<20} {s['average']:.1f}  ({s['grade']})")

    write_report(report, "grade_report.txt")
    print("\nReport written to grade_report.txt")


if __name__ == "__main__":
    main()