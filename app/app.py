import streamlit as st
import pandas as pd
from Visualization import app as viz_app
from train_model import app as train_app
from Findings import app as find_app

# Cache the data loading function
@st.cache_data
def load_data():
    # Get the absolute path to the directory containing the app
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the CSV file
    file_path = os.path.join(base_dir, 'airQuality_combined.csv')
    df = pd.read_csv(file_path)
    return df

# Initialize session state
if "data" not in st.session_state:
    st.session_state["data"] = load_data()
    
# Home Page Function
def home_page(df):
    # Header
    st.title("🏙️ Beijing Air Quality Analysis Dashboard")
    st.markdown(
        """
        ### Welcome to the Beijing Air Quality Analysis Dashboard!  
        This interactive app provides insights into the air quality trends and patterns in **Beijing, China** between **2013 and 2017**.
        """,
        unsafe_allow_html=True
    )
    st.write("---")

    # Purpose Section
    st.subheader("🎯 Purpose")
    st.markdown(
        """
        This app aims to:
        - 📊 Explore historical air quality data from various monitoring stations across Beijing.  
        - 📈 Visualize trends and patterns in key air pollutants like **PM2.5**, **PM10**, **SO2**, **NO2**, **CO**, and **O3**.  
        - 🏭 Identify stations and periods with the **highest pollution levels**.  
        - 🔗 Analyze the **relationships** between different pollutants.  
        - 🖥️ Provide an interface for **interactive exploration** and **data visualization**.
        """,
        unsafe_allow_html=True
    )
    st.write("---")

    # Data Source Section
    st.subheader("📂 Data Source")
    st.markdown(
        """
        - The data used in this app was collected from **12 air quality monitoring stations** in Beijing between **2013 and 2017**.  
        - It includes hourly measurements of various pollutants and meteorological parameters like **temperature**, **pressure**, and **wind speed**.  
        - The dataset was obtained from the **UCI Machine Learning Repository** and preprocessed for this analysis.
        """
    )
    st.write("---")

    # Dataset Preview
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(10))
    st.write(f"**Total Rows:** {df.shape[0]} | **Total Columns:** {df.shape[1]}")

    # Footer
    st.markdown(
        """
        ---
        **Created by [Bapti Niloy Sarkar](mailto:baptiniloy@gmail.com)**  
        """,
        unsafe_allow_html=True
    )

# Page routing
PAGES = {
    "Home": lambda: home_page(st.session_state["data"]),
    "Visualizations": viz_app,
    "Train Model": train_app, 
    "Findings": find_app
}

# Initialize session state
if "data" not in st.session_state:
    st.session_state["data"] = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES.get(selection, lambda: st.error("Page not found."))
page()
