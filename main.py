#e-commerce sales data analysis with Python(From Seller's Perspective)

#order_ID, Date, castomer_ID , Product, Catagory, Price, Quantity
#Payment Mode, City & State

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#importing data set
df = pd.read_csv('Ecommerce_Sales.csv')
print (df.head())

# Data overview
#Dataset shape and info 
print (df.head)
#Attribute names and datatype for your data type also finds missing values 
print (df.info)

#Statistical summary (statistical summery: mean max avg %)
print (df.describe())

#check for missingf values : Find null value attributes 
print (df.isnull().sum())

#Data cleaning 
#Convert 'date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

#Remove any rows with missing values 
df.dropna(inplace = True)

#Create a new column "Total amount" Price and quality acc
df['Total_Amount'] =  df['Price'] * df['Quantity']

#Explore data find top 5 cities with highest sales 
top_cities = df.groupby('City')['Total_Amount'].sum().sort_values(ascending=False).head(5)

#Find the monthly sales
monthly_sales = df.groupby(df['Date'].dt.month)['Total_Amount'].sum()
print("Monthly Sales")
print(monthly_sales)


#Analyze sales scale evolve with time 
Sales_over_time = df.groupby('Date')['Total_Amount'].sum()
print("Sales Over Time")
print(Sales_over_time)


monthly_sales.plot(kind= 'line', marker ='o', title= 'Monthly Sales Trend', figsize=(14, 7))
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.show()
