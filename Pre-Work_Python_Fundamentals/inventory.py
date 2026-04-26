inventorys = {
    "laptop": {"price": 999.99, "quantity": 15},
    "mouse": {"price": 29.99, "quantity": 50},
    "monitor": {"price": 199.99, "quantity": 50},
    "keyboard": {"price": 69.99,"quantity":20}
}
low_stock = set()

def display_inventory():
    print("\n" + "=" * 50)
    print("                 Inventory List")
    print("=" * 50)

    if not inventorys: 
        print("No inventory yet")
        return 
     
    print(f"  {'Item':<12}{'Price':<7} {'Quantity':>12}{'Total':>10}")
    grand_total = 0 
    for key, info in inventorys.items():
        grand_total += info['price']*info['quantity']
        print(f"\n {key:<12} ${info['price']:>7.2f} {info['quantity']:>8}       ${info['price']*info['quantity']:<10.2f} ")
        
    print('-' * 50)
    print(f"{'Total':<21}               ${grand_total:<31.2f}")
    print("=" * 50)

    search = input("\nSearch for an item: ").lower()
    inventory = inventorys.get(search)

    if inventory: 
        print(f"\nFound: {search}")
        print(f"Price: ${inventory['price']}")
        print(f"Quantity: {inventory['quantity']}")
    else:
        print(f"Cannot find {search}. Please search for another item.")

    print(f"---Inventory Update---")
    item_purchase = input("Would you like to (1) purchase / (2) restock?").lower()
    confirmation = input("Enter item name: ").lower()
    item = inventorys.get(confirmation)
    if item is None: 
        print(f"Cannot find item. Please look for another item to purchase.")
    else:
        # print(f"Great. {item_purchase} is {item['price']}.")
        if item_purchase == '1':
            item['quantity'] -= 1
            print(f"Purchased item {confirmation}. Updated quantity: {item['quantity']}")
        elif item_purchase == '2':
            amount = int(input("How many units to restock?"))
            item['quantity'] += amount 
            print(f"Restocked {confirmation}. Updated quantity: {item['quantity']}")
        else:
            print("Invalid choice. Please enter 1 or 2. ")
    low_stock.clear()
    for key, info in inventorys.items():
        if info['quantity'] < 10: 
            low_stock.add(key)
display_inventory()

if low_stock: 
    print(f"\n Low Stock Alert: {', '.join(low_stock)}")
else:
    print("\n All items are sufficiently stocked.")




