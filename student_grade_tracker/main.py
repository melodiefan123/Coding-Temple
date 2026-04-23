from grade_utils import load_students, calculate_average, get_letter_grade

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
    if not students:
        return {
            "total_students": 0,
            "class_average": None,
            "highest_average": None,
            "lowest_average": None,
            "grade_distribution": {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0, "N/A": 0},
            "students": []
        }
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
         return {
        "total_students": total_students,
        "class_average": None,
        "highest_average": None,
        "lowest_average": None,
        "grade_distribution": grade_distribution,
        "students": student_summaries
        }
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