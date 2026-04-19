

print("="*45)
print("                 MyTo-Do List")
print("="*45)

tasks = ["Buy groceries", "Finish homework", "Call the dentist"]
count = 0


total_tasks = len(tasks)

for task in tasks:
    count +=1
    print(f"{count}.{task}")

print(f"\nTotal tasks: {total_tasks}")

user_question = input("\nWhat would you like to do? \n 1.Add a task\n 2. Remove a task\n\n Choice:")

if user_question == "1": 
    new_task = input("Enter new task:")
    # print("Choice: 1")
    # print(f"Enter new task: {new_task}")
    tasks.append(new_task)
elif user_question == "2":
    remove_task = input("Enter task to remove:")
    try:
        tasks.remove(remove_task)
    except ValueError:
        print(f"'{remove_task}' not found in your list.")
    else: 
        print("Invalid choice. Please enter 1 or 2.")


print(f"\nUpdated list:")
count = 0 
for task in tasks:
    count +=1
    print(f"{count}.{task}")

total_tasks = len(tasks)
print(f"\nTotal tasks: {total_tasks}")

