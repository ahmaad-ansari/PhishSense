"""
Feature Extraction Main Script

This script serves as the main entry point for the PhishSense feature extraction system.
It utilizes argparse to handle command-line arguments for input and output file paths.
The script reads a CSV file containing URLs and their types, extracts features from each URL,
and saves the results to another CSV file. The extraction process involves two steps: reading the
CSV file and then extracting features from the URLs. The resulting CSV file can be used as a labeled
dataset for training machine learning models.

Usage:
  python main.py --input input_csv_file.csv --output output_features_csv_file.csv

Arguments:
  --input (-i): Path to the input CSV file containing URLs and types.
  --output (-o): Path to the output CSV file where features will be saved.

The script performs the following steps:
  1. Parses command-line arguments using argparse.
  2. Reads the input CSV file and extracts URLs with their corresponding types.
  3. Utilizes the 'read_csv' and 'process_urls' functions from the 'read_csv' and 'extract_features' modules.
  4. Saves the extracted features to the specified output CSV file.

Author: Ahmaad Ansari
Date: March 10, 2024
"""

import argparse
import pandas as pd
from read_csv import read_csv
from extract_features import process_urls

def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract features from URLs in a CSV file.')
    parser.add_argument('--input', '-i', required=True, help='Input CSV file with URLs and types')
    parser.add_argument('--output', '-o', required=True, help='Output CSV file for extracted features')
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_arguments()

    # Step 1: Read CSV and get URLs with types
    urls_and_types = read_csv(args.input)

    # Step 2: Extract features and save to CSV
    process_urls(urls_and_types, args.output)
