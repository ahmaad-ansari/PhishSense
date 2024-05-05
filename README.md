# PhishSense

## Table of Contents
- [Overview](#overview)
- [Usage](#usage)
  - [1. Installation](#1-installation)
  - [2. Running the System](#2-running-the-system)
  - [3. Output](#3-output)
- [Notes](#notes)
- [Machine Learning Description](#machine-learning-description)

## Overview

PhishSense is a system designed to extract features from URLs, classify them as either legitimate or phishing, and create a structured dataset for machine learning model training. The system consists of Python scripts that read a CSV file containing URLs and their corresponding types, then extracts features from each URL using web scraping techniques. The extracted features are saved to a CSV file, which can be used to train machine learning models for phishing detection.

## Usage

### 1. Installation

Make sure you have Python installed on your system. Additionally, install the required Python packages using the following command:

```bash
pip install -r requirements.txt
```

### 2. Running the System

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/PhishSense.git
   cd PhishSense
   ```

2. **Prepare the CSV File:**

   Create a CSV file (`your_csv_file.csv`) with columns 'url' and 'type', where 'type' indicates whether the URL is legitimate (0) or phishing (1).

   ```csv
   url,type
   http://example.com,0
   http://phishing.com,1
   ```

3. **Run the Main Script:**

   Execute the main script (`main.py`) with the input CSV file and desired output file for extracted features. Optionally, you can specify the start and end lines (inclusive) to read from the input CSV file:

   ```bash
   python main.py --input your_csv_file.csv --output extracted_features.csv --start-line 1 --end-line 100
   ```

   This will read the CSV, extract features from each URL, and save the results to a new CSV file (`extracted_features.csv`).

### 3. Output

The system generates a CSV file (`extracted_features.csv`) containing the extracted features for each URL, including the URL itself, title, number of links, and the type of the website (legitimate or phishing). This file can be used as a labeled dataset for training machine learning models.

## Demo

Watch this video to see PhishSense's interface and trained machine learning models in action.

https://github.com/ahmaad-ansari/PhishSense/assets/88805493/652d2ca0-24d2-4aa6-9ff7-651b7c3b65db


## Notes

- Ensure that the URLs in the input CSV file are accessible, as the system makes web requests to extract features.
- The machine learning model training part is not included in this system. You can use the generated `extracted_features.csv` file to train your own machine learning model for phishing detection.

## Machine Learning Description

The IPYNB file (`Machine Learning Models.ipynb`) contains code for training and evaluating machine learning models for phishing detection. The file includes the following sections:

1. **Setup**: Installation of necessary libraries and modules.
2. **Data Loading and Preprocessing**: Loading the dataset and preprocessing steps such as standard scaling.
3. **Data Visualization**: Visualizing the dataset using Principal Component Analysis (PCA).
4. **Support Vector Machine (SVM)**: Training, evaluation, and visualization of results for SVM model.
5. **Neural Networks**: Building, training, evaluation, and visualization of results for neural network model.
6. **Random Forest**: Training, evaluation, and visualization of results for random forest model.
