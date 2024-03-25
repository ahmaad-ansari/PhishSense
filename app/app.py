import streamlit as st
import pandas as pd
import machine_learning_models as ml
import extract_features as ef
from bs4 import BeautifulSoup
import requests as re
import warnings

# Suppressing warnings for better presentation
warnings.filterwarnings("ignore")

# Set page title and favicon
st.set_page_config(page_title="PhishSense", page_icon="🔍")

# Set page header
st.title('PhishSense')

# Introduction section with different styling
st.markdown("""
    **Content-Based Phishing Detection Using Machine Learning**

    PhishSense is a tool designed to identify potential phishing websites using machine learning algorithms.
    Unlike traditional URL-based approaches, PhishSense analyzes the content of web pages to assess their legitimacy.
""")


# Project details section with different styling
with st.expander("Machine Learning Model Results", expanded=True):
    st.info("Below are the results of the selected machine learning model:")
    st.table(ml.generate_df_results("../data/extracted_features.csv"))

# Machine learning model selection
st.sidebar.subheader("Machine Learning Model")
choice = st.sidebar.selectbox("Select Model", ['Support Vector Machine', 'Random Forest', 'Neural Network'])

model = None

if choice == 'Support Vector Machine':
    model = ml.train_svm_model()  # Call the function to train SVM model
    st.sidebar.write('SVM model is selected!')
elif choice == 'Random Forest':
    model = ml.train_rf_model()  # Call the function to train RF model
    st.sidebar.write('RF model is selected!')
else:
    model = ml.train_nn_model()  # Call the function to train NN model
    st.sidebar.write('NN model is selected!')

st.sidebar.subheader("URL Check")
url = st.sidebar.text_input('Enter the URL')
# check the url is valid or not
if st.sidebar.button('Check!'):
    if url:
        try:
            response = re.get(url, verify=False, timeout=4)  # Removed verify=False for better security
            response.raise_for_status()  # Raise an exception for non-200 status codes

            if response.status_code != 200:
                st.error(f"HTTP connection was not successful for the URL: {url}")
            else:
                features = ef.extract_features_from_html(response.text, url, "unknown")  # Assuming you don't know the website type beforehand

                # Convert features to numeric format, excluding the URL and website type
                numeric_features = {}
                for key, value in features.items():
                    if key not in ['url', 'type']:
                        try:
                            numeric_features[key] = float(value)
                        except ValueError:
                            # If value cannot be converted to float, exclude it from numeric conversion
                            pass


                vector = [list(numeric_features.values())]  # Convert the dictionary to a list of values
                
                # Predict using the selected model
                result = model.predict(vector)

                if result[0] == 0:
                    st.sidebar.success("This web page seems legitimate!")
                    st.sidebar.balloons()
                else:
                    st.sidebar.warning("Attention! This web page is a potential phishing site!")
                    st.sidebar.error("Do not enter sensitive information.")
        except Exception as e:
            st.sidebar.error("Error occurred while trying to access the URL. Please check the URL and try again.")
    else:
        st.sidebar.warning("Please enter a URL.")

st.sidebar.markdown("---")
st.sidebar.markdown("**SOFE4840U**")



