import pandas as pd
import matplotlib.pyplot as plt

messy = pd.DataFrame({
    "product": ["Widget A", "Widget B", "widget a", "Widget C", "Widget B",
                "Widget A", " Widget C", "Widget D", None, "Widget A"],
    "sales": ["150", "200", "175", "300", "200",
              "180", "250", "abc", "100", "-50"],
    "date": ["2025-01-01", "2025-01-01", "2025-01-02", "2025-01-02", "2025-01-03",
             "2025-01-03", "2025-01-04", "2025-01-04", "2025-01-05", "2025-01-05"],
    "region": ["North", "South", "north", "East", "South",
               "West", "east", "North", "South", "West"],
})


# Clean it: Standardize names/regions, convert types, handle missing/invalid values, remove duplicates
messy = messy.dropna(subset=['product'])
messy['product'] = messy['product'].str.strip().str.title()
messy['region'] = messy['region'].str.strip().str.title()
messy['sales'] = pd.to_numeric(messy['sales'], errors = "coerce")
messy = messy.dropna(subset=["sales"])
messy = messy[messy["sales"] >0]
messy['date'] = pd.to_datetime(messy['date'], errors="coerce")

# Analyze and visualize: Total sales by product (bar), daily trend (line), distribution (histogram)
# Save visualizations to a PNG file
sales_by_product = messy.groupby("product")["sales"].sum()
plt.bar(sales_by_product.index, sales_by_product.values)
plt.title("Total Sales By Product") 
plt.xlabel("Products")
plt.ylabel("Sales")
plt.savefig("Sales_By_Product_Bar.png", dpi=150)
plt.show()

#Line Chart
daily_trend = messy.groupby("date")["sales"].sum()
plt.plot(daily_trend.index, daily_trend.values)
plt.title("Daily Trend")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.savefig("Daily_Trend_Line.png", dpi=150)
plt.show()


#Histogram
plt.hist(messy["sales"])
plt.title("Distribution")
plt.xlabel("Sales")
plt.ylabel("Frequency")
plt.savefig("Distribution_Histogram.png", dpi=150)
plt.show()





