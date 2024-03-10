# PhishSense

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

   Execute the main script (`main.py`) with the input CSV file and desired output file for extracted features:

   ```bash
   python main.py --input your_csv_file.csv --output extracted_features.csv
   ```

   This will read the CSV, extract features from each URL, and save the results to a new CSV file (`extracted_features.csv`).

### 3. Output

The system generates a CSV file (`extracted_features.csv`) containing the extracted features for each URL, including the URL itself, title, number of links, and the type of the website (legitimate or phishing). This file can be used as a labeled dataset for training machine learning models.

## Notes

- Ensure that the URLs in the input CSV file are accessible, as the system makes web requests to extract features.
- The machine learning model training part is not included in this system. You can use the generated `extracted_features.csv` file to train your own machine learning model for phishing detection.