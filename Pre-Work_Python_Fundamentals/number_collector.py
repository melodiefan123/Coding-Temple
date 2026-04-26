try:
    question_1 = input("Enter a number:")
    question_2 = input("Enter another number:")
    question_3 = input("Enter one more number:")
    sum = int(question_1) + int(question_2) + int(question_3)
    average = float(sum / 3)

    
    print(f"\nYour numbers: {question_1}, {question_2}, {question_3}")
    print(f"Sum: {sum}")
    print(f"Average: {average}")
except ValueError:
    print("Invalid input. Please enter a valid number.")