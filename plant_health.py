import streamlit as st
from joblib import load
import sklearn  
from predfined_classes import classes

# Define the plant health classes
label_classes = ['Healthy', 'High Stress', 'Moderate Stress']

# Load the trained random forest model
loaded_clf = load('random_forest_model.joblib')


def plant_health_page():
  # Buttons to set input values
    st.title("HelioAI Plant Health Prediction")
    st.write("Enter plant health data below:")

    # Create three columns for the buttons
    col1, col2, col3 = st.columns([1, 1.1, 1])  # Adjust ratios if needed

    # Place one button in each column
    with col1:
        if st.button("Healthy"):
            st.session_state.tmp_data = classes["Healthy"]

    with col2:
        if st.button("Unhealthy"):
            st.session_state.tmp_data = classes["Unhealthy"]

    with col3:
        if st.button("Critical"):
            st.session_state.tmp_data = classes["Critical"]

    # # Create button layout in a row
    # st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    # if st.button("Healthy", key="healthy"):
    #     st.session_state.tmp_data = classes["Healthy"]
    # if st.button("Unhealthy", key="unhealthy"):
    #     st.session_state.tmp_data = classes["Unhealthy"]
    # if st.button("Critical", key="critical"):
    #     st.session_state.tmp_data = classes["Critical"]
    # st.markdown('</div>', unsafe_allow_html=True)

    # Default values or session state
    if "tmp_data" in st.session_state:
        plant_data = st.session_state.tmp_data
    else:
        plant_data = st.session_state.get("plant_data", classes["Healthy"])

    # Input fields for plant data
    soil_moisture = st.slider("Soil Moisture (%)", 0,
                              100, value=plant_data["Soil_Moisture"])
    ambient_temp = st.slider("Ambient Temperature (°C)",
                             0.0, 60.0, value=plant_data["Ambient_Temperature"])
    soil_temp = st.slider("Soil Temperature (°C)", 0.0,
                          60.0, value=plant_data["Soil_Temperature"])
    humidity = st.slider("Humidity (%)", 0, 100, value=plant_data["Humidity"])
    light_intensity = st.slider(
        "Light Intensity (lux)", 0, 10000, value=plant_data["Light_Intensity"])
    soil_ph = st.slider("Soil pH", 0.0, 14.0, value=plant_data["Soil_pH"])
    nitrogen_level = st.slider(
        "Nitrogen Level (mg/kg)", 0, 300, value=plant_data["Nitrogen_Level"])
    phosphorus_level = st.slider(
        "Phosphorus Level (mg/kg)", 0, 300, value=plant_data["Phosphorus_Level"])
    potassium_level = st.slider(
        "Potassium Level (mg/kg)", 0, 300, value=plant_data["Potassium_Level"])
    chlorophyll_content = st.slider(
        "Chlorophyll Content (mg/m²)", 0.0, 200.0, value=plant_data["Chlorophyll_Content"])
    electrochemical_signal = st.slider(
        "Electrochemical Signal (mV)", 0.0, 100.0, value=plant_data["Electrochemical_Signal"])

    # Collect data into a dictionary
    # plant_data = {
    #     "Soil_Moisture": soil_moisture,
    #     "Ambient_Temperature": ambient_temp,
    #     "Soil_Temperature": soil_temp,
    #     "Humidity": humidity,
    #     "Light_Intensity": light_intensity,
    #     "Soil_pH": soil_ph,
    #     "Nitrogen_Level": nitrogen_level,
    #     "Phosphorus_Level": phosphorus_level,
    #     "Potassium_Level": potassium_level,
    #     "Chlorophyll_Content": chlorophyll_content,
    #     "Electrochemical_Signal": electrochemical_signal,
    # }
    
    plant_data_with_units = {
        "Soil_Moisture": f"{soil_moisture}%",
        "Ambient_Temperature": f"{ambient_temp}°C",
        "Soil_Temperature": f"{soil_temp}°C",
        "Humidity": f"{humidity}%",
        "Light_Intensity": f"{light_intensity} lux",
        "Soil_pH": f"{soil_ph} pH",
        "Nitrogen_Level": f"{nitrogen_level} mg/kg",
        "Phosphorus_Level": f"{phosphorus_level} mg/kg",
        "Potassium_Level": f"{potassium_level} mg/kg",
        "Chlorophyll_Content": f"{chlorophyll_content}mg/m²",
        "Electrochemical_Signal": f"{electrochemical_signal}mV",
    }

    if st.button("Save Data to chatbot"):
        st.session_state.plant_data = plant_data_with_units
        st.success("Data saved!!")

    # Button to predict plant health
    if st.button("Predict Plant Health"):

        try:
            prediction = label_classes[int(loaded_clf.predict(
                [[x for x in plant_data.values()]])[0])]

            st.success("Prediction Successful!")
            st.write(f"Predicted Plant Health Classes: {prediction}")
        except:
            st.error("Error in prediction! Please check your inputs.")
