
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

def app():
    st.title("Visualizations")
    st.write("Explore the visual insights.")

    # Load the dataset
    df = pd.read_csv('airQuality_refined.csv')  # Ensure this file is prepared and available
    # Verify column presence
    st.subheader("Dataset Columns")
    st.write(df.columns)  # Display columns for debugging

    # Ensure the dataset has the required 'date' and 'station' columns
    #if 'date' in df.columns and 'station' in df.columns and 'AQI' in df.columns:

        # Combined AQI Line Plot for All Stations
        st.subheader("AQI for All Stations Over Years")
        fig = px.line(
            df_yearly,
            x='year',
            y='AQI',
            color='station',
            title='AQI for All Stations Over Years',
            labels={'year': 'Year', 'AQI': 'AQI'},
        )
        st.plotly_chart(fig)

        # Time-Series Subplots for Individual Pollutants
        pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM', 'AQI']
        fig, axes = plt.subplots(len(pollutants), 1, figsize=(16, 20), sharex=True)
        fig.subplots_adjust(hspace=0.5)
        for i, pollutant in enumerate(pollutants):
            if pollutant in df.columns:
                df.set_index('date')[pollutant].plot(
                    ax=axes[i],
                    marker='.',
                    alpha=0.5,
                    linestyle='None',
                    title=pollutant
                )
                axes[i].set_ylabel('ug / m3')
                axes[i].set_xlabel('Years')
        st.pyplot(fig)

    #else:
        #st.error("The dataset does not contain the required columns ('date', 'station', 'AQI'). Please check the dataset structure.")
