#All required imports
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

#Set all the pio templates to be white in color for consistency.
pio.templates.default = "plotly_white"

#Load and peek at the data.
data = pd.read_csv("../dataset/supply_chain_data.csv")
print(data.head())

#Descriptive statistics
print(data.describe())

#EDA for supply chain
fig = px.scatter(data, x = "Price", y = "Revenue generated", color = 'Product type', hover_data = ['Number of products sold'], trendline = "ols")
fig.show()

#COMMENT: It is evident from the plot that skincare products generate more revenue. Higher the prices of the skincare products, higher the revenue generated.

#Sales data by product type

sales_data = data.groupby('Product type')['Number of products sold'].sum().reset_index()

pie_chart = px.pie(sales_data, values = 'Number of products sold', names = 'Product type', title = 'Sales by Product Type', hover_data = ['Number of products sold'], hole = 0.5, color_discrete_sequence=px.colors.qualitative.Pastel)

pie_chart.update_traces(textposition = 'inside', textinfo = 'percent+label')
pie_chart.show()

#COMMENT: This pie chart shows that 45% of the business comes from skincare, 29.5% from haircare, and 25.5% comes from cosmetics.

#Total Revenue generated from shipping carriers

total_revenue = data.groupby('Shipping carriers')['Revenue generated'].sum().reset_index()

bar_chart = go.Figure()

bar_chart.add_trace(go.Bar(x = total_revenue['Shipping carriers'], y = total_revenue['Revenue generated']))

bar_chart.update_layout(title = "Total Revenue by Shipping Carrier",
                        xaxis_title = "Shipping Carrier",
                        yaxis_title = "Revenue Generated")

bar_chart.show()

#COMMENT: Carrier B generated the most revenue out the 3 carriers.

#Average Lead Time and Average Manufacturing Costs of all the products in the company

avg_lead_time = data.groupby('Product type')['Lead time'].mean().reset_index()

avg_manufacturing_cost = data.groupby('Product type')['Manufacturing costs'].mean().reset_index()

result = pd.merge(avg_lead_time, avg_manufacturing_cost, on='Product type')

result.rename(columns = {'Lead time': 'Average Lead Time', 'Manufacturing costs': 'Average Manufacturing Costs'}, inplace = True)

print(result)

#COMMENT: Average lead time and average manufacturing costs for cosmetics is the lowest.

#Analyzing SKUs to get 10 SKUs which outperform all other SKUs

sku_revenue = data.groupby('SKU')['Revenue generated'].sum().reset_index()

top_n = 10
top_n_sku = sku_revenue.sort_values(by="Revenue generated", ascending = False).head(top_n)

top_sku_data = data[data['SKU'].isin(top_n_sku['SKU'])].sort_values(by="Revenue generated", ascending=False)

revenue_chart = px.line(top_sku_data, x = "SKU", y = "Revenue generated", title = "Revenue Generated by top 10 SKU")

revenue_chart.show()

sku_stock = data.groupby('SKU')['Stock levels'].sum().reset_index()

top_n_sku_stock = sku_stock.sort_values(by="Stock levels", ascending = False).head(top_n)

top_sku_stock_data = data[data['SKU'].isin(top_n_sku_stock['SKU'])].sort_values(by="Stock levels", ascending=False)

stock_chart = px.line(top_sku_stock_data, x = "SKU", y = "Stock levels", title = "Stock levels by top 10 SKU")

stock_chart.show()

sku_quantity = data.groupby('SKU')['Order quantities'].sum().reset_index()

top_n_sku_order = sku_quantity.sort_values(by="Order quantities", ascending = False).head(top_n)

top_sku_order_data = data[data['SKU'].isin(top_n_sku_order['SKU'])].sort_values(by="Order quantities", ascending=False)

order_quantity_chart = px.bar(top_sku_order_data, x = "SKU", y = "Order quantities", title = "Order Quantity by top 10 SKU")

order_quantity_chart.show()

#COMMENT: 