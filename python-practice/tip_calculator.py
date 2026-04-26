#tip_calculator.py - Interactive tip calculator


# bill_text = input("\\nEnter the bill amount: $")
# bill = float(bill_text)
def main():
    print("=" * 35)
    print("        Tip Calculator")
    print("=" * 35)

    #Get the bill amount (input returns a string, so convert to float) 
    tip_percentages = [15, 18, 20, 25]
    while True:
        try:
            bill = float(input("\nEnter the bill amount: $"))
            break
        except ValueError:
            print("Please enter a valid number.")

    #calculate tip amounts for common percentages
    # tip_15 = bill * 0.15
    # tip_18 = bill * 0.18
    # tip_20 = bill * 0.20
    # tip_25 = bill * 0.25

    # total_15 = bill + tip_15
    # total_18 = bill + tip_18
    # total_20 = bill + tip_20
    # total_25 = bill + tip_25

    #Ask about splitting 
    while True: 
        try: 
            people_text = int(input("How many people are splitting the bill? "))
            if people_text <= 0:
                print("Please enter a number greater than 0.")
                continue
            break
        except ValueError: 
            print("Please enter a valid number. ")

    #Display results
    print(f"\nBill Amount: ${bill:.2f}")
    print(f"Number of people: {people_text}")
    print("-" * 35)
    print(f"{'Tip %':<10} {'Tip' :<10} {'Total':<10} {'Per Person':<10}")
    print("-" * 35)
    for percent in tip_percentages:
        tip = bill * (percent / 100)
        total = bill + tip
        print(f"{f'{percent}%':<10} ${tip:<9.2f} ${total:<9.2f} ${total/people_text:<9.2f}")
    # print(f"{'15%':<10} ${tip_15:<9.2f} ${total_15:<9.2f} ${total_15/people:<9.2f}")
    # print(f"{'18%':<10} ${tip_18:<9.2f} ${total_18:<9.2f} ${total_18/people:<9.2f}")
    # print(f"{'20%':<10} ${tip_20:<9.2f} ${total_20:<9.2f} ${total_20/people:<9.2f}")
    # print(f"{'25%':<10} ${tip_25:<9.2f} ${total_25:<9.2f} ${total_25/people:<9.2f}")
    print("=" * 35) 

main()