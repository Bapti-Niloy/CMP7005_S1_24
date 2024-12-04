import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
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
    st.title("Train K-Nearest Neighbors (KNN) Model")
    st.write("Use KNN regression to predict Air Quality Index (AQI) with customizable parameters and real-time evaluation.")

    # Load and preprocess data
    df = st.session_state["data"]

    # Ensure necessary columns exist
    if not all(col in df.columns for col in ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]):
        st.error("The dataset must include key pollutant columns like PM2.5, PM10, SO2, NO2, CO, O3.")
        return

    # Perform AQI calculation
    with st.spinner("Calculating AQI..."):
        df = calculate_aqi(df)
    st.success("AQI calculated successfully!")

    # Feature and target selection
    st.sidebar.title("Feature and Target Selection")
    selected_features = st.sidebar.multiselect(
        "Select Features",
        options=df.columns.tolist(),
        default=["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]
    )
    target_variable = st.sidebar.selectbox(
        "Select Target Variable",
        options=df.columns.tolist(),
        index=df.columns.tolist().index("AQI") if "AQI" in df.columns else 0
    )

    if not selected_features or not target_variable:
        st.error("Please select at least one feature and a target variable.")
        return

    # Handle missing values and ensure alignment
    X = df[selected_features]
    y = df[target_variable]
    valid_rows = X.notna().all(axis=1) & y.notna()
    X = X[valid_rows]
    y = y[valid_rows]

    # Split data into training and testing sets
    st.sidebar.title("Data Split Settings")
    test_size = st.sidebar.slider("Test Size", 0.1, 0.5, 0.2, 0.05)
    random_state = st.sidebar.number_input("Random State (Optional)", min_value=0, max_value=1000, value=42, step=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Parameter grid for GridSearchCV
    st.sidebar.title("KNN Hyperparameters")
    n_neighbors_range = st.sidebar.slider("Number of Neighbors (k)", 1, 50, (1, 15))
    weights_options = st.sidebar.selectbox("Weights", ["uniform", "distance"])
    param_grid = {
        "n_neighbors": range(n_neighbors_range[0], n_neighbors_range[1] + 1),
        "weights": [weights_options]
    }

    # Train KNN with GridSearchCV
    st.subheader("Hyperparameter Tuning with GridSearchCV")
    with st.spinner("Training KNN model with GridSearchCV..."):
        gridsearch = GridSearchCV(KNeighborsRegressor(), param_grid, cv=5, scoring="neg_mean_squared_error")
        gridsearch.fit(X_train_scaled, y_train)
        best_params = gridsearch.best_params_

    st.write(f"**Best Parameters Found:** {best_params}")
    best_model = gridsearch.best_estimator_

    # Evaluate the model
    train_preds = best_model.predict(X_train_scaled)
    test_preds = best_model.predict(X_test_scaled)

    train_mse = mean_squared_error(y_train, train_preds)
    train_rmse = np.sqrt(train_mse)
    test_mse = mean_squared_error(y_test, test_preds)
    test_rmse = np.sqrt(test_mse)
    test_r2 = r2_score(y_test, test_preds)
    test_mae = mean_absolute_error(y_test, test_preds)

    st.subheader("Model Evaluation Metrics")
    st.write(f"**Train RMSE:** {train_rmse:.2f}")
    st.write(f"**Test RMSE:** {test_rmse:.2f}")
    st.write(f"**R-squared (Test):** {test_r2:.2f}")
    st.write(f"**Mean Absolute Error (Test):** {test_mae:.2f}")

    # RMSE vs. Number of Neighbors
    st.subheader("RMSE vs. Number of Neighbors")
    k_range = range(n_neighbors_range[0], n_neighbors_range[1] + 1)
    train_rmse_list = []
    test_rmse_list = []

    for k in k_range:
        knn = KNeighborsRegressor(n_neighbors=k, weights=weights_options)
        knn.fit(X_train_scaled, y_train)
        train_preds = knn.predict(X_train_scaled)
        test_preds = knn.predict(X_test_scaled)
        train_rmse_list.append(np.sqrt(mean_squared_error(y_train, train_preds)))
        test_rmse_list.append(np.sqrt(mean_squared_error(y_test, test_preds)))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(k_range, train_rmse_list, label="Train RMSE", marker="o")
    ax.plot(k_range, test_rmse_list, label="Test RMSE", marker="o")
    ax.set_xlabel("Number of Neighbors (k)")
    ax.set_ylabel("RMSE")
    ax.set_title("RMSE vs. Number of Neighbors")
    ax.legend()
    st.pyplot(fig)
