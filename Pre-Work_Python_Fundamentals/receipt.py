item1_name = "Notebook"

item1_price = float("4.99")
item1_qty = int("2")
item1_total = item1_price * item1_qty

item2_name = "Pen Pack"
item2_price = float("7.50")
item2_qty = int("1")
item2_total = item2_price * item2_qty

item3_name = "Backpack"
item3_price = float("34.99")
item3_qty = int("1")
item3_total = item3_price * item3_qty

tax_rate = float("0.075")   # 7.5% sales tax

subtotal = item1_total + item2_total + item3_total
tax_amount = subtotal * tax_rate
total = subtotal + tax_amount

print("=" * 45)
print("                 Store Receipt")
print("=" * 45)

print(f"{item1_name:<16} ${item1_price:>2.2f} x {item1_qty:<10}${item1_total:<15.2f}")
print(f"{item2_name:<16} ${item2_price:>2.2f} x {item2_qty:<10}${item2_total:<15.2f}")
print(f"{item3_name:<16} ${item3_price:>2.2f} x {item3_qty:<10}${item3_total:<9.2f}")

print("-" * 45)

print(f"{'Subtotal':<35}${subtotal:>.2f}")
print(f"{'Tax (7.5%)':<35}${tax_amount:>.2f}")

print("=" * 45)
print(f"{'Total':<35}${total:>.2f}")
print("=" * 45)
