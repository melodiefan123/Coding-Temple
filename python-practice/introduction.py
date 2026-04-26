#My first Python program
#This prints a personal introduction

print("=" * 40) # Prints a line of 40 equals signs
print("Personal Instroduction")
print("=" * 40)

#Personal details stored as variables
first_name = "Maria"
last_name = "Garcia"
age = 28
city = "Denver"
favorite_language = "Python"

#Display the introduction
print(f"Name: {first_name} {last_name}")
print(f"Age: {age}")
print(f"City: {city}")
print(f"Favorite Language: {favorite_language}")

#f-strings let you embed variables direclty in text
print("=" * 40)

print(f"\n{first_name} {last_name} is {age} years old and lives in {city}.")
print(f"They are currently learning {favorite_language} to build AI systems.")