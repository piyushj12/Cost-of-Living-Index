import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

# Load the data
data = pd.read_csv("costofliving.csv")

# Set page title
st.set_page_config(page_title="Cost of Living Index Insights", page_icon=":chart_with_upwards_trend:")
# Select the top 50 cities
top_cities = data.sort_values(by='Cost of Living Index', ascending=False).head(50)

#spliting the city and country
new_df=data.copy()
city_country = []
for row in new_df['City']:
    try:
        city, _, country = row.partition(',')[3].strip()
    except IndexError:
        city, country  = row, ''
    city_country.append((city, country))
new_df[['City', 'Country names']] = pd.DataFrame(city_country, columns=['City', 'Country'])


# Create a sidebar for selecting the analysis
analysis = st.sidebar.selectbox("Select Analysis", [ "Overview of the Dataset","Rental Prices by City","Most Expensive cities to live","Groceries index by city","Restuarants by city","Purchasing Power Index", "cost of living index", "choropleth","Summary"])



# Define the functions for each analysis

def show_data():
    st.subheader("About the Data")
    st.write("The project goal of the cost of living index by city dataset is to provide a comprehensive analysis of the cost of living in different cities worldwide, to help individuals and businesses about where to live and invest. This helps to explore the relationship between the cost of living, local salaries, and standard of living in different cities, and to identify the cities where residents have the highest and lowest purchasing power.\n\n ")
   
    st.write(data)
    st.subheader("Dataset Attributes")
    st.write("**Rank**: This represents the rank of each city based on the cost of living index.\n\n**City**: This is the name of the city being analyzed in the dataset.\n\n**Cost of living index**: This is a measure of how expensive is to live in a particular city.\n\n**Rent index**: This is the measure of how expensive is to rent a place to live in a city.\n\n**Cost of the living index plus rent index**: This is the sum of the cost of living index and rent index which represents the overall cost of living for someone renting a place in a city.\n\nGroceries index**: This is a measure of how expensive groceries are in the city.\n\n**Local purchasing power index**: This is a measure of how much purchasing power the average person in the city has, This includes the cost of living, and local salaries, and indicates how much people can afford to buy with their money within the city.\n\n**Restaurant price index**: This is a measure of how expensive is to eat out at restaurants in a city.\n\n")

                                                    
def most_expensive_cities():
    st.subheader("Most Expensive Cities to Live In")
    # Using a horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 20))
    sns.barplot(x='Cost of Living Index', y='City', data=top_cities, palette='rocket')
    plt.title("Most Expensive Cities to Live In")
    plt.xlabel("Cost of Living Index")
    plt.ylabel("City")
    plt.xticks(rotation=90)
    st.pyplot(fig)
    st.markdown('City with Highest Cost of living index is **Hamilton, Bermuda** with an index of 149.02.')
    # Calculate the average of the "column_name" column
    average_CLRI = data["Cost of Living Plus Rent Index"].mean()
    st.write("The average Cot of Living Index is **{:.2f}**".format(average_CLRI))

def groceries_index():
    st.subheader("Grocery Prices by City")
    # Using a box plot
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x='Groceries Index', data=top_cities, orient='h', palette='rocket')
    plt.title("Grocery Prices by City")
    plt.xlabel("Groceries Index")
    st.pyplot(fig)
    st.markdown('City with Highest Grocery Price index is **Hamilton, Bermuda** with an index of 149.02.')
    average_GPC = data["Groceries Index"].mean()
    st.write("The average Grocery Price Index is **{:.2f}**".format(average_GPC))



def restuarant_index():
    st.subheader("Restaurant and Food Prices by City")
    # Using a grouped bar chart
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.barplot(x='City', y='value', hue='variable', data=pd.melt(top_cities[['City', 'Restaurant Price Index']], ['City']), palette='rocket')
    plt.title("Restaurant and Food Prices by City")
    plt.xlabel("City")
    plt.ylabel("Index")
    plt.xticks(rotation=90)
    st.pyplot(fig)
    st.markdown('City with Highest Restaurant and Food Index is **Hamilton, Bermuda** with an index of 155.22.')
    average_RFI = data["Restaurant Price Index"].mean()
    st.write("The average cost Index for restaurants and food is **{:.2f}**".format(average_RFI))
                                                    

def cost_of_living_index():

    st.subheader("Cities versus cost of living index using Heatmap")
    df_pivot = top_cities.pivot(index='City', columns='Cost of Living Index', values='Cost of Living Index')

    # Create the heatmap using Seaborn
    heatmap = sns.heatmap(df_pivot, cmap='YlOrRd')

    # Set the title and axis labels
    title = "Cost of Living Index by City"
    x_axis = "Cost of Living Index"
    y_axis = "City"

