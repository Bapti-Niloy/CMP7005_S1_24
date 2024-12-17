import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import time
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
    st.title("Visualizations")
    st.write("Explore visual insights.")

    st.title("📊 Real-Time Pollutant Monitoring")

    df = st.session_state["data"]
    df = preprocess_data(df)

    # Select Station for Real-Time Monitoring
    station = st.selectbox("Select a Station for Monitoring:", df['station'].unique())
    refresh_interval = st.slider("Refresh Interval (seconds)", 1, 10, 5)

    # Real-time updates
    placeholder = st.empty()
    while True:
        # Filter and display the latest data
        recent_data = df[df['station'] == station].tail(20)
        fig = px.line(
            recent_data,
            x="date",
            y=["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"],
            title=f"Real-Time Pollutant Levels at {station}",
            markers=True
        )
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(refresh_interval)

    df = st.session_state["data"]

    # Create 'date' column using day, month, and year
    if all(col in df.columns for col in ['day', 'month', 'year']):
        df['date'] = pd.to_datetime(df[['day', 'month', 'year']], errors='coerce')
    else:
        st.error("The dataset must contain 'day', 'month', and 'year' columns to construct the 'date' column.")
        return

    # Drop rows with invalid or missing dates
    #df = df.dropna(subset=['date'])

    # Convert relevant columns to numeric
    numeric_cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

    # Calculate AQI
    df = calculate_aqi(df)

    # Histogram with dropdown filters
    selected_pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    fig = px.histogram(df, x='station', y=selected_pollutants, title='Mean Pollutant Levels by Station', barmode='stack')
    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                buttons=[
                    dict(args=[{"visible": [True] * 6}], label="All Pollutants"),
                    *[dict(args=[{"visible": [i == j for j in range(6)]}], label=p) for i, p in enumerate(selected_pollutants)],
                ],
            )
        ]
    )
    st.plotly_chart(fig)

    # Monthly average line plot
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month
    monthly_avg = df.groupby(['Year', 'Month'])[numeric_cols].mean().reset_index()
    monthly_avg['Date'] = pd.to_datetime(monthly_avg[['Year', 'Month']].assign(DAY=1))
    fig = px.line(monthly_avg, x="Date", y=selected_pollutants, title="Monthly Average Pollutant Concentrations")
    fig.update_layout(xaxis_title="Date", yaxis_title="Concentration (ug/m3)", hovermode="x unified")
    st.plotly_chart(fig)

    # Set 'date' as index
    df.set_index('date', inplace=True)

    # Pollutant selection
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM', 'AQI']
    selected_pollutant = st.selectbox("Select a pollutant to view its graph:", pollutants)

    # Plot selected pollutant
    st.subheader(f"Time-Series Plot for {selected_pollutant}")
    fig, ax = plt.subplots(figsize=(16, 6))
    df[selected_pollutant].plot(marker='.', alpha=0.5, linestyle='None', ax=ax, title=f"{selected_pollutant} Over Time")
    ax.set_xlabel("Years")
    ax.set_ylabel("Concentration (ug/m3)")
    st.pyplot(fig)

    # Pairwise scatter plots
    pollutants_df = df[selected_pollutants].dropna()
    pairplot_fig = sns.pairplot(pollutants_df, diag_kind="kde", plot_kws={"alpha": 0.5})
    plt.suptitle('Pairwise Scatter Plots of Pollutants', y=1.02)
    st.pyplot(pairplot_fig.figure)

    # Sunburst chart: Mean pollutant values per station
    mean_pollutant_per_station = df.groupby('station')[selected_pollutants].mean()
    melted = mean_pollutant_per_station.reset_index().melt(id_vars='station', var_name='Pollutant', value_name='Mean Value')
    fig = px.sunburst(melted, path=['station', 'Pollutant'], values='Mean Value', color='Mean Value')
    fig.update_layout(title='Mean Pollutant Values per Station')
    st.plotly_chart(fig)

    # Sunburst chart: AQI by station and year
    st.subheader("Sunburst Chart: AQI by Station and Year")
    df.reset_index(inplace=True)  # Make 'date' a column
    df['Year'] = df['date'].dt.year
    fig = px.sunburst(df, path=['station', 'Year'], values='AQI', color='AQI', color_continuous_scale='RdYlGn_r')
    fig.update_layout(title='Mean AQI by Station and Year')
    st.plotly_chart(fig)
    df.set_index('date', inplace=True)  # Restore 'date' as index
