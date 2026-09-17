# ============================================================
# BookNook Books
# Exploration & Core Matplotlib Charts
# ============================================================

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# 2. DATABASE CONNECTION
# ============================================================

load_dotenv()

password = os.environ["DB_PASSWORD"]

DATABASE_URL = (
    f"postgresql+psycopg2://postgres:{password}"
    f"@localhost:5432/booknook"
)

engine = create_engine(DATABASE_URL)

print("Connected to BookNook database.")


# ============================================================
# 3. PULL DATA FROM DATABASE
# ============================================================

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

print("\n============================================================")
print("DATAFRAME")
print("============================================================")

print(df)


# ============================================================
# 4. BASIC DATAFRAME EXPLORATION
# ============================================================

df["order_date"] = pd.to_datetime(df["order_date"])

df["line_total"] = df["quantity"] * df["unit_price"]

print("\n============================================================")
print("FIRST 5 ROWS")
print("============================================================")

print(df.head())


print("\n============================================================")
print("DATAFRAME INFO")
print("============================================================")

print(df.info())


print("\n============================================================")
print("DESCRIPTIVE STATISTICS")
print("============================================================")

print(df.describe())


print("\n============================================================")
print("UNIQUE CATEGORIES")
print("============================================================")

print(df["category"].unique())


# ============================================================
# 5. NUMPY WARM-UP
# ============================================================

values = df["line_total"].to_numpy()

mean_value = np.mean(values)
std_value = np.std(values)

above_average = values[values > mean_value]
above_average_count = len(above_average)

print("\n============================================================")
print("NUMPY STATISTICS")
print("============================================================")

print(f"Mean order-line value: {mean_value:.2f}")
print(f"Standard deviation: {std_value:.2f}")
print(f"Order lines above average: {above_average_count}")


# ============================================================
# 6. DAILY REVENUE
# ============================================================

daily_revenue = (
    df.groupby("order_date")["line_total"]
    .sum()
)

print("\n============================================================")
print("DAILY REVENUE")
print("============================================================")

print(daily_revenue)


# ============================================================
# CHART 1 - DAILY REVENUE TREND
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    daily_revenue.index,
    daily_revenue.values,
    marker="o",
    color="RED"
)

plt.title("BookNook - Daily Revenue Trend")
plt.xlabel("Order Date")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 7. REVENUE BY CATEGORY
# ============================================================

category_revenue = (
    df.groupby("category")["line_total"]
    .sum()
    .sort_values(ascending=False)
)

print("\n============================================================")
print("REVENUE BY CATEGORY")
print("============================================================")

print(category_revenue)


# ============================================================
# CHART 2 - REVENUE BY CATEGORY
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    category_revenue.index,
    category_revenue.values, 
    color="#ED7D31"
)

plt.title("BookNook - Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 8. CUMULATIVE REVENUE
# ============================================================

cumulative_revenue = daily_revenue.cumsum()

print("\n============================================================")
print("CUMULATIVE REVENUE")
print("============================================================")

print(cumulative_revenue)


# ============================================================
# CHART 3 - CUMULATIVE REVENUE AREA CHART
# ============================================================

plt.figure(figsize=(10, 6))

plt.fill_between(
    cumulative_revenue.index,
    cumulative_revenue.values, 
    color="GREEN",
    alpha=0.4
)

plt.plot(
    cumulative_revenue.index,
    cumulative_revenue.values,
    color="GREEN",
    linewidth=2
)

plt.title("BookNook - Cumulative Revenue")
plt.xlabel("Order Date")
plt.ylabel("Cumulative Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ============================================================
# 9. HISTOGRAM DATA
# ============================================================

print("\n============================================================")
print("ORDER-LINE VALUES")
print("============================================================")

print(df["line_total"])


# ============================================================
# CHART 4 - HISTOGRAM
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["line_total"],
    bins=20, color="#70AD47",
    edgecolor="black"
)



plt.title("BookNook - Distribution of Order-Line Values")
plt.xlabel("Order-Line Value")
plt.ylabel("Frequency")

plt.tight_layout()

plt.show()


# ============================================================
# CHART 5 - SCATTER PLOT
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    df["unit_price"],
    df["quantity"], alpha=0.6,
    color="#548235", 
    edgecolors="black"
)

plt.title("BookNook - Unit Price vs Quantity")
plt.xlabel("Unit Price")
plt.ylabel("Quantity")

plt.tight_layout()

plt.show()

# ============================================================
# 6. FOUR CORE CHARTS IN ONE FIGURE
# ============================================================

# Daily revenue
daily_revenue = (
    df.groupby("order_date")["line_total"]
    .sum()
)

# Revenue by category
category_revenue = (
    df.groupby("category")["line_total"]
    .sum()
    .sort_values(ascending=False)
)


# Create 2 x 2 subplot figure
fig, axes = plt.subplots(2, 2, figsize=(10, 6))


# ============================================================
# PLOT 1 - DAILY REVENUE TREND
# ============================================================

ax1 = axes[0, 0]

ax1.plot(
    cumulative_revenue.index,
    cumulative_revenue.values,
    color="GREEN",
    linewidth=2
)

ax1.set_title("BookNook - Daily Revenue Trend")
ax1.set_xlabel("Order Date")
ax1.set_ylabel("Revenue")

ax1.tick_params(axis="x", rotation=45)


# ============================================================
# PLOT 2 - REVENUE BY CATEGORY
# ============================================================

ax2 = axes[0, 1]

ax2.bar(
    category_revenue.index,
    category_revenue.values, 
    color="#ED7D31"
)

ax2.set_title("BookNook - Revenue by Category")
ax2.set_xlabel("Category")
ax2.set_ylabel("Revenue")

ax2.tick_params(axis="x", rotation=45)


# ============================================================
# PLOT 3 - DISTRIBUTION OF ORDER-LINE VALUES
# ============================================================

ax3 = axes[1, 0]

ax3.hist(
    df["line_total"],
    bins=20, color="#70AD47",
    edgecolor="black"
)

ax3.set_title("BookNook - Distribution of Order-Line Values")
ax3.set_xlabel("Order-Line Value")
ax3.set_ylabel("Frequency")


# ============================================================
# PLOT 4 - UNIT PRICE VS QUANTITY
# ============================================================

ax4 = axes[1, 1]

ax4.scatter(
    df["unit_price"],
    df["quantity"], alpha=0.6,
    color="#548235", 
    edgecolors="black"
)

ax4.set_title("BookNook - Unit Price vs Quantity")
ax4.set_xlabel("Unit Price")
ax4.set_ylabel("Quantity")


# ============================================================
# FINAL LAYOUT
# ============================================================

fig.suptitle(
    "BookNook Books - Core Analysis",
    fontsize=16
)

plt.tight_layout()

plt.show()

# ============================================================
# 10. FINAL SUMMARY
# ============================================================

print("\n============================================================")
print("SUMMARY")
print("============================================================")

print(f"Total order lines: {len(df)}")
print(f"Total revenue: {df['line_total'].sum():.2f}")
print(f"Average order-line value: {np.mean(values):.2f}")
print(f"Standard deviation: {np.std(values):.2f}")
print(f"Order lines above average: {above_average_count}")



