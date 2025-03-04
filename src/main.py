#All required imports
import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from opencage.geocoder import OpenCageGeocode

#Set all the pio templates to be white in color for consistency.
pio.templates.default = "plotly_white"

#Load and peek at the data.
data = pd.read_csv("../dataset/supply_chain_data.csv")
print(data.head())

#Descriptive statistics
print(data.describe())

#EDA for supply chain
fig = px.scatter(data,
                 x = "Price",
                 y = "Revenue generated",
                 color = 'Product type',
                 hover_data = ['Number of products sold'],
                 trendline = "ols")
fig.show()

#COMMENT: It is evident from the plot that skincare products generate more revenue. Higher the prices of the skincare products, higher the revenue generated.

#Sales data by product type

sales_data = data.groupby('Product type')['Number of products sold'].sum().reset_index()

pie_chart = px.pie(sales_data,
                   values = 'Number of products sold',
                   names = 'Product type',
                   title = 'Sales by Product Type',
                   hover_data = ['Number of products sold'],
                   hole = 0.5,
                   color_discrete_sequence=px.colors.qualitative.Pastel)

pie_chart.update_traces(textposition = 'inside', textinfo = 'percent+label')
pie_chart.show()

#COMMENT: This pie chart shows that 45% of the business comes from skincare, 29.5% from haircare, and 25.5% comes from cosmetics.

#Total Revenue generated from shipping carriers

total_revenue = data.groupby('Shipping carriers')['Revenue generated'].sum().reset_index()

bar_chart = go.Figure()

bar_chart.add_trace(go.Bar(x = total_revenue['Shipping carriers'],
                           y = total_revenue['Revenue generated']))

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

revenue_chart = px.line(top_sku_data,
                        x = "SKU",
                        y = "Revenue generated",
                        title = "Revenue Generated by top 10 SKU")

revenue_chart.show()

sku_stock = data.groupby('SKU')['Stock levels'].sum().reset_index()

top_n_sku_stock = sku_stock.sort_values(by="Stock levels", ascending = False).head(top_n)

top_sku_stock_data = data[data['SKU'].isin(top_n_sku_stock['SKU'])].sort_values(by="Stock levels", ascending=False)

stock_chart = px.line(top_sku_stock_data,
                      x = "SKU",
                      y = "Stock levels",
                      title = "Stock levels by top 10 SKU")

stock_chart.show()

sku_quantity = data.groupby('SKU')['Order quantities'].sum().reset_index()

top_n_sku_order = sku_quantity.sort_values(by="Order quantities", ascending = False).head(top_n)

top_sku_order_data = data[data['SKU'].isin(top_n_sku_order['SKU'])].sort_values(by="Order quantities", ascending=False)

order_quantity_chart = px.bar(top_sku_order_data,
                              x = "SKU",
                              y = "Order quantities",
                              title = "Order Quantity by top 10 SKU")

order_quantity_chart.show()

#COMMENT: This gave us an analysis of which 10 SKUs are most profitable, which 10 SKUs stock levels are always good, and which 10 SKUs are ordered the most.

#Carrier Shipping Cost Analysis

shipping_cost_chart = px.bar(data,
                             x = "Shipping carriers",
                             y = "Shipping costs",
                             title = "Shipping Costs by Carrier")

shipping_cost_chart.show()

#COMMENT: Though Carrier B helps the company generate the most revenue, it can be seen that it is the most expensive among the three carriers.
# The reason that it is most sought can be its popularity, positive reviews, etc.

#Cost and Mode of Transportation distribution

transportation_chart = px.pie(data,
                              values = "Shipping costs",
                              names = "Transportation modes",
                              title = "Cost Distribution by Transportation Mode",
                              hole = 0.5,
                              color_discrete_sequence = px.colors.qualitative.Pastel)

transportation_chart.show()

#COMMENT: From the plot, we observe that shipping costs are distributed mostly among Road, Air and the next in line is shipping costs of Rail.
# The company spends the least on transportation by sea.

#Defect Rate Analysis

defect_rates_by_product = data.groupby('Product type')['Defect rates'].mean().reset_index()

defect_rate_chart = px.bar(defect_rates_by_product,
                           x = "Product type",
                           y = "Defect rates",
                           title = "Average Defect Rates by Product Type")

defect_rate_chart.show()

#COMMENT: It can be observed that the defect rate is the highest in haircare products. From the previous analysis, we know the haircare products do not contribute to the revenue that much.
# Along with that, the average lead time and average manufacturing costs of haircare products is on the higher end.
# The company should make a business decision about looking into how to make the haircare products less defective or generating more revenue.

#Defect Rates by Mode of transportation

defect_rates_by_transportation = pd.pivot_table(data, values = 'Defect rates', index = ['Transportation modes'], aggfunc = 'mean')

