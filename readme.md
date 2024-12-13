# SímboloAI: Plant Health Prediction & Chatbot

SímboloAI is a Streamlit-based application that integrates plant health prediction and a chatbot to assist users with plant health management. The application provides AI-driven insights into plant health data and offers a chatbot interface for interactive support.

---

## Features

### 1. **Plant Health Prediction**
- Predicts plant health using a trained Random Forest model.
- Provides an easy-to-use interface for entering plant data manually.
- Predefined data templates for Healthy, Unhealthy, and Critical conditions.

### 2. **Interactive Chatbot**
- AI-driven chatbot for plant health support.
- Users can save plant data from the prediction page and use it for more accurate chatbot recommendations.
- Powered by Groq's AI model.

---

## Requirements

- Python 3.8+
- Streamlit
- Scikit-learn
- Joblib
- Groq API

Install dependencies using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Installation & Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Lextor-lb/plant-health-prediction
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Place the trained Random Forest model (`random_forest_model.joblib`) in the root directory.

4. Update the Groq API key in the `chatbot_page` function:

   ```python
   client = Groq(
       api_key="your_api_key_here"
   )
   ```

5. Run the application:

   ```bash
   streamlit run app.py
   ```

---

## File Structure

```
.
├── app.py                # Main application entry point
├── chatbot.py            # Chatbot implementation
├── plant_health.py       # Plant health prediction functionality
├── random_forest_model.joblib  # Trained model (add this file manually)
├── requirements.txt      # Required Python packages
└── predefined_classes.py # Predefined plant data templates
```

---

## Usage

### **1. Plant Health Prediction Page**

1. Select **Plant Health Prediction** from the sidebar.
2. Use the predefined buttons to populate initial plant data:
   - Healthy
   - Unhealthy
   - Critical
3. Adjust sliders for each plant parameter as needed.
4. Save the data to use it in the chatbot or predict plant health directly.
5. Press the **Predict Plant Health** button to get predictions based on the input data.

### **2. Chatbot Page**

1. Select **Chatbot** from the sidebar.
2. View the disclaimer for model usage.
3. Interact with the chatbot by typing your queries in the input field.
4. If plant data is saved, the chatbot incorporates it into its responses.

---

## Parameters for Plant Data

| Parameter              | Range      | Unit        |
|------------------------|------------|-------------|
| Soil Moisture          | 0 - 100    | %           |
| Ambient Temperature    | 0.0 - 60.0 | °C          |
| Soil Temperature       | 0.0 - 60.0 | °C          |
| Humidity               | 0 - 100    | %           |
| Light Intensity        | 0 - 10,000 | lux         |
| Soil pH                | 0.0 - 14.0 | pH           |
| Nitrogen Level         | 0 - 300    | ppm         |
| Phosphorus Level       | 0 - 300    | ppm         |
| Potassium Level        | 0 - 300    | ppm         |
| Chlorophyll Content    | 0.0 - 200.0| µg/g        |
| Electrochemical Signal | 0.0 - 100.0| mA/s        |

---

## Disclaimer

The predictions and recommendations provided by this application are generated using AI models and may not always be accurate or comprehensive. Always consult a qualified expert for critical plant health concerns or emergencies.

## Acknowledgments

- **Streamlit** for the interactive web app framework.
- **Groq API** for AI chatbot capabilities.
- **Scikit-learn** for machine learning model development.

---

