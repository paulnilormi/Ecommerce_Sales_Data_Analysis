#Customer& Revenue From Sales Data


#Attribute that going to be used:
#Order ID, Date, Product, Price, Payment, City, State

#Import the necessary libraries
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

#Importing the dataset
df = pd.read_csv('Ecommerce_Sales.csv')
print(df.head())

#Data Overview

#Dataset shape and info. (for number and col in the dataset)
print(df.head())
#Attributes name (and datatype of your data type) also finds missing values
print(df.info())


#Statistics Summary (Staticstical summary: mean max avg %)
print(df.describe())

#check for missing values : Finds null value attributes
print(df.isnull().sum())

#Convert the date
df['Date'] = pd.to_datetime(df['Date'])

#df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Use this if you are using Google Colab to avoid errors
#df = df.dropna(subset=['Date'])  # Use this if you are using Google Colab

#Create Total Amount
df['Total Amount'] = df['Price'] * df['Quantity']

#Group by Customer_ID and calculate the total sales of each customer
customer_sales = df.groupby('Customer_ID')['Total Amount'].sum().reset_index()
customer_sales = customer_sales.sort_values(by='Total Amount', ascending=False)
print("Customer sales data:")
print(customer_sales.head())

# Monthly Expenditure by each customer by Customer_ID
monthly_expenditure = df.groupby(['Customer_ID', df['Date'].dt.to_period('M')])['Total Amount'].sum().reset_index()
monthly_expenditure['Date'] = monthly_expenditure['Date'].dt.to_timestamp()
print("Monthly expenditure by each customer:")
print(monthly_expenditure)

# Highest Expenditure of each customer monthly
highest_monthly_expenditure = monthly_expenditure.loc[monthly_expenditure.groupby('Customer_ID')['Total Amount'].idxmax()]
print("Highest monthly expenditure of each customer:")
print(highest_monthly_expenditure)

#Time series Analysis (Monthly Revenue Trend)
# Monthly Revenue Trend
monthly_revenue = df.groupby(df['Date'].dt.to_period('M'))['Total Amount'].sum().reset_index()
monthly_revenue['Date'] = monthly_revenue['Date'].dt.to_timestamp()

plt.figure(figsize=(14, 7))
sns.lineplot(data=monthly_revenue, x='Date', y='Total Amount', marker='o')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.grid(True)
plt.tight_layout()
plt.show()


#State_wise Performance
# Total revenue by state
state_performance = df.groupby('State')['Total Amount'].sum().sort_values(ascending=False).reset_index()

plt.figure(figsize=(14, 7))
sns.barplot(data=state_performance, x='Total Amount', y='State', palette='pastel')
plt.title('State-wise Revenue Performance')
plt.xlabel('Revenue')
plt.ylabel('State')
plt.tight_layout()
plt.show()

#Most Profitable Products
# Total revenue per product
product_revenue = df.groupby('Product')['Total Amount'].sum().sort_values(ascending=False).reset_index()

plt.figure(figsize=(14, 7))
sns.barplot(data=product_revenue.head(10), x='Total Amount', y='Product', palette='viridis')
plt.title('Top 10 Most Profitable Products')
plt.xlabel('Revenue')
plt.ylabel('Product')
plt.tight_layout()
plt.show()

#Customer Segmentation - RFM Analysis
# RFM (Recency, Frequency, Monetary) Analysis
print(df.columns)

snapshot_date = df['Date'].max() + pd.Timedelta(days=1)
rfm = df.groupby('Customer_ID').agg({
    'Date': lambda x: (snapshot_date - x.max()).days,
    'Order_ID': 'nunique',   # <-- Fix the column name here
    'Total Amount': 'sum'
}).reset_index()


rfm.columns = ['Customer_ID', 'Recency', 'Frequency', 'Monetary']


print("RFM Segmentation Sample:")
print(rfm.head())

#High Value Customer Identification
# High Value Customers - Top 10 by Monetary
high_value_customers = rfm.sort_values(by='Monetary', ascending=False).head(10)

plt.figure(figsize=(14, 10))
sns.barplot(data=high_value_customers, x='Monetary', y='Customer_ID', palette='summer')
plt.title('Top 10 High Value Customers by Total Spend')
plt.xlabel('Total Spend (Monetary)')
plt.ylabel('Customer ID')
plt.tight_layout()
plt.show()

#Payment Method Analysis
# Payment Method Distribution
payment_method = df['Payment_Mode'].value_counts().reset_index()
payment_method.columns = ['Payment Method', 'Count']

plt.figure(figsize=(12, 10))
sns.barplot(data=payment_method, x='Count', y='Payment Method', palette='twilight')
plt.title('Distribution of Payment Methods')
plt.xlabel('Number of Orders')
plt.ylabel('Payment Method')
plt.tight_layout()
plt.show()

#Day-Wise and Hour-wise Sales Heatmap
# Extract Day and Hour
df['Day'] = df['Date'].dt.day_name()
df['Hour'] = df['Date'].dt.hour

# Create pivot table for heatmap
heatmap_data = df.pivot_table(index='Day', columns='Hour', values='Total Amount', aggfunc='sum')

# Sort days in proper order
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data = heatmap_data.reindex(days_order)

plt.figure(figsize=(15, 6))
sns.heatmap(heatmap_data, cmap='YlOrRd', linewidths=0.5, linecolor='gray')
plt.title('Sales Heatmap by Day and Hour')
plt.xlabel('Hour of the Day')
plt.ylabel('Day of the Week')
plt.tight_layout()
plt.show()


