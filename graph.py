import pandas as pd
import matplotlib.pyplot as plt
# Manually create a DataFrame with the sales data provided in the message
sales_data = {
    "ID": [1, 2, 3, 4, 5, 6],
    "Category": [
        "APPAREL", "CLIMBING", "TRAVEL",
        "TRAVEL", "CLIMBING", "FISHING GEAR"
    ],
    "Subcategory": [
        "PANTS & SHORTS", "ROPES & SLINGS", "CARRY-ONS",
        "OTHER", "AVALANCHE SAFETY", "FISHING LINE"
    ],
    "Sales Units": [711.0, 972.0, 2576.0, 116.0, 2652.0, 444.0],
    "Revenue": [106.65, 106.92, 437.92, 16.24, 265.2, 57.72],
    "Order Count": [9, 12, 14, 4, 13, 12],
    "Year": [2023, 2024, 2024, 2024, 2022, 2022],
    "Month": [2, 7, 5, 10, 1, 1],
    "Profit": [14.22, 29.16, 283.36, 1.16, 106.08, 62.16],
    "Region": [
        "LATIN AMERICA", "CHINA", "LATIN AMERICA",
        "EUROPE", "AFRICA", "NORTH AMERICA"
    ],
    "Year-Month": ["2023-02", "2024-07", "2024-05", "2024-10", "2022-01", "2022-01"]
}

# Create a DataFrame from the sales_data dictionary
df_sales = pd.DataFrame(sales_data)

# Filter the data for climbing gear sales
climbing_gear_sales = df_sales[df_sales["Category"] == "CLIMBING"]

# Display the filtered climbing gear sales data
climbing_gear_sales

# Create a bar chart to visualize climbing gear sales
plt.figure(figsize=(10, 6))
plt.bar(climbing_gear_sales['Subcategory'], climbing_gear_sales['Sales Units'], color=['skyblue', 'lightgreen'])

# Adding labels and title
plt.xlabel('Subcategory', fontsize=12)
plt.ylabel('Sales Units', fontsize=12)
plt.title('Climbing Gear Sales Units by Subcategory', fontsize=14)
plt.xticks(rotation=45)

# Save the plot as a .png file
plt.tight_layout()
plot_path = 'climbing_gear_sales.png'
plt.savefig(plot_path)

plot_path