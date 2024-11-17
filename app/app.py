import streamlit as st

st.set_page_config(
    page_title="Interactive Data App",
    page_icon="📊",
    layout="wide",
)

st.sidebar.title("Navigation")
st.sidebar.write("Use the sidebar to navigate between pages.")

st.title("Welcome to the Interactive Data App!")
st.markdown(
    """
    - **EDA**: Perform exploratory data analysis.
    - **Handle Missing Values**: Apply methods to manage missing data.
    - **Visualizations**: Create interactive charts.
    """
)

st.image(
    "https://via.placeholder.com/800x300.png?text=Data+Visualization+App",
    caption="Analyze, preprocess, and visualize your data.",
)
