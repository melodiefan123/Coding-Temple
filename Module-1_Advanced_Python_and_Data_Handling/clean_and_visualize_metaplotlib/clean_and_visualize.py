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

# Analyze and visualize: Total sales by product (bar), daily trend (line), distribution (histogram)
# Save visualizations to a PNG file