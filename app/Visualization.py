import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def calculate_aqi(df):
    """Calculate AQI and its category for each row in the dataset."""
    def calculate_iaqi(pollutant, concentration, breakpoints):
        if concentration is None or pd.isna(concentration):
            return None
        for i in range(len(breakpoints['concentration']) - 1):
            if breakpoints['concentration'][i] <= concentration <= breakpoints['concentration'][i + 1]:
                iaqi = (
                    (breakpoints['iaqi'][i + 1] - breakpoints['iaqi'][i]) /
                    (breakpoints['concentration'][i + 1] - breakpoints['concentration'][i])
                ) * (concentration - breakpoints['concentration'][i]) + breakpoints['iaqi'][i]
                return round(iaqi)
        return None

    def get_aqi_category(iaqi):
        if iaqi is None:
            return "Unknown"
        if iaqi <= 50: return "Good"
        if iaqi <= 100: return "Moderate"
        if iaqi <= 150: return "Unhealthy for Sensitive Groups"
        if iaqi <= 200: return "Unhealthy"
        if iaqi <= 300: return "Very Unhealthy"
        return "Hazardous"

    # Define breakpoints for pollutants
    breakpoints = {
        "PM2.5": {"concentration": [0, 12, 35.5, 55.5, 150.5], "iaqi": [0, 50, 100, 150, 200]},
        "PM10": {"concentration": [0, 54, 154, 254, 354], "iaqi": [0, 54, 154, 254, 354]},
        "SO2": {"concentration": [0, 54, 154, 254, 354], "iaqi": [0, 54, 154, 254, 354]},
        "NO2": {"concentration": [0, 40, 80, 180, 280], "iaqi": [0, 40, 80, 180, 280]},
        "CO": {"concentration": [0, 40, 80, 180, 280], "iaqi": [0, 40, 80, 180, 280]},
        "O3": {"concentration": [0, 40, 80, 180, 280], "iaqi": [0, 40, 80, 180, 280]},
    }

    iaqi_columns = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    for pollutant in iaqi_columns:
        df[f"{pollutant}_IAQI"] = df[pollutant].apply(
            lambda x: calculate_iaqi(pollutant, x, breakpoints.get(pollutant, {"concentration": [], "iaqi": []}))
        )

    df["AQI"] = df[[f"{pollutant}_IAQI" for pollutant in iaqi_columns]].max(axis=1, skipna=True)
    df["AQI_Category"] = df["AQI"].apply(get_aqi_category)
    return df

def app():
    st.title("📊 Visualizations")

    # Sidebar for fixed checkboxes
    st.sidebar.title("Select Visualizations")
    show_histogram = st.sidebar.checkbox("Show Histogram: Pollutant Levels by Station", value=True)
    show_monthly_avg = st.sidebar.checkbox("Show Monthly Average Line Plot")
    show_time_series = st.sidebar.checkbox("Show Time-Series Plot")
    show_pairplot = st.sidebar.checkbox("Show Pairwise Scatter Plots")
    show_sunburst_station = st.sidebar.checkbox("Show Sunburst Chart: Mean Pollutants by Station")
    show_sunburst_aqi = st.sidebar.checkbox("Show Sunburst Chart: AQI by Station and Year")

    # Main data processing
    df = st.session_state["data"]
    if all(col in df.columns for col in ['day', 'month', 'year']):
        df['date'] = pd.to_datetime(df[['day', 'month', 'year']], errors='coerce')
    else:
        st.error("The dataset must contain 'day', 'month', and 'year' columns to construct the 'date' column.")
        return

    df = calculate_aqi(df)

    # Display visualizations based on checkboxes
    if show_histogram:
        st.subheader("Histogram: Pollutant Levels by Station")
        selected_pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
        fig = px.histogram(df, x='station', y=selected_pollutants, title="Mean Pollutant Levels by Station", barmode='stack')
        st.plotly_chart(fig)

    if show_monthly_avg:
        st.subheader("Monthly Average Pollutant Concentrations")
        monthly_avg = df.resample("M", on="date").mean()
        fig = px.line(monthly_avg, x=monthly_avg.index, y=selected_pollutants, title="Monthly Average Pollutant Concentrations")
        st.plotly_chart(fig)

    if show_time_series:
        st.subheader("Time-Series Plot")
        selected_pollutant = st.selectbox("Select a pollutant:", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'AQI'])
        fig, ax = plt.subplots()
        df.set_index('date')[selected_pollutant].plot(ax=ax, title=f"{selected_pollutant} Over Time")
        st.pyplot(fig)

    if show_pairplot:
        st.subheader("Pairwise Scatter Plots")
        sns_fig = sns.pairplot(df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].dropna())
        st.pyplot(sns_fig.figure)

    if show_sunburst_station:
        st.subheader("Sunburst Chart: Mean Pollutant Values by Station")
        melted = df.melt(id_vars='station', value_vars=['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
        fig = px.sunburst(melted, path=['station', 'variable'], values='value', color='value',color_continuous_scale='Rdylbu')
        st.plotly_chart(fig)

    if show_sunburst_aqi:
        st.subheader("Sunburst Chart: AQI by Station and Year")
        df['Year'] = df['date'].dt.year
        fig = px.sunburst(df, path=['station', 'Year'], values='AQI', color='AQI', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig)
