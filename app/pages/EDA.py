import streamlit as st
import pandas as pd
import io

st.title("Exploratory Data Analysis")

uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview")
    st.write(data.head())

    st.write("### Dataset Information")
    buffer = io.StringIO()
    data.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)

    st.write("### Missing Values")
    missing_summary = data.isnull().sum()
    st.write(missing_summary[missing_summary > 0])

    if st.checkbox("Show Summary Statistics"):
        st.write(data.describe())
