import streamlit as st
from joblib import load
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key="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")

# Ensure chat history is initialized in session_state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps users with their plants' health based on the given data."
        }
    ]

def chatbot_page():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("SímboloAI Chatbot")

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
            )
            
            

            # Access the response content correctly using dot notation
            response = chat_completion.choices[0].message.content

            # Display assistant message
            with st.chat_message("assistant"):
                st.markdown(response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Chatbot is not working: {e}")


            
        # if "plant_data" in st.session_state:
        #     plant_data = str(st.session_state.plant_data)
        #     user_message = st.text_input("Chat with the assistant", 
        #                                  "Predict the plant's health based on the provided data, and explain the steps to handle this situation effectively.")

        #     if st.button("Send"):
        #         chatbot_input = f"{user_message}\nPlant Data:\n{plant_data}"
        #         st.session_state.chat_history.append({"role": "user", "content": chatbot_input})

        #         chat_completion = client.chat.completions.create(
        #             messages=st.session_state.chat_history,
        #             model="llama3-8b-8192",
        #         )

        #         assistant_response = chat_completion.choices[0].message.content
        #         st.session_state.chat_history.append(
        #             {"role": "system", "content": assistant_response if assistant_response is not None else "No response received."}
        #         )
        #         st.write(assistant_response)

        # else:
        #     user_message = st.text_input("Chat with the assistant", "Hi, there!")
        #     if st.button("Send"):
        #         chatbot_input = f"{user_message}"
        #         st.session_state.chat_history.append({"role": "user", "content": chatbot_input})

        #         chat_completion = client.chat.completions.create(
        #             messages=st.session_state.chat_history,
        #             model="llama3-8b-8192",
        #         )

        #         assistant_response = chat_completion.choices[0].message.content
        #         st.session_state.chat_history.append(
        #             {"role": "system", "content": assistant_response if assistant_response is not None else "No response received."}
        #         )
        #         st.write(assistant_response)
