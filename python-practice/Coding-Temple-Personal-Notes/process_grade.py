import csv

#Read student data
students = []

with open("students.csv", 'r') as file: 
    reader = csv.DictReader(file)
    for row in reader: 
        #Convert score to int and store the full record
        row['score'] = int(row['score'])
        students.append(row)

print(f"Loaded {len(students)} student records.")


#Analyze group scores by subject

subjects = {}
for student in students: 
    subject = student["subject"]
    if subject not in subjects: 
        subjects[subject] = []
    subjects[subject].append(student["score"])

#Calculate average per subject
print("\n=== Subject Averages ===")
for subject, scores in subjects.items(): 
    avg = sum(scores) / len(scores)
    print(f"{subject}: {avg:.1f} ({len(scores)} students)")


#Write results to a text file 
all_scores = [s["score"] for s in students]

with open("grade_report.txt", "w") as file:
    file.write("GRADE REPORT\n")
    file.write("=" * 40 + "\n\n")
    file.write(f"Total students:{len(students)}\n")
    file.write(f"Overall average: {sum(all_score)/len(all_scores):.1f}\n")
    file.write(f"Highest score: {max(all_scores)}\n")
    file.write(f"Lowest score: {min(all_scores)\n\n}")

    file.write("BY SUBJECT:\n")
    for subject, scores in subjects.items(): 
        avg = sum(scores)/len(scores)
        file.write(f" {subject}: {avg:.1f} avg ({len(scores)} students)\n")

print("\n Report written to grade_report.txt")

#Add letter grades and write to new csv

def get_letter_grade(score):
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"

with open("students_graded.csv", "w", newline="") as file: 
    writer = csv.DictWriter(file, fieldnames = ["name", "score", "subject", "grade"])
    writer.writeheader()

    for student in students: 
        student["grade"] = get_letter_grade(student["score"])
        writer.writerow(student)
    
print("Graded data written to students_graded.csv")
