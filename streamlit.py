# from joblib import load
# from groq import Groq

# # Define the plant health classes
# classes = ['Healthy', 'High Stress', 'Moderate Stress']

# # Load the trained random forest model
# loaded_clf = load('random_forest_model.joblib')


# # Initialize the Groq client
# client = Groq(
#     api_key="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")

# # Initialize the chat history list
# chat_history = [
#     {  # Initial message (optional)
#         "role": "system",
#         "content":
#         ("You are an Ai assistant that help user for their plants to get healthy based on give"
#          "Ask the user to provide the following information: Soil Moisture, Ambient Temperature, "
#          "Soil Temperature, Humidity, Light Intensity, Soil pH, Nitrogen Level, Phosphorus Level, "
#          "Potassium Level, Chlorophyll Content, and Electrochemical Signal. "
#          "Once you have all the required inputs, generate a JSON payload to send for prediction."
#          )
#     },
# ]
import streamlit as st
from joblib import load
import sklearn

# Define the plant health classes
classes = ['Healthy', 'High Stress', 'Moderate Stress']

# Load the trained random forest model
loaded_clf = load('random_forest_model.joblib')
sample_data = [[
     27.521108772254976, 22.24024536256306, 21.90043535506952,
    55.29190389508887, 556.172805131218, 5.581954516265902, 10.003649716693408,
    45.80685202827101, 39.0761990273964, 35.703005710811865, 0.9414021464707312
]]

if st.button("Reset"):
    preditation = loaded_clf.predict(sample_data)
    st.write(classes[preditation[0]])
else:
    st.write("Goodbye")
    

