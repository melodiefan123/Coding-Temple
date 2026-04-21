import csv

sales = []
with open('sales_data.csv', 'r') as file: 
    reader = csv.DictReader(file)
    for row in reader: 
        row['quantity'] = int(row['quantity'])
        row['price'] = float(row['price'])
        sales.append(row)
    
    total_revenue = 0
    product_revenue = {}
    product_quantity = {}
    day_revenue = {}
    for row in sales: 
        total_revenue += row['quantity']*row['price']
        if row['product'] not in product_revenue: 
             product_revenue[row['product']] = 0 
        product_revenue[row['product']] += row['quantity']*row['price']
        if row['product'] not in product_quantity: 
            product_quantity[row['product']] = 0
        product_quantity[row['product']] += row['quantity']
        if row['date'] not in day_revenue: 
            day_revenue[row['date']] = 0 
        day_revenue[row['date']] += row['quantity']*row['price']
    
    current_date = list(day_revenue.keys())[0]
    current_price = list(day_revenue.values())[0]
    for date, price in day_revenue.items():
        if current_price < price: 
            current_price = price
            current_date = date


# Writes formatted summary

with open('sales_report.txt', 'w') as file: 
    file.write("SALES SUMMARY\n")
    file.write("=" * 40 + "\n\n")
    file.write(f"Total Revenue: ${total_revenue}\n")
    for product, revenue in product_revenue.items(): 
        file.write(f"Product Revenue: ${revenue}\n")
        file.write(f"Quantity Sold: {product_quantity[product]}\n")
         
    file.write(f"Highest total Revenue: {current_date}   {current_price}\n")

print(f"Report written to sales_report.txt ")


#Product Summary csv

with open('product_summary.csv', 'w', newline="") as file:
    writer = csv.DictWriter(file, fieldnames = ["product", "total_quantity", "total_revenue"])
    writer.writeheader()

    for product, revenue in product_revenue.items():
        writer.writerow({"product":product, "total_quantity": product_quantity[product], "total_revenue": revenue}) 
print("Data written to product_summary.csv")






