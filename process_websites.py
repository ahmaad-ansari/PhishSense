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
        print(f"Error processing HTML content: {e}")
        return None

def process_csv(input_csv, output_csv, label):
    # Read the input CSV file
    df = pd.read_csv(input_csv, header=None, names=['id', 'url'])

    # Add 'https://www.' to each URL
    df['url'] = 'https://www.' + df['url'].astype(str)

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

