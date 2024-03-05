"""
Web Scraping Script

This script reads a list of website URLs from a file, scrapes their HTML content,
and saves it in a specified directory.

Script Flow:
1. Reads website URLs from 'website_list.txt'.
2. Fetches HTML content from each URL using BeautifulSoup.
3. Saves HTML content in individual files in the 'html_dataset' directory.

Usage:
- Ensure 'requests', 'beautifulsoup4', and 'bs4' are installed.
- Create a virtual environment and install dependencies using 'pip install -r requirements.txt'.
- Create 'website_list.txt' with a list of website URLs.
- Run the script using 'python script_name.py'.

Author: Ahmaad Ansari
Date: March 5, 2024
"""

import os
import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        # Fetch the HTML content from the URL with a timeout of 10 seconds
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_and_save_html(url, save_directory):
    html_content = get_html(url)

    if html_content:
        # Extracting the domain name to use as a filename
        try:
            domain_name = url.split('//')[1].split('/')[0]
        except IndexError:
            print(f"Error extracting domain name from {url}")
            return

        filename = f"{domain_name}.html"

        # Creating the directory if it doesn't exist
        try:
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
                print(f"Created directory: {save_directory}")
        except OSError as e:
            print(f"Error creating directory {save_directory}: {e}")
            return

        # Saving the HTML content to a file
        try:
            with open(os.path.join(save_directory, filename), 'w', encoding='utf-8') as file:
                file.write(html_content)
                print(f"Saved HTML content for {url} in {filename}")
        except IOError as e:
            print(f"Error saving file {filename}: {e}")

def scrape_multiple_websites_from_file(file_path, save_directory):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    for url in urls:
        scrape_and_save_html(url, save_directory)

def main():
    # Specify the file containing the list of website names
    website_list_file = 'website_list.txt'

    # Specify the directory to save HTML files
    save_directory = 'html_dataset'

    # Scrape and save HTML for multiple websites from the file
    print(f"Scraping websites from {website_list_file} and saving HTML in {save_directory}")
    scrape_multiple_websites_from_file(website_list_file, save_directory)

if __name__ == "__main__":
    main()
