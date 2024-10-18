# Importing libraries
import pandas as pd
import mysql.connector
import streamlit as slt
from streamlit_option_menu import option_menu

# Load the single CSV file
df = pd.read_csv("Final_busdetails_df.csv")

# Extract unique route names for the select box options
lists_routes = df['Route_name'].unique()

# Setting up Streamlit page
slt.set_page_config(layout="wide")

web = option_menu(
    menu_title="🚌 OnlineBus",
    options=["Home", "📍 States and Routes"],
    icons=["house", "info-circle"],
    orientation="horizontal"
)

# Home page setting
if web == "Home":
    slt.image("image.jpeg", width=200)
    slt.title("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")
    slt.subheader(":blue[Domain:] Transportation")
    slt.subheader(":blue[Objective:] ")
    slt.markdown(
        "The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data..."
    )
    slt.subheader(":blue[Skills:]")
    slt.markdown("Selenium, Python, Pandas, MySQL, mysql-connector-python, Streamlit.")
    slt.subheader(":blue[Developed by:] Bharath Roshan")

# States and Routes page setting
if web == "📍 States and Routes":
    selected_route = slt.selectbox("Select Route", lists_routes)

    col1, col2 = slt.columns(2)
    with col1:
        select_type = slt.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = slt.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
    TIME = slt.time_input("Select the time")

    def type_and_fare(bus_type, fare_range):
        """Fetch bus details based on bus type and fare range."""
        try:
            conn = mysql.connector.connect(
                host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
                port=4000,
                user="3tP2n3cmYGyRe9X.root",
                password="74Yie0ZCA7nyFVTo",
                database="project"  # Change this if needed
            )
            my_cursor = conn.cursor()

            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper":
                bus_type_condition = "Bus_type LIKE '%Sleeper%'"
            elif bus_type == "semi-sleeper":
                bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
            else:
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{selected_route}"
                AND {bus_type_condition} AND Start_time >= '{TIME}'
                ORDER BY Price, Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()

            # Closing the cursor after executing the query
            my_cursor.close()
            conn.close()

            # Create a DataFrame from the results
            df_result = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df_result
        except mysql.connector.Error as err:
            slt.error(f"Error: {err}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    df_result = type_and_fare(select_type, select_fare)
    slt.dataframe(df_result)
