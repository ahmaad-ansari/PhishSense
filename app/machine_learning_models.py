# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.metrics import confusion_matrix

# Define global variables for x_train and y_train
x_train_global = None
y_train_global = None

# Function to load data from a CSV file
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Shuffle the DataFrame
    df = df.sample(frac=1)
    return df

# Function to preprocess the loaded data
def preprocess_data(df):
    # Dropping the 'url' column
    df = df.drop('url', axis=1)
    # Dropping duplicate rows
    df = df.drop_duplicates()
    X = df.drop('type', axis=1)
    Y = df['type']
    # Standardizing the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, Y

# Function to train a Support Vector Machine model
def train_svm_model():
    global x_train_global, y_train_global
    
    svm_model = svm.LinearSVC()
    svm_model.fit(x_train_global, y_train_global)
    return svm_model

# Function to train a Random Forest model
def train_rf_model():
    global x_train_global, y_train_global
    
    rf_model = RandomForestClassifier(n_estimators=60)
    rf_model.fit(x_train_global, y_train_global)
    return rf_model

# Function to create a Neural Network model
def create_nn_model(input_dim):
    model = Sequential([
        Dense(64, activation='relu', input_dim=input_dim),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Function to train a Neural Network model
def train_nn_model():
    global x_train_global, y_train_global
    
    input_dim = x_train_global.shape[1]
    nn_model = create_nn_model(input_dim)
    nn_model.fit(x_train_global, y_train_global, epochs=10, batch_size=32, verbose=0)
    return nn_model

# Function to evaluate the performance of a trained model
def evaluate_model(model, X_test, y_test):
    if isinstance(model, svm.LinearSVC) or isinstance(model, RandomForestClassifier):
        predictions = model.predict(X_test)
    else:
        predictions_prob = model.predict(X_test)
        predictions = (predictions_prob > 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true=y_test, y_pred=predictions).ravel()
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    return accuracy, precision, recall

# Function to generate a DataFrame of results for different models
def generate_df_results(file_path):
    global x_train_global, y_train_global  # Declare global variables

    df = load_data(file_path)
    X, Y = preprocess_data(df)
    x_train_global, x_test, y_train_global, y_test = train_test_split(X, Y, test_size=0.2, random_state=10)
    
    # Train models
    svm_model = train_svm_model()
    rf_model = train_rf_model()
    nn_model = train_nn_model()

    models = [svm_model, rf_model, nn_model]
    model_names = ['Support Vector Machine', 'Random Forest', 'Neural Network']

    # DataFrame to store evaluation results
    results = pd.DataFrame(index=model_names, columns=['Accuracy', 'Precision', 'Recall'])

    # Evaluate each model
    for model, name in zip(models, model_names):
        accuracy, precision, recall = evaluate_model(model, x_test, y_test)
        results.loc[name] = [accuracy, precision, recall]

    return results
