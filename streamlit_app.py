import streamlit as st
from joblib import load
import sklearn
from groq import Groq
from plant_health import plant_health_page
from chatbot import chatbot_page

# Set page config
st.set_page_config(
    page_title="Plant Health Classification",
    page_icon="img/imges.jpg",
    layout="centered",
    initial_sidebar_state="expanded"
)



def main():
    page = st.sidebar.radio(
        "Select a Page", ("Plant Health Prediction", "Chatbot"))

    if page == "Plant Health Prediction":
        plant_health_page()
    elif page == "Chatbot":
        chatbot_page()

    st.sidebar.markdown("##### Data")
    
    # Create an empty container to hold the plant data in the sidebar
    plant_data_container = st.sidebar.empty()

    if "plant_data" in st.session_state:
        # Display the plant data within the container
        plant_data_container.write(st.session_state.plant_data)

        # Display the "Clear Data" button, and remove the plant data when clicked
        if st.sidebar.button("Clear Data"):
            del st.session_state.plant_data
            plant_data_container.empty()  # Clear the container where data was displayed
            # st.rerun()
    else:
        st.sidebar.error("Data haven't been chosen")


# Initialize the session state for the first time
if "page" not in st.session_state:
    st.session_state.page = "Plant Health Prediction"

if __name__ == "__main__":
    main()


# def main():

#     page = st.sidebar.radio(
#         "Select a Page", ("Plant Health Prediction", "Chatbot"))

#     if page == "Plant Health Prediction":
#         plant_health_page()
#     elif page == "Chatbot":
#         chatbot_page()

#     st.sidebar.markdown("##### Data")
#     if "plant_data" in st.session_state:
#         st.sidebar.write(st.session_state.plant_data)
        
#         if st.sidebar.button("Clear Data"):
#                 del st.session_state.plant_data
#                 plant_data_container.empty()
#     else:
#         st.sidebar.error("Data haven't choosen")
        