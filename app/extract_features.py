"""
URL Feature Extraction Module

This script defines functions for extracting features from HTML content of URLs and saving the results to a CSV file.
The module includes the 'extract_features' function, which takes a URL and its type as input, performs a web request,
parses the HTML content, and extracts features such as title and the number of links. Additionally, the 'process_urls'
function utilizes 'extract_features' to process a list of URLs with their corresponding types, creating a Pandas DataFrame
from the extracted features and saving it to a specified output CSV file.

Usage:
  from extract_features import extract_features, process_urls
  features_list = extract_features('http://example.com', 'legitimate')
  process_urls([(url1, type1), (url2, type2)], 'output_features.csv')

Functions:
  - extract_features(url, website_type): Extracts features from the HTML content of a URL.
  - process_urls(urls_and_types, output_file): Processes a list of URLs with types and saves the features to a CSV file.

Note: The 'extract_features' function can be modified to include additional features as needed.

Author: Ahmaad Ansari
Date: March 10, 2024
"""

import os
import logging
import requests
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import re

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configure the logger to print to the console
console = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')

# Set up colors for logging levels
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0m"

# Create a class to colorize log messages
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.ERROR:
            return RED + super().format(record) + RESET
        elif record.levelno == logging.INFO:
            return GREEN + super().format(record) + RESET
        else:
            return super().format(record)

console.setFormatter(ColoredFormatter('%(levelname)s: %(message)s'))

# Add the console handler to the logger
logger.addHandler(console)

def extract_features(url, website_type):
    result = None  # Initialize result to None

    try:
        # Ensure the URL has the correct protocol (https:// or http://)
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Set a user agent to mimic a web browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        # Make a request to the URL with headers
        response = requests.get(url, headers=headers, timeout=5, verify=False)

        # Check for successful response status code
        response.raise_for_status()

        # Log successful request
        logger.info(f"Successfully fetched {url}")

    except requests.exceptions.RequestException as e:
        # Log error if the request fails
        logger.error(f"Error fetching {url}: {e}")
    else:
        # If there was no error, proceed with further processing
        result = extract_features_from_html(response.text, url, website_type)

    return result

def extract_features_from_html(html_content, url, website_type):
    # Use BeautifulSoup to parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Binary Features
    has_login_form = len(soup.select('form[action*="login"]')) > 0
    has_https = url.startswith('https://')
    has_iframe = len(soup.find_all('iframe')) > 0
    phishing_words = ['login', 'password', 'account', 'verify', 'security', 'authenticate', 'update', 'confirm', 'identity', 'validation', 'billing', 'unusual', 'suspicious', 'urgent', 'information', 'recovery', 'suspend', 'fraud', 'alert', 'compromise']
    has_phishing_words = any(word in html_content.lower() for word in phishing_words)
    has_title = bool(soup.title)
    keywords = ['official', 'authorized', 'genuine', 'secure', 'trusted', 'verified', 'legitimate']
    has_keywords = any(word in html_content.lower() for word in keywords)
    has_external_links = any('href' in link.attrs and link['href'].startswith(('http://', 'https://')) for link in soup.find_all('a'))
    has_popular_script_libraries = any(lib in html_content.lower() for lib in ['jquery', 'angular', 'react', 'vue'])

    # Quantitative Features
    num_links = len(soup.find_all('a'))
    num_images = len(soup.find_all('img'))
    num_scripts = len(soup.find_all('script'))
    num_styles = len(soup.find_all('link', rel='stylesheet'))
    num_forms = len(soup.find_all('form'))
    num_input_tags = len(soup.find_all('input'))

    # Content Length Features
    content_length = len(html_content)
    avg_word_length = sum(len(word) for word in re.findall(r'\b\w+\b', html_content)) / len(re.findall(r'\b\w+\b', html_content)) if len(re.findall(r'\b\w+\b', html_content)) > 0 else 0

    # Heuristic Features
    avg_link_text_length = sum(len(link.text) for link in soup.find_all('a')) / num_links if num_links > 0 else 0

    # URL Structure Features
    num_subdomains = len(url.split('.')) - 2  # subtract 2 to exclude 'http://' or 'https://'
    num_special_chars = sum(1 for char in url if char in ['-', '_', '.', '~', ':', '/', '?', '#', '[', ']', '@', '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', '='])  # count special characters in the URL

    return {
        'url': url,
        'type': website_type,
        'has_login_form': has_login_form,
        'has_https': has_https,
        'has_iframe': has_iframe,
        'has_phishing_words': has_phishing_words,
        'num_links': num_links,
        'num_images': num_images,
        'num_scripts': num_scripts,
        'num_styles': num_styles,
        'num_forms': num_forms,
        'num_input_tags': num_input_tags,
        'content_length': content_length,
        'avg_word_length': avg_word_length,
        'has_title': has_title,
        'has_keywords': has_keywords,
        'has_external_links': has_external_links,
        'avg_link_text_length': avg_link_text_length,
        'has_popular_script_libraries': has_popular_script_libraries,
        'num_subdomains': num_subdomains,
        'num_special_chars': num_special_chars
    }

import os

def process_urls(urls_and_types, output_file):
    # Initialize an empty list to store features
    features_list = []

    # Check if the output CSV file already exists
    if os.path.exists(output_file):
        # If it exists, read the existing data
        existing_data = pd.read_csv(output_file)
        # Append the new features to the existing data
        features_list += existing_data.to_dict('records')

    for url, website_type in urls_and_types:
        # Extract features for each URL
        features = extract_features(url, website_type)

        # Check if features were successfully extracted
        if features is not None:
            features_list.append(features)

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(features_list)

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)
