import pandas as pd

data = {
    "student": ["Alice", "Bob", "Charlie", "Diana", "Eve",
                 "Frank", "Grace", "Henry", "Iris", "Jack"],
    "course": ["Python", "Python", "SQL", "SQL", "Python",
               "SQL", "Python", "SQL", "Python", "SQL"],
    "score": [92, 78, 85, 91, 88, 72, 95, 68, 84, 90],
    "hours_studied": [20, 12, 18, 22, 15, 8, 25, 10, 16, 19],
    "passed": [True, True, True, True, True, False, True, False, True, True],
}

df = pd.DataFrame(data)
# print(data)

# How many students are in each course?
print("\n" + "=" * 60)
print("Q1 — Students per course (value_counts)")
print("=" * 60)
course = df.groupby("course")['student'].count()
print(course.to_string())

# What is the average score per course?
print("\n" + "=" * 60)
print("Q2 — Average score per course (groupby + mean)")
print("=" * 60)
avg_score = df.groupby('course')['score'].mean()
print(avg_score.to_string())


# Who are the top 3 students by score?
print("\n" + "=" * 60)
print("Q3 — Top 3 students by score (nlargest)")
print("=" * 60)
top_students = df.sort_values("score", ascending=False)['student'].iloc[0:3]
print(top_students.to_string())
# What is the average hours studied for students who passed vs. didn’t pass?
print("\n" + "=" * 60)
print("Q4 — Avg hours studied by pass/fail (groupby on boolean)")
print("=" * 60)
avg_hours = df.groupby('passed')['hours_studied'].mean()
print(avg_hours.to_string())
# Create a "grade" column: 90+ = “A”, 80-89 = “B”, 70-79 = “C”, below 70 = “F”
print("\n" + "=" * 60)
print("Q5 — Add 'grade' column (pd.cut for grade bands)")
print("=" * 60)

def assign_grade(score):
    if score >=90: 
        return "A"
    elif score >= 80: 
        return "B"
    elif score >= 70: 
        return "C"
    else: 
        return "F"

df['grade'] = df["score"].apply(assign_grade)
print(df[["student", "score", "grade"]].to_string())

# What’s the distribution of grades per course?
print("\n" + "=" * 60)
print("Q6 — Grade distribution per course (groupby + value_counts + unstack)")
print("=" * 60)
grade_distribution = df.groupby(["course", "grade"]).size()

print(grade_distribution.to_string())