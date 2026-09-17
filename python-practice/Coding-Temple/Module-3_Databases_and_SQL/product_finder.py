import sqlite3

connection = sqlite3.connect(":memory:")  # In-memory DB — disappears when script ends
cursor = connection.cursor()

# Create a products table
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        rating REAL,
        in_stock INTEGER DEFAULT 1
    )
""")

# Insert sample data — a small electronics store
products = [
    ("Wireless Mouse", "Accessories", 29.99, 4.5, 1),
    ("Mechanical Keyboard", "Accessories", 89.99, 4.8, 1),
    ("USB-C Hub", "Accessories", 34.99, 4.2, 0),
    ("27-inch Monitor", "Displays", 299.99, 4.6, 1),
    ("24-inch Monitor", "Displays", 179.99, 4.3, 1),
    ("Webcam HD", "Accessories", 49.99, 3.9, 1),
    ("Noise-Canceling Headphones", "Audio", 199.99, 4.7, 1),
    ("Bluetooth Speaker", "Audio", 59.99, 4.1, 0),
    ("Laptop Stand", "Accessories", 39.99, 4.4, 1),
    ("External SSD 1TB", "Storage", 89.99, 4.6, 1),
    ("External SSD 2TB", "Storage", 149.99, 4.5, 1),
    ("Flash Drive 64GB", "Storage", 12.99, 4.0, 1),
]

cursor.executemany("""
    INSERT INTO products (name, category, price, rating, in_stock) 
    VALUES (?, ?, ?, ?, ?)
""", products)
connection.commit()

# Which products are out of stock? (Show name and category)
print("\nOut Of Stock")
cursor.execute("SELECT name, category FROM products WHERE in_stock = 0")
for row in cursor.fetchall():
    print(f" {row[0]}: {row[1]}")
# Which products have a rating of 4.5 or higher AND cost less than $100? (Show name, rating, price)
print("\n Rating Higher Than 4.5")

cursor.execute("SELECT name, rating, price FROM products WHERE rating >= 4.5 AND price < 100")
for row in cursor.fetchall():
    print(f" Name: {row[0]} Rating: {row[1]} Price:{row[2]}")

# What are the 3 most expensive products in the "Accessories" category? (Show name and price, sorted by price descending)
print("\n Most Expensive Products")

cursor.execute("SELECT name, price FROM products WHERE category = 'Accessories' ORDER BY price DESC LIMIT 3")
for row in cursor.fetchall():
    print(f" Name:{row[0]} Price: {row[1]}")

# Which products have "Monitor" in their name? (Show all columns)
print("\n Monitor Products")

cursor.execute("SELECT * FROM products WHERE name  LIKE '%Monitor%'")

print(cursor.fetchall())

# Which products are NOT in the "Accessories" category and are in stock? (Show name, category, price, sorted by category then price)
print("\n In Stock and Not In Accessories")

cursor.execute("SELECT name, category, price FROM products WHERE category != 'Accessories' AND in_stock = 1 ORDER BY category, price")

for row in cursor.fetchall(): 
    print(f"Name: {row[0]} Category: {row[1]} Price: {row[2]}")