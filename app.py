import streamlit as st
from phishing_detector import PhishingDetector
import joblib
from tensorflow.keras.models import load_model
import numpy as np

# Function to load models with error handling
def load_models():
    try:
        svm_model = joblib.load('models/svm_model.pkl')
        neural_network_model = load_model('models/neural_network_model.h5')
        random_forest_model = joblib.load('models/random_forest_model.pkl')
        return svm_model, neural_network_model, random_forest_model
    except Exception as e:
        st.error(f"Error: Failed to load the models. {str(e)}")
        return None, None, None

# Load the models
svm_model, neural_network_model, random_forest_model = load_models()

# Main function
def main():
    st.title("PhishSense")
    st.subheader("Content-Based Phishing Detection System Using Machine Learning")

    # Input URL
    url = st.text_input("Enter the URL:", "")

    # Dropdown for model choice
    model_choice = st.selectbox("Choose a Machine Learning Model:", ["Support Vector Machine", "Neural Network", "Random Forest"])

    # Feature extraction and prediction button
    if st.button("Extract Features and Predict"):
        if url:
            # Initialize PhishingDetector
            detector = PhishingDetector(svm_model, neural_network_model, random_forest_model)

            # Extract features with error handling
            try:
                features = detector.extract_features(url)
                if features is None:
                    st.error(f"Error: The page at {url} is not accessible.")
                    return
            except Exception as e:
                st.error(f"Error: Failed to extract features. {str(e)}")
                return

            # Remove the URL feature from the dictionary
            features.pop('url', None)
            features.pop('type', None)

            # Convert boolean values to integers (True to 1, False to 0)
            for key in features:
                if isinstance(features[key], bool):
                    features[key] = int(features[key])

            # Convert features to numpy array, replacing 'unknown' with NaN
            try:
                features_array = np.array([float(val) if val != 'unknown' else np.nan for val in features.values()])
            except Exception as e:
                st.error(f"Error: Failed to convert features to array. {str(e)}")
                return

            # Check for NaN values in the features array
            if np.isnan(features_array).any():
                problematic_indices = np.where(np.isnan(features_array))[0]
                problematic_features = [list(features.keys())[idx] for idx in problematic_indices]
                st.error(f"Error: Some feature values could not be converted to float. Problematic features: {problematic_features}")
                return

            # Reshape features array to 2D
            features_array = features_array.reshape(1, -1)

            # Predict using the chosen model
            try:
                result = detector.predict(features_array, model_choice)
                if result == 0:
                    st.success("The website appears to be legitimate.")
                else:
                    st.error("The website appears to be phishing.")
            except Exception as e:
                st.error(f"Error: Failed to make prediction. {str(e)}")

    # Copyright message
    st.write("""
    ---
    Copyright © 2024 PhishSense. All rights reserved.
    """)

# Execute the main function
if __name__ == "__main__":
    main()
