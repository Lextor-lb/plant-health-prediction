import streamlit as st
import requests

# URLs for the APIs
PLANT_API_URL = "https://1062c805-eea0-4753-8d98-17434c474000-00-2n4oyam338xuj.janeway.replit.dev/plant-health-prediction"
CHATBOT_API_URL = "https://1062c805-eea0-4753-8d98-17434c474000-00-2n4oyam338xuj.janeway.replit.dev/chatbot"

# Function to validate plant data ranges
def validate_plant_data(data):
    valid = True
    errors = []

    # Define valid ranges for each input
    if not (0 <= data["Soil_Moisture"] <= 100):
        valid = False
        errors.append("Soil Moisture should be between 0 and 100%.")

    if not (0.0 <= data["Ambient_Temperature"] <= 60.0):
        valid = False
        errors.append("Ambient Temperature should be between 0 and 60°C.")

    if not (0.0 <= data["Soil_Temperature"] <= 60.0):
        valid = False
        errors.append("Soil Temperature should be between 0 and 60°C.")

    if not (0 <= data["Humidity"] <= 100):
        valid = False
        errors.append("Humidity should be between 0 and 100%.")

    if not (0 <= data["Light_Intensity"] <= 10000):
        valid = False
        errors.append("Light Intensity should be between 0 and 10,000 lux.")

    if not (0.0 <= data["Soil_pH"] <= 14.0):
        valid = False
        errors.append("Soil pH should be between 0 and 14.")

    if not (0 <= data["Nitrogen_Level"] <= 300):
        valid = False
        errors.append("Nitrogen Level should be between 0 and 300 ppm.")

    if not (0 <= data["Phosphorus_Level"] <= 300):
        valid = False
        errors.append("Phosphorus Level should be between 0 and 300 ppm.")

    if not (0 <= data["Potassium_Level"] <= 300):
        valid = False
        errors.append("Potassium Level should be between 0 and 300 ppm.")

    if not (0.0 <= data["Chlorophyll_Content"] <= 200.0):
        valid = False
        errors.append("Chlorophyll Content should be between 0 and 200 µg/g.")

    if not (0.0 <= data["Electrochemical_Signal"] <= 100.0):
        valid = False
        errors.append("Electrochemical Signal should be between 0 and 100 mA/s.")

    return valid, errors

# Function for Plant Health Prediction Page
def plant_health_page():
    st.title("Plant Health Prediction")

    # Predefined classes
    classes = {
        "Healthy": {
            "Soil_Moisture": 40,
            "Ambient_Temperature": 25.0,
            "Soil_Temperature": 20.0,
            "Humidity": 50,
            "Light_Intensity": 5000,
            "Soil_pH": 6.5,
            "Nitrogen_Level": 150,
            "Phosphorus_Level": 100,
            "Potassium_Level": 120,
            "Chlorophyll_Content": 50.0,
            "Electrochemical_Signal": 50.0,
        },
        "Unhealthy": {
            "Soil_Moisture": 20,
            "Ambient_Temperature": 35.0,
            "Soil_Temperature": 30.0,
            "Humidity": 20,
            "Light_Intensity": 2000,
            "Soil_pH": 4.5,
            "Nitrogen_Level": 50,
            "Phosphorus_Level": 30,
            "Potassium_Level": 40,
            "Chlorophyll_Content": 10.0,
            "Electrochemical_Signal": 10.0,
        },
        "Critical": {
            "Soil_Moisture": 5,
            "Ambient_Temperature": 50.0,
            "Soil_Temperature": 45.0,
            "Humidity": 5,
            "Light_Intensity": 500,
            "Soil_pH": 3.0,
            "Nitrogen_Level": 10,
            "Phosphorus_Level": 10,
            "Potassium_Level": 10,
            "Chlorophyll_Content": 5.0,
            "Electrochemical_Signal": 5.0,
        },
    }

    # Buttons to set input values
    st.write("Enter plant health data below:")
    col1, col2, col3 = st.columns(3)

    if col1.button("Healthy"):
        st.session_state.plant_data = classes["Healthy"]
    if col2.button("Unhealthy"):
        st.session_state.plant_data = classes["Unhealthy"]
    if col3.button("Critical"):
        st.session_state.plant_data = classes["Critical"]

    # Default values or session state
    plant_data = st.session_state.get("plant_data", classes["Healthy"])

    # Input fields for plant data
    soil_moisture = st.slider("Soil Moisture (%)", 0, 100, value=plant_data["Soil_Moisture"])
    ambient_temp = st.slider("Ambient Temperature (°C)", 0.0, 60.0, value=plant_data["Ambient_Temperature"])
    soil_temp = st.slider("Soil Temperature (°C)", 0.0, 60.0, value=plant_data["Soil_Temperature"])
    humidity = st.slider("Humidity (%)", 0, 100, value=plant_data["Humidity"])
    light_intensity = st.slider("Light Intensity (lux)", 0, 10000, value=plant_data["Light_Intensity"])
    soil_ph = st.slider("Soil pH", 0.0, 14.0, value=plant_data["Soil_pH"])
    nitrogen_level = st.slider("Nitrogen Level (ppm)", 0, 300, value=plant_data["Nitrogen_Level"])
    phosphorus_level = st.slider("Phosphorus Level (ppm)", 0, 300, value=plant_data["Phosphorus_Level"])
    potassium_level = st.slider("Potassium Level (ppm)", 0, 300, value=plant_data["Potassium_Level"])
    chlorophyll_content = st.slider("Chlorophyll Content (µg/g)", 0.0, 200.0, value=plant_data["Chlorophyll_Content"])
    electrochemical_signal = st.slider("Electrochemical Signal (mA/s)", 0.0, 100.0, value=plant_data["Electrochemical_Signal"])

    # Collect data into a dictionary
    plant_data = {
        "Soil_Moisture": soil_moisture,
        "Ambient_Temperature": ambient_temp,
        "Soil_Temperature": soil_temp,
        "Humidity": humidity,
        "Light_Intensity": light_intensity,
        "Soil_pH": soil_ph,
        "Nitrogen_Level": nitrogen_level,
        "Phosphorus_Level": phosphorus_level,
        "Potassium_Level": potassium_level,
        "Chlorophyll_Content": chlorophyll_content,
        "Electrochemical_Signal": electrochemical_signal,
    }

    # Validate plant data
    valid, errors = validate_plant_data(plant_data)

    # Show error messages if validation fails
    if not valid:
        for error in errors:
            st.error(error)
        return

    # Button to predict plant health
    if st.button("Predict Plant Health"):
        response = requests.post(PLANT_API_URL, json={"data": [plant_data]})
        if response.status_code == 200:
            predictions = response.json()
            st.success("Prediction Successful!")
            st.write("Predicted Plant Health Classes:")
            for idx, prediction in enumerate(predictions.get("predictions", []), start=1):
                st.write(f"Plant {idx}: {prediction}")
        else:
            st.error("Error in prediction! Please check your inputs.")

# Main function to manage navigation between pages
def main():
    page = st.sidebar.radio("Select a Page", ("Plant Health Prediction", "Chatbot"))

    if page == "Plant Health Prediction":
        plant_health_page()

# Initialize the session state for the first time
if "page" not in st.session_state:
    st.session_state.page = "Plant Health Prediction"

if __name__ == "__main__":
    main()
