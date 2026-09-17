# grade_functions.py

def get_letter_grade(score):
    """Convert a numeric score to a letter grade."""
    if score >= 90: 
        return "A"
    elif score >= 80:
        return "B"
    elif score >=70: 
        return "C"
    elif score >= 60: 
        return "D"
    else:
        return "F"

def calculate_stats(scores):
    """Calculate basic statistics for a list of scores. Returns a dictionary with average, highest, lowest, and count."""
    if not scores: #Handle empty list
        return {"average": 0, "highest": 0, "lowest": 0, "count": 0}
    
    return{
        "average": sum(scores) / len(scores),
        "highest": max(scores),
        "lowest": min(scores),
        "count": len(scores)
    }

def count_grades(scores):
    """Count how many scores fall into each letter grade"""
    counts = {'A': 0, 'B': 0,'C': 0,'D': 0,'F': 0}
    for score in scores: 
        grade = get_letter_grade(score) #Reuse our other function
        counts[grade] += 1
    return counts

def display_reports(scores):
    """Display a complete grade report"""
    stats = calculate_stats(scores)
    grades = count_grades(scores)
    passing = sum(1 for s in scores if s >= 60)

    print("=== Grade Report ===")
    print(f"Total scores: {stats['count']}")
    print(f"Average: {stats['average']:.1f}")
    print(f"Highest: {stats['highest']}")
    print(f"Lowest: {stats['lowest']}")
    print(f"Passing: {passing} ({passing/stats['count']*100:.0f}%)")
    print()
    print("Grade Distribution:")
    for grade, count in grades.items():
        print(f" {grade}: {count} students")

#Main program - clean and simple
scores = [88, 45, 92, 67, 73, 95, 81, 56, 78, 100, 62, 85, 90, 38, 71]

display_reports(scores)

#Test individual functions
print(f"\nScore 85 = {get_letter_grade(85)}")
print(f"Score 42 = {get_letter_grade(42)}")

#Calculate stats for a different set
honors_scores = [92,95,98,91,100]
honors_stats = calculate_stats(honors_scores)
print(f"\nHonors average: {honors_stats['average']:.1f}")