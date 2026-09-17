#guessing_game.py
import random 
play_again = "yes"

while play_again.lower() in ["yes", "y"]:

    #Generate a randome number between 1 and 100
    secret = random.randint(1,100)
    attempts = 0 
    max_attempts = 7

    print("=== Number Guessing Game ===")
    print(f"I'm thinking of a number between 1 and 100.")
    print(f"You have {max_attempts} attempts.")
    print()

    while attempts < max_attempts: 
        #Get the player's guess with error handling 
        try: 
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts}:"))
        except ValueError: 
            print("Please enter a valid number.")
            continue #Don't count invalid input as an attempt
        
        attempts += 1

        #Check the guess
        if guess == secret: 
            print(f"\\nYou got it in {attempts} attempts!")
            break
        elif guess < secret: 
            print("Too low!")
        else:
            print("Too high!")
        
        #Show remaining attempts
        remaining = max_attempts - attempts
        if remaining > 0: 
            print(f"({remaining} attempts remaining)")

    #This runs ONLY if the loop completed without hitting 'break'
    #(meaning the player never guessed correctly)
        else:
            print(f"\\nOut of attempts! The number was {secret}.")
    
    play_again = input("\\nPlay again? (yes/no): ")

    print("Thanks for playing!")