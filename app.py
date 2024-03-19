import streamlit as st
from phishing_detector import PhishingDetector
import joblib
from tensorflow.keras.models import load_model
import numpy as np

# Load the models
try:
    svm_model = joblib.load('models/svm_model.pkl')
    neural_network_model = load_model('models/neural_network_model.h5')
    random_forest_model = joblib.load('models/random_forest_model.pkl')
except Exception as e:
    st.error(f"Error: Failed to load the models. {str(e)}")

# Main function
def main():
    st.title("PhishSense - Phishing Website Detection")

    # Input URL
    url = st.text_input("Enter the URL:", "")

    # Dropdown for model choice
    model_choice = st.selectbox("Choose a Machine Learning Model:", ["Support Vector Machine", "Neural Network", "Random Forest"])

    # Feature extraction and prediction button
    if st.button("Extract Features and Predict"):
        if url:
            # Initialize PhishingDetector
            detector = PhishingDetector(svm_model, neural_network_model, random_forest_model)

            # Extract features
            features = detector.extract_features(url)

            # Check if features were successfully extracted
            if features is None:
                st.error(f"Error: The page at {url} is not accessible.")
                return

            # Remove the URL feature from the dictionary
            features.pop('url', None)
            features.pop('type', None)

            # Convert boolean values to integers (True to 1, False to 0)
            for key in features:
                if isinstance(features[key], bool):
                    features[key] = int(features[key])

            # Convert features to numpy array, replacing 'unknown' with NaN
            features_array = np.array([float(val) if val != 'unknown' else np.nan for val in features.values()])

            # Check for NaN values in the features array
            if np.isnan(features_array).any():
                problematic_indices = np.where(np.isnan(features_array))[0]
                problematic_features = [list(features.keys())[idx] for idx in problematic_indices]
                st.error(f"Error: Some feature values could not be converted to float. Problematic features: {problematic_features}")
                return

            # Reshape features array to 2D
            features_array = features_array.reshape(1, -1)

            # Predict using the chosen model
            result = detector.predict(features_array, model_choice)

            # Show the result
            st.write(f"Prediction result using {model_choice}: {result}")

# Execute the main function
if __name__ == "__main__":
    main()
