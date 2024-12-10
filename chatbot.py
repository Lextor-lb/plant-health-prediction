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



def chatbot_page():

    if "tmp_data" in st.session_state:
        del st.session_state.tmp_data

    st.title("SímboloAI Chatbot")

    try:

        if "plant_data" in st.session_state:

            plant_data = str(st.session_state.plant_data)
            user_message = st.text_input(
                "Chat with the assistant", "Predict the plant's health based on the provided data, and explain the steps to handle this situation effectively.")

            # if st.button("Clear Data"):
            #     del st.session_state.plant_data

            if st.button("Send"):

                chatbot_input = f"{user_message}\nPlant Data:\n{plant_data}"
                st.session_state.chat_history.append({"role": "user",
                                                      "content": chatbot_input})

                chat_completion = client.chat.completions.create(
                    messages=st.session_state.chat_history,
                    model="llama3-8b-8192",
                )

                assistant_response = chat_completion.choices[0].message.content
                st.session_state.chat_history.append(
                    {"role": "system", "content": assistant_response if assistant_response is not None else "No response received."})
                st.write(assistant_response)

        else:
            user_message = st.text_input(
                "Chat with the assistant", "Hi, there!")
            if st.button("Send"):
                # try:
                chatbot_input = f"{user_message}"
                st.session_state.chat_history.append(
                    {"role": "user", "content": chatbot_input})

                chat_completion = client.chat.completions.create(
                    messages=st.session_state.chat_history,
                    model="llama3-8b-8192",
                )

                assistant_response = chat_completion.choices[0].message.content
                st.session_state.chat_history.append(
                    {"role": "system", "content": assistant_response if assistant_response is not None else "No response received."})
                st.write(assistant_response)

    except:
        st.error("Chatbot is not working")


