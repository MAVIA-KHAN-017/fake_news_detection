import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# from pydeck import deck_gl_chart
import numpy as np
import pydeck as pdk
def load_data():
    df = pd.read_csv("Crimes_2001_to_Present.csv")
    df=df.dropna()
    return df
# def get_block(df):
#     return sorted(df["Block"].unique())
def get_location(df):
    return sorted(df['Block'].unique())
    # return sorted(df["Location Description"].unique())
def main():
    # Load data
    df = load_data()
    # df_block = get_block(df)
    # # Get list of all available states
    location=get_location(df)
    # Set the title of the dashboard
    st.title('Chicago Crime Rate- 2001 to Present')
    # Add some text
    st.subheader('Crime Data Set')
    st.markdown('Streamlit Dashboard :bar_chart: :chart_with_upwards_trend: :male-technologist::skin-tone-2: :desktop_computer:')
    # Display the data as a table
    st.write(df.head(200))
    # Add a drop-down widget to select state
    selected_block=st.sidebar.selectbox("LOCATION", location)
    filtered_data = df[df["Block"] == selected_block]
    st.write(filtered_data.head(200))
    col1, col2, col3, col4= st.columns(4)
    col1.metric(label="Total number of Crimes", value=filtered_data["Case Number"].nunique())
    st.subheader("Horizontal Bar Plot of Number of Crimes by Primary Type")
    histogram_chart= filtered_data.groupby("Primary Type").size()
    st.bar_chart(histogram_chart)
    # Sidebar for user input
    st.sidebar.title('Crime Selection')
    crime_list = filtered_data['Primary Type'].unique()
    selected_crime = st.sidebar.selectbox('Select a crime type:', crime_list)
    # Filter the DataFrame for the selected crime
    crime_df = filtered_data[filtered_data['Primary Type'] == selected_crime]
    # Extract time information
    crime_df['Time'] = pd.to_datetime(crime_df['Date']).dt.time
    # Group the data by time and count occurrences
    crime_count_by_time = crime_df.groupby('Time').size().reset_index(name='Count')
    # Plot the line graph using Plotly
    fig = px.line(crime_count_by_time, x='Time', y='Count', title=f'Trend of {selected_crime} Over Time')
    fig.update_xaxes(title='Time')
    fig.update_yaxes(title='Number of Crimes')
    # Show the plot in the Streamlit app
    st.plotly_chart(fig)
    st.title('Crime Map of Chicago')
    # Filter out rows with missing latitude and longitude values
    hotspots = filtered_data.dropna(subset=['Latitude', 'Longitude'])
    # Plot the crime locations on a map using Plotly Express
    fig = px.scatter_mapbox(
        hotspots,
        lat='Latitude',
        lon='Longitude',
        color='Primary Type',
        hover_name='Primary Type',
        hover_data=['Description'],
        mapbox_style='carto-positron',
        zoom=100,
        title='Crime Map of Chicago'
    )
    # Customize the map layout
    fig.update_layout(
        mapbox=dict(
            bearing=0,
            center=dict(lat=41.8781, lon=-87.6298),  # Chicago's latitude and longitude
            pitch=0,
            zoom=10
        ),
    )
    # Extract time information
    df['Time'] = pd.to_datetime(df['Date']).dt.time
    # Group the data by time and count occurrences
    crime_count_by_time = df.groupby('Time').size().reset_index(name='Count')
    # Plot the correlation using Plotly Express
    fig = px.scatter(
        crime_count_by_time,
        x='Time',
        y='Count',
        title='Correlation between Time and Number of Crimes',
        trendline='ols'  # Add a linear trendline to visualize the correlation
    )
    # Show the plot in the Streamlit app
    st.plotly_chart(fig)
    # Show the map in the Streamlit app
    st.plotly_chart(fig)
# Run the app
if __name__ == "__main__":
    main()