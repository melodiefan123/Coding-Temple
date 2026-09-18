# buggy_program.py — Contains 4 bugs. Find and fix them all.

def calculate_stats(numbers) #SyntaxError: There's no ':' for the function [with help of AI]
    total = sum(numbers)
    count = len(numbers)
    average = total / count
    
    above_average = []
    for num in numbers:
        if num > average: #SyntaxError: There's no ':' after the if statement [Found myself]
            above_average.append(num)
    
    return {
        "total": total,
        "average": average, 
        "above_average": above_average,
        "above_count": len(above_average)
    }

scores = [85, 92, 78, 95, 88, 70, 93] #TypeError: can't add a string to numbers [Found myself]
result = calculate_stats(scores)

print(f"Total: {result['total']}")
print(f"Average: {result['average']}") #NameError: should be in string keys [With help of AI]
print(f"Above average: {result['above_count']} scores")