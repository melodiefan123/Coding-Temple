products = [
    {"name": "Laptop", "price": 999.99, "category": "electronics", "in_stock": True},
    {"name": "Python Book", "price": 39.99, "category": "books", "in_stock": True},
    {"name": "Headphones", "price": 149.99, "category": "electronics", "in_stock": False},
    {"name": "Desk Lamp", "price": 29.99, "category": "home", "in_stock": True},
    {"name": "AI Textbook", "price": 89.99, "category": "books", "in_stock": True},
    {"name": "Monitor", "price": 349.99, "category": "electronics", "in_stock": True},
    {"name": "Notebook", "price": 4.99, "category": "office", "in_stock": True},
    {"name": "Keyboard", "price": 79.99, "category": "electronics", "in_stock": False},
]

#Using list comprehensions, map, filter, and/or lambda:

# Get all in-stock products (filter)
in_stock = [p for p in products if p["in_stock"]]

# Add a "discounted_price" field that’s 10% off the original (map - create new dicts, don’t mutate)
discounted_prices = [{**p, "discounted_price": p['price'] - (p['price'] *0.1)} for p in products]

# Get only electronics under $200 (filter with two conditions)
electronics_under_200 = [p for p in products if p['category'] == 'electronics' and p['price'] < 200]

# Sort all products by price, lowest first (use sorted with a key lambda)
sorted_by_price = sorted(products, key=lambda p: p['price'])

# Calculate the total value of all in-stock products (reduce or sum with comprehension)
total_value_in_stock = sum(p['price'] for p in products if p['in_stock'])


# Group products by category, return a dictionary like {"electronics": [...], "books": [...], ...} Do not use for loops with append. Use comprehensions or functional tools only. Do not modify the original products list.
category_groups = {category: [p for p in products if p['category'] == category] for category in set(p['category'] for p in products)}


print("\n" + "=" * 60)
print("Task 6 — Products grouped by category (dict comprehension)")
print("=" * 60)
for cat, items in category_groups.items():
    names = ", ".join(p["name"] for p in items)
    print(f"  {cat:<12}: {names}")

print("\nOriginal products list unchanged:", len(products), "items")