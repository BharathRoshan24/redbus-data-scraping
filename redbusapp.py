#!/usr/bin/env python
# coding: utf-8

# In[2]:


# importing libraries
import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu

# Load the single CSV file containing all the bus details
df = pd.read_csv("Final_busdetails_df.csv")

# Extract unique route names for the dropdown menu
route_names = df['Route_name'].unique()

# Setting up Streamlit page
slt.set_page_config(layout="wide")

web = option_menu(
    menu_title="🚌 Online Bus",
    options=["Home", "📍 States and Routes"],
    icons=["house", "info-circle"],
    orientation="horizontal"
)

# Home page setting
if web == "Home":
    slt.image("image.jpeg", width=200)
    slt.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    slt.subheader(":blue[Domain:] Transportation")
    # ... [Rest of your introduction content]

# States and Routes page setting
if web == "📍 States and Routes":
    selected_state = slt.selectbox("List of States", ["Kerala", "Andhra Pradesh", "Telangana", "Goa", "Rajasthan"])

    col1, col2 = slt.columns(2)
    with col1:
        selected_type = slt.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        selected_fare = slt.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
    selected_time = slt.time_input("Select the time")

    # Filtering data based on user selection
    def filter_buses(state, bus_type, fare_range, time):
        fare_min, fare_max = (50, 1000) if fare_range == "50-1000" else (1000, 2000) if fare_range == "1000-2000" else (2000, 100000)
        bus_type_condition = f"Bus_type LIKE '%{bus_type.capitalize()}%'"

        filtered_df = df[
            (df['Route_name'] == state) &
            (df['Price'].between(fare_min, fare_max)) &
            (df['Start_time'] >= str(time)) &
            (df['Bus_type'].str.contains(bus_type_condition))
        ]
        return filtered_df

    # Call the filter function and display the results
    df_result = filter_buses(selected_state, selected_type, selected_fare, selected_time)
    slt.dataframe(df_result)


# In[6]:


conn = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="roshan21", 
    database="RED_BUS_DETAILS"
)


# In[ ]:




