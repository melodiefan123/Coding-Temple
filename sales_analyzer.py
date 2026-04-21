import csv

with open('sales_data.csv', 'r') as file: 
    reader = csv.DictReader()
    