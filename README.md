# PhishSense

## Web Scraping Script

This script reads a list of website URLs from a file, scrapes their HTML content, and saves it in a specified directory.

Script Flow:
1. Reads website URLs from 'website_list.txt'.
2. Fetches HTML content from each URL using BeautifulSoup.
3. Saves HTML content in individual files in the 'html_dataset' directory.

Usage:
- Ensure 'requests', 'beautifulsoup4', and 'bs4' are installed.
- Create a virtual environment and install dependencies using 'pip install -r requirements.txt'.
- Create 'website_list.txt' with a list of website URLs.
- Run the script using 'python webscraper.py'.

## HTML Feature Extraction Script

This script extracts various features from an HTML file using BeautifulSoup.

Script Flow:
1. Instantiates the HTMLFeatureExtractor class with the HTML content.
2. Extracts binary features such as the presence of tags (title, form, input, etc.).
3. Extracts quantitative features like the number of tags (input, button, img, etc.).
4. Extracts heuristic features to aid in phishing detection.
5. Prints the extracted features.

Usage:
- Ensure 'requests' and 'beautifulsoup4' are installed.
- Create a virtual environment and install dependencies using 'pip install -r requirements.txt'.
- Specify the path to the HTML file in 'html_file_path'.
- Run the script using 'python extract_html_features.py'.
