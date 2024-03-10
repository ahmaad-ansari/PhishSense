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

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import logging

def extract_features(url, website_type):
    try:
        # Set a user agent to mimic a web browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        # Make a request to the URL with headers
        response = requests.get(url, headers=headers, timeout=5)

        # Check for successful response status code
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

    return extract_features_from_html(response.text, url, website_type)

def extract_features_from_html(html_content, url, website_type):
    # Use BeautifulSoup to parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Binary Features
    has_login_form = len(soup.select('form[action*="login"]')) > 0
    has_https = url.startswith('https://')
    has_iframe = len(soup.find_all('iframe')) > 0
    phishing_words = ['login', 'password', 'account', 'verify', 'security', 'authenticate', 'update', 'confirm', 'identity', 'validation', 'billing', 'unusual', 'suspicious', 'urgent', 'information', 'recovery', 'suspend', 'fraud', 'alert', 'compromise']
    has_phishing_words = any(word in html_content.lower() for word in phishing_words)

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
    title = soup.title.text.strip() if soup.title else None
    keywords = ['official', 'authorized', 'genuine', 'secure', 'trusted', 'verified', 'legitimate']
    has_keywords = any(word in html_content.lower() for word in keywords)
    has_external_links = any(link['href'].startswith(('http://', 'https://')) for link in soup.find_all('a'))
    avg_link_text_length = sum(len(link.text) for link in soup.find_all('a')) / num_links if num_links > 0 else 0
    has_popular_script_libraries = any(lib in html_content.lower() for lib in ['jquery', 'angular', 'react', 'vue'])

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
        'title': title,
        'has_keywords': has_keywords,
        'has_external_links': has_external_links,
        'avg_link_text_length': avg_link_text_length,
        'has_popular_script_libraries': has_popular_script_libraries,
        'num_subdomains': num_subdomains,
        'num_special_chars': num_special_chars
    }

def process_urls(urls_and_types, output_file):
    # Extract features for each URL
    features_list = [extract_features(url, website_type) for url, website_type in urls_and_types if extract_features(url, website_type) is not None]

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(features_list)

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)