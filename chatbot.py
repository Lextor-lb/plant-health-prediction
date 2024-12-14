import streamlit as st
from joblib import load
from groq import Groq
import time
# Initialize the Groq client
client = Groq(
    api_key="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"
)

def chatbot_page():
    
        
    # Ensure chat history and messages are initialized in session_state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "system",
                "content": """You are an AI assistant that helps users with their plants' health based on the given data.      
                        Soil_Moisture (%): Measures the water content in soil, crucial for maintaining adequate hydration levels.
                        Ambient_Temperature (°C): Ambient temperature around the plant.
                        Soil_Temperature (°C): Soil temperature near plant roots.
                        Humidity (%): Air humidity level, which affects plant transpiration and growth.
                        Light_Intensity (Lux): Measures light exposure, essential for photosynthesis.
                        Soil_pH: Indicates the acidity or alkalinity of the soil, affecting nutrient availability.
                        Nitrogen_Level (mg/kg): Key nutrient supporting plant growth and leaf development.
                        Phosphorus_Level (mg/kg): Nutrient important for root and flower development.
                        Potassium_Level (mg/kg): Nutrient aiding in overall plant resilience and disease resistance.
                        Chlorophyll_Content (mg/m²): Chlorophyll concentration reflects photosynthetic activity and plant health.
                        Electrochemical_Signal (mV): Represents stress signals detected in plants, often due to environmental changes or internal stress responses.
                        Plant_Health_Status: Categorical label indicating the overall health of the plant, based on soil moisture and nutrient levels. It has three possible values:"""
            }
        ]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    
    
    st.title("HelioBot")

    try:
        with st.expander("❗Disclaimer"):
            st.markdown(
                "* The predictions and recommendations provided by this chatbot are generated using an AI model and may not always be accurate or comprehensive.\n"
                "* This chatbot is for informational and educational purposes only and should not replace professional advice for plant health management.\n"
                "* Always consult a qualified expert for critical plant health concerns or emergencies."
            )

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("What is up?"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Prepare prompt for the assistant
            if "plant_data" in st.session_state:
                plant_data = str(st.session_state.plant_data)
                prompt = f"{prompt}\nPlant Data:\n{plant_data}"

            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            
            # Generate response from the model
            chat_completion = client.chat.completions.create(
                messages=st.session_state.chat_history,
                model="llama3-8b-8192",
                # stop="",
                stream=True,
            )
            
            with st.chat_message("assistant"):
                # Placeholder for streaming content
                response_container = st.empty()
                response_text = ""  
                
                # Stream and update content dynamically
                for chunk in chat_completion:
                    streamed_text = chunk.choices[0].delta.content or " "
                    response_text += streamed_text
                    response_container.markdown(response_text) 
                    print(chunk.choices[0].delta.content)
                    time.sleep(0.05)              

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})

    except Exception as e:
        st.error(f"Chatbot is not working: {e}")
