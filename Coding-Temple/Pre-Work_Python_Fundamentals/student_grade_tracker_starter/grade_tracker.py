"""
Project: Student Grade Tracker
Pre-Work Section C — Python Fundamentals

Objective: Build a data processing script that reads student grades from
a CSV, calculates averages, assigns letter grades, and writes a summary report.
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

    Args:
        filepath: Path to the CSV file.

    Returns:
        A list of dicts, one per student, or an empty list if the file is missing.
    """
    students = []
    try:
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(dict(row))
    except FileNotFoundError:
        print(f"File not found: {filepath}. Check that you're running the script from the project root folder.")
        return []
    return students


# ============================================================
# FUNCTION 2: Calculate average, handling missing values
# ============================================================

def calculate_average(grades: list) -> float | None:
    """
    Calculate the average of a list of grade values.

    Grade values may be strings, empty strings, or numbers.
    Ignores any value that cannot be converted to a float.

    Args:
        grades: A list of values (e.g., ["92", "88", "", "79"]).

    Returns:
        The average as a float rounded to 1 decimal place, or None if no valid grades exist.
    """
    valid_grades = []
    for grade in grades:
        if grade is None or str(grade).strip() == "":
            continue
        try:
            valid_grades.append(float(grade))
        except ValueError:
            continue

    if not valid_grades:
        return None

    return round(sum(valid_grades) / len(valid_grades), 1)


# ============================================================
# FUNCTION 3: Assign letter grade
# ============================================================

def get_letter_grade(average: float | None) -> str:
    """
    Convert a numeric average to a letter grade.

    Scale:
        90+   → "A"
        80-89 → "B"
        70-79 → "C"
        60-69 → "D"
        < 60  → "F"
        None  → "N/A"

    Args:
        average: The numeric average, or None.

    Returns:
        The letter grade as a string.
    """
    if average is None:
        return "N/A"
    elif average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


# ============================================================
# FUNCTION 4: Generate summary report
# ============================================================

def generate_report(students: list[dict]) -> dict:
    """
    Generate a class summary report.

    Args:
        students: The list of student dicts from load_students().

    Returns:
        A dict containing total_students, class_average, highest_average,
        lowest_average, grade_distribution, and individual student results.
    """
    total_students = len(students)
    grade_distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0, "N/A": 0}
    student_summaries = []
    all_averages = []

    # Defined outside the loop to improve performance
    subjects = ['math', 'science', 'english', 'history']

    for student in students:
        grades = [student.get(sub) for sub in subjects]
        average = calculate_average(grades)
        letter_grade = get_letter_grade(average)

        student_summary = {
            "name": student.get('student_name', 'Unknown'),
            "average": average,
            "grade": letter_grade
        }
        student_summaries.append(student_summary)

        grade_distribution[letter_grade] += 1
        if average is not None:
            all_averages.append(average)

    if all_averages:
        class_average = round(sum(all_averages) / len(all_averages), 1)
        highest_average = float(max(all_averages))
        lowest_average = float(min(all_averages))
    else:
        class_average = None
        highest_average = None
        lowest_average = None

    return {
        "total_students": total_students,
        "class_average": class_average,
        "highest_average": highest_average,
        "lowest_average": lowest_average,
        "grade_distribution": grade_distribution,
        "students": student_summaries
    }


# ============================================================
# FUNCTION 5: Write report to a file
# ============================================================

def write_report(report: dict, filepath: str) -> None:
    """
    Write the summary report to a formatted text file.

    Args:
        report:   The dict returned by generate_report().
        filepath: Path to write the report file.
    """
    with open(filepath, "w") as file:
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
            avg_display = f"{student['average']:.1f}" if student['average'] is not None else "N/A"
            file.write(f"  {student['name']:<20} Avg: {avg_display:<5} Grade: {student['grade']}\n")


# ============================================================
# MAIN — do not modify
# ============================================================

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