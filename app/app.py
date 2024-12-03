# Home Page
# app.py
import streamlit as st
import pandas as pd
from Visualization import app as viz_app
from train_model import app as train_app
from Findings import app as find_app

# Cache the data loading function
@st.cache_data
def load_data():
    df = pd.read_csv('airQuality_combined.csv')
    return df

# Initialize session state
if "data" not in st.session_state:
    st.session_state["data"] = load_data()

# Page routing
PAGES = {
    "Home": lambda: home_page(st.session_state["data"]),
    "Visualizations": viz_app,
    "Train Model": train_app, 
    "Findings": find_app
}

def home_page(df):
    """Home page with dataset preview and basic stats."""
    st.title("Welcome to the Air Quality Analysis App!")
    st.write("This app explores air quality data from Beijing, China, between 2013 and 2017.")
    st.write("---")
    st.subheader("Merged Data Preview")
    st.dataframe(df.head(10))

    # Display dataset stats in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Total Shape:**", df.shape)
    with col2:
        st.write("**Data Types:**")
        st.dataframe(df.dtypes.reset_index().rename(columns={"index": "Column", 0: "Type"}))
    with col3:
        st.write("**Column Names:**", df.columns.tolist())

# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES.get(selection, lambda: st.error("Page not found."))
page()
