"""
WebScraper Script

This script defines the WebScraper class, which provides functionality to fetch HTML content from a given URL using the requests library.

The class includes two methods:
  - get_html(url): Makes a GET request to the specified URL with a timeout of 10 seconds, checks if the request was
    successful, prints success or error messages, and returns the HTML content.
  - scrape_html(url): Calls the get_html method to fetch HTML content, checks if HTML content is retrieved
    successfully, prints success or error messages, and returns the HTML content.

Author: Ahmaad Ansari
Date: March 5, 2024
"""


import requests

class WebScraper:

    def __init__(self):
        pass

    def get_html(self, url):
        try:
            # Make a GET request to the specified URL with a timeout of 10 seconds
            response = requests.get(url, timeout=10)
            
            # Check if the request was successful (status code 200)
            response.raise_for_status()
            
            # Print a success message and return the HTML content
            print(f"Successfully fetched HTML from: {url}")
            return response.text
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that may occur during the request
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_html(self, url):
        # Call the get_html method to fetch HTML content
        html_content = self.get_html(url)
        
        # Check if HTML content is retrieved successfully
        if html_content:
            # Print a success message and return the HTML content
            print("HTML content successfully retrieved.")
            return html_content
        else:
            # Print an error message if HTML content retrieval fails
            print("Failed to retrieve HTML content.")
            return None