# Display the chart in the Streamlit app
    st.pyplot(heatmap.get_figure())
    st.markdown('City with Highest Cost of Living Index is **Hamilton, Bermuda** with an index of 149.02.')
    average_RI = data["Rent Index"].mean()
    st.write("The average Rental Price is **{:.2f}**".format(average_RI))

def rental_prices():
    # Create a bar chart of the rental prices by city
    st.subheader("Rental Prices by City")
    # Using a scatter plot with regression line
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(x='Rent Index', y='Cost of Living Index', data=top_cities)
    plt.title("Rental Prices vs. Cost of Living Index")
    plt.xlabel("Rent Index")
    plt.ylabel("Cost of Living Index")
    st.pyplot(fig)
    st.markdown('City with Highest rental Price is **San Francisco, CA, United States** with an index of 108.42.')
    average_RI = data["Rent Index"].mean()
    st.write("The average Rental Price is **{:.2f}**".format(average_RI))
    
def purchasing_power():
    
    st.subheader("Purchasing Power Index")
# Group the data by city and compute the mean of the local purchasing power
    grouped = top_cities.groupby('City').mean()['Local Purchasing Power Index'].reset_index()

# Sort the data by local purchasing power index
    grouped = grouped.sort_values(by='Local Purchasing Power Index')

# Create the bar chart using Altair
    bars = alt.Chart(grouped).mark_bar().encode(
    x=alt.X('Local Purchasing Power Index', title='Local Purchasing Power Index'),
    y=alt.Y('City', sort=alt.EncodingSortField('Local Purchasing Power Index', order='descending'), title='City')
    )

# Set the title and axis labels
    title = "Local Purchasing Power Index by City"
    x_axis = "Local Purchasing Power Index"
    y_axis = "City"

# Display the chart in the Streamlit app
    st.altair_chart(bars, use_container_width=True)
    st.markdown('City with Highest Purchasing Power is **Houston, TX, United States** with an index of 172.98.')
    average_LPP = data["Local Purchasing Power Index"].mean()
    st.write("The average cost Index for restaurants and food is **{:.2f}**".format(average_LPP))
def choropleth():
    fig = px.choropleth(data_frame=new_df,
                    locations='City',
                    locationmode='country names',
                    color='Cost of Living Index',
                    hover_name='City',
                    title='Cost of Living Index by City',
                    color_continuous_scale='YlOrRd',
                    scope='world')

    # Show the map
    fig.show()
#Summmary Page
def Summary():
    st.subheader("Summary")
    st.write("Our project is to analyze the cost of living in different cities around the world using a dataset that provides a cost of living index score based on goods, groceries, housing, and restaurants. Scores above 100 mean higher costs of living. We aim to identify cities with the highest and lowest purchasing power by analyzing rankings, city names, cost of living index scores, rent index scores, combined cost of living and rent index scores, grocery and restaurant price index scores, and local purchasing power index scores. We will explore the most expensive cities to live in, rental price variations, cities with high/low grocery prices, variations in restaurant and food prices, and cities with high/low local purchasing power. \n\n Our analysis of the cost of living in different cities around the world can help you make informed decisions when choosing a place to live or invest. By understanding the cost of goods, groceries, housing, and restaurants in different cities, we can help you identify cities with the highest and lowest purchasing power to make the most of your budget.")
    # Define the list of authors
    authors = ["--By","Piyush Jain", "Sai Nikhil Botla", "Tharun Abhinav Suraneni","Ilyas Safi"]
# Get the app's content container and add some padding
    content_container = st.container()
    content_container.empty()
    content_container.write("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
    content_container.write("<style>.main {padding-bottom: 3rem;}</style>", unsafe_allow_html=True)

# Add the authors' names to the content container using Markdown
    st.write("\n\n")
    authors_html = "<br>".join(authors)
    content_container.write(f"<div style='bottom:0; right:0;'>{authors_html}</div>", unsafe_allow_html=True)
# Call the appropriate function based on the user's selection

if analysis == "Rental Prices by City":
    rental_prices()
elif analysis =="Most Expensive cities to live":
    most_expensive_cities()
elif analysis =="Groceries index by city":
    groceries_index()
elif analysis =="Restuarants by city":
    restuarant_index()
elif analysis =="Purchasing Power Index":
    purchasing_power()
elif analysis == "cost of living index":
    cost_of_living_index()
elif analysis=="choropleth":
    choropleth()
elif analysis =="Overview of the Dataset":
     show_data()
elif analysis == "Summary":
    Summary()
    
    
