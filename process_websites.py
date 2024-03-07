"""
Feature Extraction Script

This script extracts features from HTML content specified in a CSV file and saves the results to another CSV file.

Usage:
  python script_name.py input_csv output_csv label

Arguments:
  - input_csv: Path to the input CSV file containing 'id' and 'url' columns.
  - output_csv: Path to the output CSV file where features will be saved.
  - label: Integer label (0 for legitimate, 1 for phishing) to be associated with the extracted features.

The script performs the following steps:
  1. Reads the input CSV file containing 'id' and 'url' columns.
  2. Adds 'https://' to each URL in the dataframe.
  3. Instantiates the WebScraper class and HTMLFeatureExtractor class.
  4. Iterates through each row in the dataframe, scrapes HTML content, and extracts features.
  5. Creates a dataframe from the extracted features.
  6. Saves the dataframe to the output CSV file.
  7. Prints a message indicating the successful extraction and saving of features.

Author: Ahmaad Ansari
Date: March 5, 2024
"""


import pandas as pd
from web_scraper import WebScraper
from html_feature_extractor import HTMLFeatureExtractor

def extract_features(html_content, label):
    
    try:
        # Instantiate the HTMLFeatureExtractor class
        html_feature_extractor = HTMLFeatureExtractor(html_content)

        # Extract binary features
        html_feature_extractor.extract_binary_features()

        # Extract quantitative features
        html_feature_extractor.extract_quantitative_features()

        # Extract heuristic features
        html_feature_extractor.extract_heuristic_features()

        # Create a dictionary with features and labels
        features = html_feature_extractor.features.copy()
        features['label'] = label

        return features
    except Exception as e:
        # Print an error message if feature extraction fails
        print(f"Error processing HTML content: {e}")
        return None

def process_csv(input_csv, output_csv, label):

    # Read the input CSV file
    df = pd.read_csv(input_csv, header=None, names=['id', 'url'])

    # Add 'https://' to each URL
    df['url'] = 'https://' + df['url'].astype(str)

    # Create an empty list to store the extracted features
    features_list = []

    # Instantiate the WebScraper class
    web_scraper = WebScraper()

    # Process each row in the dataframe
    for _, row in df.iterrows():
        url = row['url']
        html_content = web_scraper.scrape_html(url)

        if html_content:
            features = extract_features(html_content, label)

            if features:
                features['url'] = url
                features_list.append(features)

    # Create a dataframe from the list of features
    output_df = pd.DataFrame(features_list)

    # Save the dataframe to the output CSV file
    output_df.to_csv(output_csv, index=False)
    print(f"Features extracted and saved to {output_csv}")

if __name__ == "__main__":
    import sys

    # Ensure the correct number of command-line arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python script_name.py input_csv output_csv label")
        sys.exit(1)

    # Extract command-line arguments
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    label = int(sys.argv[3])  # Assuming label is an integer (0 for legitimate, 1 for phishing)

    # Process the CSV files and extract features
    process_csv(input_csv, output_csv, label)
