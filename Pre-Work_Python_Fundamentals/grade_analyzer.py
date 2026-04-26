scores = [88, 45, 92, 67, 73, 95, 81, 56, 78, 100, 62, 85, 90, 38, 71]

grades = {'A': 0, 'B': 0,'C': 0,'D': 0,'F': 0 }
for score in scores:
    if score >= 90:
        grades['A'] += 1
    elif score >= 80:
        grades['B'] += 1
    elif score >= 70:
        grades['C'] += 1
    elif score >=60:
       grades['D'] += 1
    else:
       grades['F'] += 1
    



#Display Output
print("=== Grade Analyzer ===")
print(f"Total scores: {len(scores)}")
print(f"Average: {sum(scores)/len(scores):.1f}")
print(f"Highest: {max(scores)}")
print(f"Lowest: {min(scores)}")
print(f"Passing: {grades['A']+grades['B']+grades['C']+grades['D']} ({((grades['A']+grades['B']+grades['C']+grades['D'])/len(scores))*100:.1f})%")
print(f"Failing: {grades['F']} ({(grades['F']/len(scores)*100)})%")

print("\nGrade Distribution: ")
for key, value in grades.items():
    print(f"{key}: {value} students")

print("\n--- Add More Scores ---")

while True:
    score_add = input("Enter a score (or 'done' to finish):")

    if score_add == "done": 
        print("Exiting program")
        break
    try: 
        converted_score = int(score_add)
        scores.append(converted_score)
        print(f"Updated average: {sum(scores)/len(scores):.1f}")
    except ValueError: 
        print("Please enter a valid integer.")

print(f"Final average: {sum(scores)/len(scores):.1f}")








