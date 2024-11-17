import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Interactive Visualizations")

uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    numeric_columns = data.select_dtypes(include=["float", "int"]).columns
    if len(numeric_columns) > 0:
        st.write("### Create a Chart")
        x_axis = st.selectbox("Choose X-axis", options=numeric_columns)
        y_axis = st.selectbox("Choose Y-axis", options=numeric_columns)
        chart_type = st.selectbox("Choose Chart Type", ["Scatter", "Line", "Bar"])

        if chart_type == "Scatter":
            fig = px.scatter(data, x=x_axis, y=y_axis)
        elif chart_type == "Line":
            fig = px.line(data, x=x_axis, y=y_axis)
        elif chart_type == "Bar":
            fig = px.bar(data, x=x_axis, y=y_axis)

        st.plotly_chart(fig)
    else:
        st.write("No numeric columns available for visualization.")
