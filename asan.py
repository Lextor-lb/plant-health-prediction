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

    if not (0 <= data["Ambient_Temperature"] <= 60):  # Allow slightly higher temperature range
        valid = False
        errors.append("Ambient Temperature should be between 0 and 60°C.")

    if not (0 <= data["Soil_Temperature"] <= 60):  # Same for soil temperature
        valid = False
        errors.append("Soil Temperature should be between 0 and 60°C.")

    if not (0 <= data["Humidity"] <= 100):
        valid = False
        errors.append("Humidity should be between 0 and 100%.")

    if not (0 <= data["Light_Intensity"] <= 10000):  # Allow higher light intensity range
        valid = False
        errors.append("Light Intensity should be between 0 and 10,000 lux.")

    if not (0 <= data["Soil_pH"] <= 14):
        valid = False
        errors.append("Soil pH should be between 0 and 14.")

    if not (0 <= data["Nitrogen_Level"] <= 300):  # Increased range for Nitrogen Level
        valid = False
        errors.append("Nitrogen Level should be between 0 and 300 ppm.")

    if not (0 <= data["Phosphorus_Level"] <= 300):  # Increased range for Phosphorus Level
        valid = False
        errors.append("Phosphorus Level should be between 0 and 300 ppm.")

    if not (0 <= data["Potassium_Level"] <= 300):  # Increased range for Potassium Level
        valid = False
        errors.append("Potassium Level should be between 0 and 300 ppm.")

    if not (0 <= data["Chlorophyll_Content"] <= 200):  # Increased range for Chlorophyll Content
        valid = False
        errors.append("Chlorophyll Content should be between 0 and 200 µg/g.")

    if not (0 <= data["Electrochemical_Signal"] <= 100):  # Increased range for Electrochemical Signal
        valid = False
        errors.append("Electrochemical Signal should be between 0 and 100 mA/s.")
    
    return valid, errors

# Function for Plant Health Prediction Page
def plant_health_page():
    st.title("Plant Health Prediction")

    # Input fields for plant data
    st.write("Enter plant health data below:")
    soil_moisture = st.number_input("Soil Moisture (%)", value=10)
    ambient_temp = st.number_input("Ambient Temperature (°C)", value=10.0)
    soil_temp = st.number_input("Soil Temperature (°C)", value=10.0)
    humidity = st.number_input("Humidity (%)", value=10.0)
    light_intensity = st.number_input("Light Intensity (lux)", value=10)
    soil_ph = st.number_input("Soil pH", value=10.0)
    nitrogen_level = st.number_input("Nitrogen Level (ppm)", value=10)
    phosphorus_level = st.number_input("Phosphorus Level (ppm)", value=10)
    potassium_level = st.number_input("Potassium Level (ppm)", value=10)
    chlorophyll_content = st.number_input("Chlorophyll Content (µg/g)", value=10.0)
    electrochemical_signal = st.number_input("Electrochemical Signal (mA/s)", value=10.0)

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

    # Button to navigate to chatbot page
    if st.button("Go to Chatbot with this Data"):
        st.session_state.chat_data = plant_data  # Store the data for chatbot use
        st.session_state.page = "Chatbot"  # Change page state to "Chatbot"
        # Remove st.experimental_set_query_params, and use session state
        st.session_state.page = "Chatbot"  # Navigate to the Chatbot page directly

# Function for Chatbot Page
def chatbot_page():
    st.title("Chatbot")

    if "chat_data" in st.session_state:
        user_message = st.text_input("Chat with the assistant", "Use the plant data provided")
        plant_data = st.session_state.chat_data

        if st.button("Send"):
            # Format message for chatbot
            formatted_data = "\n".join([f"{key}: {value}" for key, value in plant_data.items()])
            chatbot_input = f"{user_message}\nPlant Data:\n{formatted_data}"

            # Query chatbot API
            response = requests.post(CHATBOT_API_URL, json={"message": chatbot_input})
            if response.status_code == 200:
                chatbot_response = response.json().get("response", "No response received.")
                st.write("Chatbot Response:")
                st.write(chatbot_response)
            else:
                st.error("Error querying chatbot!")
    else:
        st.write("No plant data provided. Please go to the Plant Health Prediction page first.")

# Main function to manage navigation between pages
def main():
    # Define the pages for navigation
    page = st.radio("Select a Page", ("Plant Health Prediction", "Chatbot"))

    if page == "Plant Health Prediction":
        plant_health_page()
    elif page == "Chatbot":
        chatbot_page()

# Initialize the session state for the first time
if "page" not in st.session_state:
    st.session_state.page = "Plant Health Prediction"

# Run the app
if __name__ == "__main__":
    main()
