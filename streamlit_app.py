import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO
from datetime import datetime

# CSV file raw URL from GitHub
GITHUB_CSV_URL = 'https://raw.githubusercontent.com/23882972/Driving-Assistance-Sensor/refs/heads/main/sensor_data.csv'

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

# Function to count rows in df
def count_rows(df):
    return len(df)

# Load CSV
df = read_web_csv()

if df is not None:
    # Show the data in the app
    st.write("Data Overview:")
    st.write(df)
    
    # Select menu for image of the driver
    selected_image = st.selectbox('Select a time of an image:', df['Timestamp'])
    image_path = f'https://raw.githubusercontent.com/23882972/Driving-Assistance-Sensor/main/photos/{selected_image}.jpg'
    st.image(image_path, caption="Image of the driver during the buzzer", use_column_width=True)
    
    # First line graph of time against acceleration
    fig = px.line(df, x='Timestamp', y='Total_Acceleration', title='Line Graph of Time against Acceleration during buzzer')
    st.plotly_chart(fig)
    
    # Second line graph of time against distance
    fig2 = px.line(df, x='Timestamp', y='Distance', title='Line Graph of Time against Distance during buzzer')
    st.plotly_chart(fig2)
    
    # Buzzer counter
    buzzer_count = count_rows(df)
    st.write(f"Number of buzzers triggered by driver: {buzzer_count}")
    
    # Time period
    initial_time = df.at[0, 'Timestamp']
    final_time = df.at[buzzer_count - 1, 'Timestamp']
    st.write(f"Time period: from {initial_time} to {final_time}")
    
    # Calculation of taken tim
    time_format = '%Y-%m-%d_%H-%M-%S'
    start_time = datetime.strptime(initial_time, time_format)
    end_time = datetime.strptime(final_time, time_format)
    time_diff = end_time - start_time
    minutes = time_diff.total_seconds() / 60
    st.write(f"Time taken: {minutes:.2f} minutes")
    
    # Buzzer rate aka driver's rating
    buzzer_rate = buzzer_count / minutes
    st.write(f"Driver's buzzer rate: {buzzer_rate:.2f} buzzers per minute")
    rating = ""
    if buzzer_rate > 5:
        rating = "Dangerous"
    elif buzzer_rate <=5 or buzzer_rate > 2:
        rating = "Normal"
    else:
        rating = "Accurate"
    st.write(f"Driver's driving rating: {rating}")
