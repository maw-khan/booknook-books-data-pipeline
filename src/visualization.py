
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import webbrowser

from pywaffle import Waffle
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# 1. CONNECT TO BOOKNOOK DATABASE
# ============================================================

load_dotenv()

password = os.environ["DB_PASSWORD"]

DATABASE_URL = (
    f"postgresql+psycopg2://postgres:{password}"
    "@localhost:5432/booknook"
)

engine = create_engine(DATABASE_URL)

print("Connected to BookNook database.")


# ============================================================
# 2. LOAD THE DATAFRAME
# ============================================================
# We need the same joined DataFrame analysis.

query = """
SELECT
    o.order_id,
    o.order_date,
    o.status,
    p.product_name,
    p.category,
    oi.quantity,
    oi.unit_price
FROM orders AS o
JOIN orderitems AS oi
    ON o.order_id = oi.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
ORDER BY o.order_id, oi.order_item_id;
"""

df = pd.read_sql(query, engine)

df["order_date"] = pd.to_datetime(df["order_date"])

df["line_total"] = df["quantity"] * df["unit_price"]

print("\nBookNook Data:")
print(df)


# ============================================================
# 3. SEABORN SETTINGS
# ============================================================

sns.set_theme(style="whitegrid")


# ============================================================
# 4. SEABORN BAR CHART
# ============================================================
# Recreate the category revenue bar chart
# using Seaborn.

category_revenue = (
    df.groupby("category")["line_total"]
    .sum()
    .sort_values(ascending=False)
)

order = (
    df.groupby("category")["line_total"]
    .sum()
    .sort_values(ascending=False)
).index

plt.figure(figsize=(10, 6))

sns.barplot(data=df, x="category", y="line_total",estimator="sum", errorbar=None,order=order)

plt.title("BookNook - Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ============================================================
# 5. SEABORN HUE SCATTERPLOT
# ============================================================
# Categories are shown using different hues.

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="unit_price",
    y="quantity",
    hue="category",
    s=60,
    alpha=0.6
)

plt.title("BookNook - Quantity vs Price, Colored by Category")
plt.xlabel("Unit Price")
plt.ylabel("Quantity")

plt.tight_layout()
plt.show()


# ============================================================
# 6. WAFFLE CHART
# ============================================================
# Shows each category's share of total revenue.

shares = (
    category_revenue
    / category_revenue.sum()
    * 100
).round(1)

print("\nRevenue Share by Category:")
print(shares)


fig = plt.figure(
    FigureClass=Waffle,
    rows=5,
    columns=20,
    values=shares.to_dict(),
    title={
        "label": "BookNook - Revenue Share by Category",
        "loc": "center"
    },
    labels=[
        f"{category} ({percentage}%)"
        for category, percentage in shares.items()
    ],
    legend={
        "loc": "upper left",
        "bbox_to_anchor": (1, 1)
    },
    figsize=(12, 7)
)

plt.tight_layout()
plt.show()


# ============================================================
# 7. GET CUSTOMER COUNT BY CITY
# ============================================================

city_query = """
SELECT
    city,
    COUNT(*) AS n
FROM customers
GROUP BY city
ORDER BY n DESC;
"""

city_counts = pd.read_sql(city_query, engine)

print("\nCustomer Count by City:")
print(city_counts)


# ============================================================
# 8. CITY COORDINATES
# ============================================================

city_coords = {
    "Islamabad": [33.6989, 73.0369],
    "Rawalpindi": [33.6007, 73.0679],
    "Lahore": [31.5497, 74.3436],
    "Karachi": [24.8600, 67.0100],
    "Peshawar": [34.0144, 71.5675],
    "Faisalabad": [31.4180, 73.0790],
    "Multan": [30.1978, 71.4711],
    "Gujranwala": [32.1500, 74.1833],
    "Sialkot": [32.5000, 74.5333],
    "Quetta": [30.1958, 67.0172]
}

# ============================================================
# 9. CHECK FOR MISSING CITY COORDINATES
# ============================================================

missing_cities = [
    city
    for city in city_counts["city"]
    if city not in city_coords
]

if missing_cities:
    print("\nWARNING - Coordinates missing for:")
    print(missing_cities)
else:
    print("\nAll customer cities have coordinates.")


# ============================================================
# 10. CREATE FOLIUM MAP
# ============================================================

m = folium.Map(
    location=[33.6844, 73.0479],
    zoom_start=5
)


# ============================================================
# 11. ADD CIRCLE MARKERS
# ============================================================

for _, row in city_counts.iterrows():

    city = row["city"]
    count = row["n"]

    if city in city_coords:

        folium.CircleMarker(
            location=city_coords[city],
            radius=5 + count * 2,
            popup=f"{city}: {count} customers",
            tooltip=city,
            color="#1F4E79", fill=True, fill_opacity=0.7
        ).add_to(m)


# ============================================================
# 12. SAVE MAP
# ============================================================

map_file = "booknook_customer_map.html"

m.save(map_file)

print(f"\nMap saved as: {map_file}")


# ============================================================
# 13. OPEN MAP IN BROWSER
# ============================================================

webbrowser.open(map_file)


# ============================================================
# 14. TASK COMPLETE
# ============================================================

print("1. Seaborn category revenue bar chart")
print("2. Seaborn hue scatterplot")
print("3. Waffle revenue-share chart")
print("4. Folium customer-city map")
print("5. Customer map saved as booknook_customer_map.html")