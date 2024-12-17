import streamlit as st

def app():
    st.title("Key Findings")
    st.write("### 1. AQI Trends and Variability")
    st.write("""
    - The AQI levels show significant variability across stations and over time (years and months).  
    - Some stations, like **Aotizhongxin**, exhibit higher AQI values compared to others, suggesting poorer air quality in those areas.  
    - Overall, there seems to be a **decreasing trend** in AQI from 2013 to 2017, indicating potential improvements in air quality over time, although more detailed analysis is needed to confirm this trend.
    """)

    st.write("### 2. Pollutant Contributions")
    st.write("""
    - The analysis reveals that **CO (Carbon Monoxide)** is the most dominant pollutant among **PM2.5, PM10, SO2, NO2, CO, and O3**.  
    - Different stations show varying levels of pollutants. For example, stations like **Guanyuan** and **Aotizhongxin** consistently rank high for PM2.5, PM10, and other pollutants.  
    - Visualizations (like the **sunburst charts**) help in identifying the stations and pollutants that require the most attention for air quality management.
    """)

    st.write("### 3. Seasonal Patterns")
    st.write("""
    - The monthly average plots indicate the presence of **seasonal patterns** in pollutant concentrations.  
    - Certain pollutants might show higher levels during specific months or seasons.  
    - These seasonal variations can be further investigated to identify contributing factors like **weather patterns**, **industrial activities**, and **seasonal changes in emissions**.
    """)

    st.write("### 4. Station-wise Pollutant Levels")
    st.write("""
    - By examining the **mean pollutant levels per station** (e.g., using the sunburst chart), we can identify specific stations with significantly higher concentrations of certain pollutants.  
    - This information can be used to **target air quality improvement efforts** in those particular areas.
    """)

    st.write("### 5. Relationship between Pollutants")
    st.write("""
    - Pairwise scatter plots highlight the **correlations** between different pollutants.  
    - For instance, there might be a **positive correlation** between **PM2.5** and **PM10**, indicating that they tend to increase or decrease together.  
    - Understanding these relationships can help in developing **more effective strategies** for controlling multiple pollutants simultaneously.
    """)

    st.write("### 6. Top Polluted Stations")
    st.write("""
    - The analysis identifies stations that consistently rank high for multiple pollutants.  
    - Stations like **Guanyuan**, **Aotizhongxin**, and **Dongsi** frequently appear among the **top polluted stations**.  
    - Prioritizing these locations for **air quality improvement initiatives** can have a significant impact on overall air quality in the region.
    """)

    st.write("### 7. Model Performance")
    st.write("""
    - **K-Nearest Neighbors** model was used for predictions and resulted in a **low RMSE value** for both train and test sets, demonstrating **reasonable prediction accuracy**.  
    - The **R-squared value** indicates that the selected pollutants can explain a substantial portion of the variation in AQI, supporting their usage as effective predictors.
    """)

    st.write("---")
    st.write("""
    These findings provide valuable insights into the air quality situation in Beijing and can guide decision-making for **environmental management** and **public health strategies**.  
    Continued monitoring and further research can help refine these findings and lead to even more effective solutions for improving air quality in the region.
    """)
    # Footer
    st.markdown(
        """
        ---
        **Created by [Bapti Niloy Sarkar](mailto:baptiniloy@gmail.com)**  
        """,
        unsafe_allow_html=True
    )