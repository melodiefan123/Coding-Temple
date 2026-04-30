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
# Which products have a rating of 4.5 or higher AND cost less than $100? (Show name, rating, price)
# What are the 3 most expensive products in the "Accessories" category? (Show name and price, sorted by price descending)
# Which products have "Monitor" in their name? (Show all columns)
# Which products are NOT in the "Accessories" category and are in stock? (Show name, category, price, sorted by category then price)