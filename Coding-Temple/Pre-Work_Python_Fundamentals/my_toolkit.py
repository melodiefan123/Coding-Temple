#Average Function 
def calculate_average(numbers):
    """Takes a list of numbers, returns the average. Returns 0 if the list is empty."""
    if not numbers: 
        return "0"
    return sum(numbers)/len(numbers)
    

#Max and Min
def find_max_and_min(numbers):
    """Takes a list of numbers, returns a tuple"""    
    max_guess = numbers[0]
    min_guess = numbers[0]
    for num in numbers: 
        if max_guess < num:
            max_guess = num
        elif min_guess > num: 
            min_guess = num

    return (max_guess, min_guess)

#Count Occurrences
def count_occurrences(items, target):
    """Takes a list and a target value, returns how many times the target appears in the list."""
    count = 0 
    for item in items:
        if item == target: 
            count += 1
    return count 

#Palindrome Test
def is_palindrome(text):
    """Takes a string, returns True if it reads the same forward and backward (case-insensitive, ignoring spaces)."""
    texts = text.lower().replace(" ", "")
    reversed_text = text.lower().replace(" ", "")[::-1]
    if texts == reversed_text: 
        return True
    else: 
        return False


#Create Report
def create_report(title, scores):
    """Takes a report title and a list of scores."""
    max_min = find_max_and_min(scores)
    return f"{title} \nAverage: {calculate_average(scores):.2f} \nMax: {max_min[0]} \nMin: {max_min[1]}"



#Tests

if __name__ == "__main__":
    # Test each function
    test_scores = [85, 92, 78, 95, 88, 70, 93]
    
    print(f"Average: {calculate_average(test_scores):.2f}")
    print(f"Max/Min: {find_max_and_min(test_scores)}")
    print(f"Count of 85: {count_occurrences(test_scores, 85)}")
    print(f"'racecar' palindrome: {is_palindrome('racecar')}")
    print(f"'hello' palindrome: {is_palindrome('hello')}")
    print()
    print(create_report("Class Scores", test_scores))
        