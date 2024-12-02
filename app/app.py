# Home Page
%%writefile app.py
import streamlit as st
import pandas as pd # Import pandas for DataFrame handling
from Visualization import app as viz_app
from Findings import app as find_app

# Load the merged DataFrame (Assuming it's saved as airQuality_combined.cs
df = pd.read_csv('airQuality_combined.csv')
PAGES = {
    "Home": lambda: (home_page(df)),
    "Visualizations": viz_app,
    "Findings": find_app
}

def home_page(df):  # Define the home_page function
    st.title("Welcome to the Air Quality Analysis App!")
    st.write("This app explores air quality data from Beijing, China, between 2013 and 2017.")
    st.write("The data includes measurements of various pollutants, temperature, pressure, and other environmental factors.")
    st.write("Use the sidebar to navigate to different sections of the app.")
    st.write("---")  # Separator
    st.subheader("Merged Data Preview")
    st.dataframe(df.head(10))  # Display the first 10 rows of the DataFrame
    # Create columns for side-by-side display
    col1, col2, col3 = st.columns(3)

    # Column 1: Display DataFrame shape
    with col1:
        st.write("**Total Shape:**")
        st.write(f"{df.shape}")

    # Column 2: Display data types
    with col2:
        st.write("**Data Types:**")
        st.write(df.dtypes.to_frame('Type').rename_axis('Column').reset_index())

    # Column 3: Display column names
    with col3:
        st.write("**Column Names:**")
        st.write(list(df.columns))

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page()

