import streamlit as st
import pandas as pd
from sklearn.impute import KNNImputer

st.title("Handle Missing Values")

uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview")
    st.write(data.head())

    st.write("### Missing Values")
    missing_summary = data.isnull().sum()
    st.write(missing_summary[missing_summary > 0])

    st.write("### Choose a Method to Handle Missing Values")
    option = st.selectbox(
        "Choose an option",
        ["No Action", "Drop Rows", "Drop Columns", "Fill with Mean/Median/Mode", "KNN Imputation"],
    )

    if option == "Drop Rows":
        data = data.dropna()
        st.write("Rows with missing values dropped.")
    elif option == "Drop Columns":
        columns = st.multiselect("Select columns to drop", data.columns)
        if st.button("Drop Columns"):
            data = data.drop(columns=columns)
            st.write(f"Columns dropped: {columns}")
    elif option == "Fill with Mean/Median/Mode":
        method = st.radio("Select method", ["Mean", "Median", "Mode"])
        if st.button("Fill Missing Values"):
            for col in data.select_dtypes(include=["float", "int"]):
                if method == "Mean":
                    data[col].fillna(data[col].mean(), inplace=True)
                elif method == "Median":
                    data[col].fillna(data[col].median(), inplace=True)
                elif method == "Mode":
                    data[col].fillna(data[col].mode()[0], inplace=True)
            st.write(f"Filled missing values using {method}.")
    elif option == "KNN Imputation":
        st.write("Applying KNN Imputation...")
        numeric_data = data.select_dtypes(include=["float", "int"])
        non_numeric_data = data.select_dtypes(exclude=["float", "int"])

        imputer = KNNImputer(n_neighbors=5)
        imputed_data = pd.DataFrame(imputer.fit_transform(numeric_data), columns=numeric_data.columns)
        data = pd.concat([imputed_data, non_numeric_data], axis=1)
        st.write("KNN Imputation applied.")

    st.write("### Updated Missing Values")
    st.write(data.isnull().sum())
