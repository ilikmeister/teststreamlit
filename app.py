import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# CSV file raw URL from GitHub
GITHUB_CSV_URL = 'https://raw.githubusercontent.com/23882972/Driving-Assistance-Sensor/refs/heads/main/Countries%20and%20death%20causes.csv'

def read_web_csv(url=GITHUB_CSV_URL):
    # Fetch the CSV file from the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Convert the CSV file into a pandas DataFrame
        csv_data = StringIO(response.text)
        return pd.read_csv(csv_data)  # Return DataFrame directly
    else:
        raise Exception(f"Failed to retrieve CSV file. Status code: {response.status_code}")

# Load CSV
df = read_web_csv()

if df is not None:
    # Show the data in the app
    st.write("Data Overview:")
    st.write(df.head())

    # Plotting: Ensure 'Year' and 'Smoking' columns exist in the DataFrame
    if 'Year' in df.columns and 'Smoking' in df.columns:
        fig = px.line(df, x='Year', y='Smoking', title='Smoking Data Over Time')
        st.plotly_chart(fig)
    else:
        st.warning("The DataFrame does not contain 'Year' or 'Smoking' columns.")

    # Ensure there are appropriate columns to filter by
    death_cause_columns = df.columns[4:31]  # Adjust as necessary based on your data structure
    if not death_cause_columns.empty:
        death_cause = st.selectbox('Select Cause of Death', death_cause_columns)
        filtered_data = df[df[death_cause].notna()]  # Filter for the selected cause
        st.write(filtered_data[[ 'Year', death_cause]])  # Show only relevant columns
    else:
        st.warning("No causes of death available to select.")

