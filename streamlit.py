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
    if "plant_data" in st.session_state:
        st.sidebar.write(st.session_state.plant_data)
    else:
        st.sidebar.error("Data haven't choosen")


# Initialize the session state for the first time
if "page" not in st.session_state:
    st.session_state.page = "Plant Health Prediction"

if __name__ == "__main__":
    main()
