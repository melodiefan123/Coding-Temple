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
print(data)

# How many students are in each course?

# What is the average score per course?

# Who are the top 3 students by score?

# What is the average hours studied for students who passed vs. didn’t pass?

# Create a "grade" column: 90+ = “A”, 80-89 = “B”, 70-79 = “C”, below 70 = “F”

# What’s the distribution of grades per course?