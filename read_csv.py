"""
CSV Reading Function

This script provides a function to read a CSV file into a Pandas DataFrame, extracting specific columns.
The 'read_csv' function takes the file path as input, reads the CSV file, and returns a list of dictionaries
containing 'url' and 'type' pairs. This function is commonly used in PhishSense to read input CSV files
containing information about URLs and their corresponding types (legitimate or phishing).

Usage:
  from read_csv import read_csv
  url_type_list = read_csv('your_csv_file.csv')

Arguments:
  - file_path: Path to the input CSV file containing 'url' and 'type' columns.

The 'read_csv' function performs the following steps:
  1. Reads the CSV file into a Pandas DataFrame.
  2. Extracts the 'url' and 'type' columns from the DataFrame.
  3. Converts the DataFrame to a list of dictionaries.

Author: Ahmaad Ansari
Date: March 10, 2024
"""

import pandas as pd

def read_csv(file_path, start_line=0, end_line=None):
  # Read CSV file into a Pandas DataFrame
  df = pd.read_csv(file_path, skiprows=range(1, start_line), nrows=end_line - start_line + 1)
  return df[['url', 'type']].values.tolist()

