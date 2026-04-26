# robust_calc.py — Handles bad input gracefully

print("=" * 35)
print("        Tip Calculator")
print("=" * 35)

#Get bill amount with error handling

try:
    bill = float(input("\nEnter the bill amount: $"))
    if bill < 0: 
          print("Error: Bill amount cannot be negative.")
          exit()
    if bill == 0: 
          print("Nothing to tip on!")
          exit()
except ValueError:
      print("\\nError: Please enter a number (e.g., 45.99)")
      exit()  # Stop the program cleanly

#Get tip percentage with error handling
try: 
     tip_rate = float(input("Enter tip percentage (e.g., 15 for 15%): "))
     if tip_rate < 0: 
           print("Error: Tip percentage cannot be negative.")
           exit()
     if tip_rate > 100: 
           print(f"Wow, {tip_rate:.0f}% is very generous!")
except ValueError:
        print("\\nError: Please enter a number for the tip percentage.")
        exit()

#Calculcate (safe because we know both are numbers now)

tip = bill * (tip_rate / 100)
total = bill + tip

#Display
print(f"\nBill Amount: ${bill:.2f}")
print(f"Tip: ({tip_rate:.0f}%): ${tip:.2f}")
print(f"Total: ${total:.2f}")
     