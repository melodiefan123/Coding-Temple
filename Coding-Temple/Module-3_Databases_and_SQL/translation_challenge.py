import sqlite3
import pandas as pd
#SQLite database 
#columns: product, category, unit_price, quantity, quarter

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE sales_data(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               product TEXT NOT NULL, 
               category TEXT NOT NULL, 
               unit_price REAL NOT NULL, 
               quantity INTEGER NOT NULL, 
               quarter TEXT NOT NULL)""")

sales_data = [
    ("Widget A", "Electronics", 29.99, 150, "2025-Q1"),
    ("Widget B", "Electronics", 49.99, 89, "2025-Q1"),
    ("Gadget X", "Accessories", 15.99, 300, "2025-Q1"),
    ("Widget A", "Electronics", 29.99, 200, "2025-Q2"),
    ("Gadget Y", "Accessories", 22.99, 175, "2025-Q2"),
    ("Widget C", "Electronics", 79.99, 50, "2025-Q2"),
    ("Gadget X", "Accessories", 15.99, 280, "2025-Q2"),
    ("Widget B", "Electronics", 49.99, 120, "2025-Q3"),
]

cursor.executemany("INSERT INTO sales_data(product, category, unit_price, quantity, quarter) VALUES (?,?,?,?,?)", sales_data)
connection.commit()

#Pandas dataframe
df = pd.DataFrame(sales_data, columns=["product","category", "unit_price", "quantity", "quarter"])

# Answer each question using BOTH SQL and pandas:
# What is the total revenue (price × quantity) per product?
    #SQL
print("=== SQL: Total Revenue ===")
cursor.execute("SELECT product, sum(unit_price * quantity) FROM sales_data GROUP BY product ")
for row in cursor.fetchall(): 
    print(f"Product:{row[0]} Total Revenue: {row[1]}")
    #pandas
print("=== Panda: Total Revenue ===")
df["total_revenue"] = df["unit_price"] * df["quantity"]
revenue_per_product = df.groupby("product")['total_revenue'].sum()
print(revenue_per_product)

# Which quarter had the highest total quantity sold?
#SQL
print("=== SQL: Highest Quantity ===")
cursor.execute("SELECT sum(quantity), quarter FROM sales_data GROUP BY quarter ORDER BY sum(quantity) DESC LIMIT 1")
for row in cursor.fetchall(): 
    print(f"{row[1]}")
#panda
print("=== Panda: Highest Quantity ===")
total_quantity = df.groupby("quarter")["quantity"].sum().idxmax()
print(total_quantity)

# What is the average unit price per category?
#SQL
print("=== SQL: Average Unit Price ===")
cursor.execute("SELECT category, avg(unit_price) FROM sales_data GROUP BY category")
for row in cursor.fetchall(): 
    print(f"Category: {row[0]} Average Price: {row[1]}")
#panda
print("=== Panda: Average Unit Price ===")
average_price = df.groupby("category")["unit_price"].mean()
print(average_price)
# Which products had total quantity over 200 across all quarters?
#SQL
print("=== SQL: Over 200 Quantity ===")
cursor.execute("SELECT product, sum(quantity) FROM sales_data GROUP BY product HAVING sum(quantity) > 200")
for row in cursor.fetchall(): 
    print(f"Product: {row[0]} Quantity: {row[1]}")
#panda
print("=== Panda: Over 200 Quantity ===")
product_totals = df.groupby("product")["quantity"].sum()
print(product_totals[product_totals > 200])

# BONUS: Use pd.read_sql() to run one of your SQL queries and get the result as a DataFrame.
query = "SELECT product, sum(quantity) FROM sales_data GROUP BY product HAVING sum(quantity) > 200"
test = pd.read_sql(query, connection)
print(test.to_string(index=False))