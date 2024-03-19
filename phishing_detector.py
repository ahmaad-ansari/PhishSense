import joblib
from extract_features import extract_features

class PhishingDetector:
    def __init__(self, svm_model, neural_network_model, random_forest_model):
        self.svm_model = svm_model
        self.neural_network_model = neural_network_model
        self.random_forest_model = random_forest_model

    def extract_features(self, url):
        return extract_features(url, website_type='unknown')

    def predict(self, features, model_choice):
        if model_choice == "Support Vector Machine":
            return self.svm_model.predict(features)
        elif model_choice == "Neural Network":
            return (self.neural_network_model.predict(features) > 0.5).astype("int32")
        elif model_choice == "Random Forest":
            return self.random_forest_model.predict(features)
