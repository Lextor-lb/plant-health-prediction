import streamlit as st
from joblib import load
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key="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")

st.session_state.chat_history = [
{
    "role": "system",
    "content": "You are an AI assistant that helps users with their plants' health based on the given data."
}
]



def chatbot_page():
   

    # Ensure chat_history is initialized in session_state if not already present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "system",
                "content": "You are an AI assistant that helps users with their plants' health based on the given data."
            }
        ]
    
    
    if "tmp_data" in st.session_state:
        del st.session_state.tmp_data

    st.title("SímboloAI Chatbot")

    try:
        if "plant_data" in st.session_state:
            plant_data = str(st.session_state.plant_data)
            user_message = st.text_input("Chat with the assistant", 
                                         "Predict the plant's health based on the provided data, and explain the steps to handle this situation effectively.")

            if st.button("Send"):
                chatbot_input = f"{user_message}\nPlant Data:\n{plant_data}"
                st.session_state.chat_history.append({"role": "user", "content": chatbot_input})

                chat_completion = client.chat.completions.create(
                    messages=st.session_state.chat_history,
                    model="llama3-8b-8192",
                )

                assistant_response = chat_completion.choices[0].message.content
                st.session_state.chat_history.append(
                    {"role": "system", "content": assistant_response if assistant_response is not None else "No response received."}
                )
                st.write(assistant_response)

        else:
            user_message = st.text_input("Chat with the assistant", "Hi, there!")
            if st.button("Send"):
                chatbot_input = f"{user_message}"
                st.session_state.chat_history.append({"role": "user", "content": chatbot_input})

                chat_completion = client.chat.completions.create(
                    messages=st.session_state.chat_history,
                    model="llama3-8b-8192",
                )

                assistant_response = chat_completion.choices[0].message.content
                st.session_state.chat_history.append(
                    {"role": "system", "content": assistant_response if assistant_response is not None else "No response received."}
                )
                st.write(assistant_response)

    except Exception as e:
        st.error(f"Chatbot is not working: {e}")
