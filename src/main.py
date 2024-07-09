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