defect_rate_transport_chart = px.pie(values = defect_rates_by_transportation['Defect rates'],
                                     names = defect_rates_by_transportation.index,
                                     title = "Defect Rates by Transportation Mode",
                                     hole = 0.5,
                                     color_discrete_sequence = px.colors.qualitative.Pastel)

defect_rate_transport_chart.show()

#COMMENT: This shows that even though the company spends almost equally on transportation modes like Road and Air, the defect rates in both these modes are on the extreme sides of the range.
# The defect rate is lowest for Air transportation and highest on the Road transportation.

#Customer Demographics Analysis

demographics_sales = data.groupby('Customer demographics')['Revenue generated'].sum().reset_index()

demographics_chart = px.bar(demographics_sales,
                            x = "Customer demographics",
                            y = "Revenue generated",
                            title = "Revenue Generated by Customer Demographics")

demographics_chart.show()

#COMMENT: As we see that, we have unknown in the data and that too the highest revenue generated is by the Unkwown group. We should look more into it.
# Out of the known demographics data, we observe the highest revenue generated is by Females which is expected as this is a Fashion and Beauty company which sells cosmetics, haircare, and skincare products.

#Unkown Data Analysis (What they bought and Where are they from)
unknown_data = data[data['Customer demographics'] == 'Unknown']

unknown_product_type = unknown_data['Product type'].value_counts()
unknown_location = unknown_data['Location'].value_counts()

print("Distribution of Product Types within 'Unknown' Demographic:")
print(unknown_product_type)

print("\nDistribution of Locations within 'Unknown' Demographic:")
print(unknown_location)

#COMMENT: 31% of the data belongs to the Unknown demographics. We can see people in that demographics bought more haircare products and not cosmetics or skincare, which might mean that there are more males.
# or equal distribution as both males and females use haircare products, whereas a more common usage of skincare and cosmetics are seen in females.

#Route Efficiency Analysis

route_efficiency = data.groupby('Routes').agg({'Costs': 'mean', 'Defect rates': 'mean'}).reset_index()

route_efficiency_chart = px.scatter(route_efficiency,
                                    x = "Costs",
                                    y = "Defect rates",
                                    size = "Defect rates",
                                    hover_name = "Routes",
                                    title = "Route Efficiency")

route_efficiency_chart.show()

#COMMENT: Route C costs the lowest and the defect rate is also lowest on Route C. On both the other routes, the defect rate is comparatively higher.
# With route B, the company is losing on costs as well as the defect rate is marginally away from the highest defect rate. Company should look into it.

#Correlation Analysis

numerical_data = data.select_dtypes(include=['float64', 'int64'])

correlation_matrix = numerical_data.corr()

heatmap = px.imshow(correlation_matrix, title = "Correlation Matrix")

heatmap.show()

encoded_data = pd.get_dummies(data, drop_first=True)

correlation_matrix = encoded_data.corr()

strong_corr = correlation_matrix[(correlation_matrix > 0.5) | (correlation_matrix < -0.5)]

heatmap = px.imshow(strong_corr, title = "Correlation Matrix")

heatmap.show()

#COMMENT: Correlation analysis is inconclusive due to either lack of strong correlations or the presence of many weak correlations that are insignificant.
# It tells us that not every analysis is always useful.

#Geographical Analysis

opencage_api_key = input("Please enter your opencage API key.\n")
geocoder = OpenCageGeocode(opencage_api_key)

# Function to get latitude and longitude
def get_lat_lon(city):
    query = city + ", India"
    results = geocoder.geocode(query)
    if results and len(results):
        return results[0]['geometry']['lat'], results[0]['geometry']['lng']
    else:
        return None, None

# Get latitude and longitude for each city
data[['Latitude', 'Longitude']] = data['Location'].apply(lambda x: pd.Series(get_lat_lon(x)))

# Drop rows with missing coordinates
data = data.dropna(subset=['Latitude', 'Longitude'])

# Create the bubble map
bubble_map = px.scatter_geo(
    data,
    lat='Latitude',
    lon='Longitude',
    size='Revenue generated',
    color='Revenue generated',
    hover_name='Location',
    size_max=50,
    title='Revenue Generated by City'
)

bubble_map.update_geos(
    projection_type="natural earth",
    resolution=50,
    showcountries=True,
    countrycolor="Black",
    showcoastlines=True,
    coastlinecolor="Black",
    showland=True,
    landcolor="lightgray",
    fitbounds="locations",
    center=dict(lat=20.5937, lon=78.9629),
    lataxis=dict(range=[6, 37]),
    lonaxis=dict(range=[68, 97])
)

bubble_map.show()

#COMMENT: This geographical analysis shows the distribution of the business across the country and how is the concentration of revenue in each area.