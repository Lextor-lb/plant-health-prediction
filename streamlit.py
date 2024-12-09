import streamlit as st
from joblib import load
import sklearn
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key="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")

# Initialize the chat history list
st.session_state.chat_history = [
    {  # Initial message (optional)
        "role": "system",
        "content":
        ("You are an Ai assistant that help user for their plants to get healthy based on their given data ")
    },
]


# Set page config
st.set_page_config(
    page_title = "Plant Health Classificatin",
    page_icon = "img/imges.jpg",
    layout="centered", 
    initial_sidebar_state="expanded"
)

# Define the plant health classes
label_classes = ['Healthy', 'High Stress', 'Moderate Stress']

# Load the trained random forest model
loaded_clf = load('random_forest_model.joblib')


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
    col1, col2, col3= st.columns(3)
    
    if col1.button("Healthy"):
        st.session_state.tmp_data = classes["Healthy"]
    if col2.button("Unhealthy"):
        st.session_state.tmp_data = classes["Unhealthy"]
    if col3.button("Critical"):
        st.session_state.tmp_data = classes["Critical"]

    # Default values or session state
    if "tmp_data" in st.session_state:
        plant_data = st.session_state.tmp_data
    else:
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
    
    if st.button("Save Data to chatbot"):
        st.session_state.plant_data = plant_data
        st.success("Data saved!!")
    
    # Button to predict plant health
    if st.button("Predict Plant Health"):
        
        try:
            prediction = label_classes[int(loaded_clf.predict([[x for x in plant_data.values()]])[0])]
                
            st.success("Prediction Successful!")
            st.write(f"Predicted Plant Health Classes: {prediction}")
        except:
            st.error("Error in prediction! Please check your inputs.")
   
def chatbot_page():
    
    if "tmp_data" in st.session_state:
        del st.session_state.tmp_data
        
    st.title("Chatbot")

    if "plant_data" in st.session_state:
       
        plant_data = str(st.session_state.plant_data)
        user_message = st.text_input("Chat with the assistant", "Use the plant data provided")
        
        if st.button("Clear Data"):
            del st.session_state.plant_data

        if st.button("Send"):
            # try:
                chatbot_input = f"{user_message}\nPlant Data:\n{plant_data}"
                st.session_state.chat_history.append({"role": "user", 
                                                      "content": chatbot_input})
                
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.chat_history,
                    model="llama3-8b-8192",
                )
                
                assistant_response = chat_completion.choices[0].message.content
                st.session_state.chat_history.append({"role":"system",
                                                      "content":assistant_response if assistant_response is not None else "No response received."
                                                      
                
                })
                st.write(assistant_response)
                
    else:
        user_message = st.text_input("Chat with the assistant", "Use the plant data provided")
        if st.button("Send"):
            # try:
                chatbot_input = f"{user_message}"
                st.session_state.chat_history.append({"role": "user", 
                                                      "content": chatbot_input})
                
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.chat_history,
                    model="llama3-8b-8192",
                )
                
                assistant_response = chat_completion.choices[0].message.content
                st.session_state.chat_history.append({"role":"system",
                                                      "content":assistant_response if assistant_response is not None else "No response received."
                                                      
                
                })
                st.write(assistant_response)

            
        
        

def main():
    
    page = st.sidebar.selectbox("Select a Page", ("Plant Health Prediction", "Chatbot"))

    if page == "Plant Health Prediction":
        plant_health_page()
    elif page == "Chatbot":
        chatbot_page()
    
    st.sidebar.markdown("##### Data")
    if "plant_data" in st.session_state:
        st.sidebar.write(st.session_state.plant_data)
    else:
        st.sidebar.error("Data haven't choosen")
    

# Initialize the session state for the first time
if "page" not in st.session_state:
    st.session_state.page = "Plant Health Prediction"

if __name__ == "__main__":
    main()

