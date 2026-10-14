# Task 2: EDA on the classicmodels sample database (MySQL)
# Step 1: Descriptive statistics and univariate analysis
# Step 3: Multivariate analysis and correlation

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Folder to save the charts
if not os.path.exists("charts"):
    os.mkdir("charts")


# (Connect to MySQL and load the table)


password = input("Enter your MySQL root password: ")
engine = create_engine("mysql+pymysql://root:" + quote_plus(password) + "@localhost:3306/classicmodels")

customers = pd.read_sql("SELECT * FROM customers", engine)
orders = pd.read_sql("SELECT * FROM orders", engine)
orderdetails = pd.read_sql("SELECT * FROM orderdetails", engine)
products = pd.read_sql("SELECT * FROM products", engine)
payments = pd.read_sql("SELECT * FROM payments", engine)

print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order details:", orderdetails.shape)
print("Products:", products.shape)
print("Payments:", payments.shape)


# STEP 1: Descriptive statistics and univariate analysis


# Numerical fields
print("\n--- Order details: quantity and price ---")
print(orderdetails[["quantityOrdered", "priceEach"]].describe())

print("\n--- Products: stock, buy price and MSRP ---")
print(products[["quantityInStock", "buyPrice", "MSRP"]].describe())

print("\n--- Payments: amount ---")
print(payments["amount"].describe())

print("\n--- Customers: credit limit ---")
print(customers["creditLimit"].describe())

# Categorical fields
print("\n--- Order status ---")
print(orders["status"].value_counts())

print("\n--- Product line ---")
print(products["productLine"].value_counts())

print("\n--- Top 10 customer countries ---")
print(customers["country"].value_counts().head(10))

# Histogram 1: price of each item in an order
plt.figure(figsize=(8, 5))
plt.hist(orderdetails["priceEach"], bins=30)
plt.title("Distribution of price per item (priceEach)")
plt.xlabel("Price each")
plt.ylabel("Number of order lines")
plt.savefig("charts/01_priceEach_histogram.png")
plt.close()

# Histogram 2: quantity ordered
plt.figure(figsize=(8, 5))
plt.hist(orderdetails["quantityOrdered"], bins=30)
plt.title("Distribution of quantity ordered")
plt.xlabel("Quantity ordered")
plt.ylabel("Number of order lines")
plt.savefig("charts/02_quantityOrdered_histogram.png")
plt.close()

# Histogram 3: payment amount
plt.figure(figsize=(8, 5))
plt.hist(payments["amount"], bins=30)
plt.title("Distribution of payment amount")
plt.xlabel("Amount")
plt.ylabel("Number of payments")
plt.savefig("charts/03_payment_amount_histogram.png")
plt.close()

# Bar chart 1: order status
status_counts = orders["status"].value_counts()
plt.figure(figsize=(9, 5))
plt.bar(status_counts.index, status_counts.values)
plt.title("Orders by status")
plt.xlabel("Order status")
plt.ylabel("Number of orders")
plt.xticks(rotation=45)
plt.savefig("charts/04_order_status_bar.png", bbox_inches="tight")
plt.close()

# Bar chart 2: product line
line_counts = products["productLine"].value_counts()
plt.figure(figsize=(9, 5))
plt.bar(line_counts.index, line_counts.values)
plt.title("Number of products by product line")
plt.xlabel("Product line")
plt.ylabel("Number of products")
plt.xticks(rotation=45)
plt.savefig("charts/05_product_line_bar.png", bbox_inches="tight")
plt.close()

# Bar chart 3: top 10 countries by number of customers
country_counts = customers["country"].value_counts().head(10)
plt.figure(figsize=(9, 5))
plt.bar(country_counts.index, country_counts.values)
plt.title("Top 10 countries by number of customers")
plt.xlabel("Country")
plt.ylabel("Number of customers")
plt.xticks(rotation=45)
plt.savefig("charts/06_top_countries_bar.png", bbox_inches="tight")
plt.close()

print("\nStep 1 charts saved")


# STEP 3: Multivariate analysis and correlation


# Joining order details with products (one row for every item in an order)
data = pd.merge(orderdetails, products, on="productCode")

# Scatter plot 1: buy price vs MSRP
plt.figure(figsize=(8, 6))
plt.scatter(data["buyPrice"], data["MSRP"], alpha=0.3)
plt.title("Buy price vs MSRP")
plt.xlabel("Buy price")
plt.ylabel("MSRP")
plt.savefig("charts/07_scatter_buyPrice_MSRP.png")
plt.close()

# Scatter plot 2: price each vs quantity ordered
plt.figure(figsize=(8, 6))
plt.scatter(data["priceEach"], data["quantityOrdered"], alpha=0.3)
plt.title("Price each vs quantity ordered")
plt.xlabel("Price each")
plt.ylabel("Quantity ordered")
plt.savefig("charts/08_scatter_priceEach_quantity.png")
plt.close()

# Heatmap: correlation between numerical columns
number_columns = data[["quantityOrdered", "priceEach", "buyPrice", "MSRP", "quantityInStock"]]
correlation = number_columns.corr()
print("\nCorrelation:")
print(correlation)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm")
plt.title("Correlation heatmap")
plt.savefig("charts/09_heatmap.png", bbox_inches="tight")
plt.close()

# Pair plot
sns.pairplot(number_columns)
plt.savefig("charts/10_pairplot.png")
plt.close()

print("\nStep 3 charts saved")



