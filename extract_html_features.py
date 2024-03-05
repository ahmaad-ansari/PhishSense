"""
HTML Feature Extraction Script

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
- Run the script using 'python script_name.py'.

Author: Ahmaad Ansari
Date: March 5, 2024
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class HTMLFeatureExtractor:
    def __init__(self, html_content):
        try:
            self.soup = BeautifulSoup(html_content, 'html.parser')
        except Exception as e:
            print(f"Error creating BeautifulSoup object: {e}")
            raise

        self.features = {}

    def extract_binary_features(self):
        # Binary features
        try:
            self.features['has_title'] = bool(self.soup.title)
            self.features['has_meta_description'] = bool(self.soup.find('meta', {'name': 'description'}))
            self.features['has_form'] = bool(self.soup.form)
            self.features['has_input'] = bool(self.soup.input)
            self.features['has_button'] = bool(self.soup.button)
            self.features['has_img'] = bool(self.soup.img)
            self.features['has_submit_button'] = bool(self.soup.find('input', {'type': 'submit'}))
            self.features['has_link'] = bool(self.soup.a)
            self.features['has_password_input'] = bool(self.soup.find('input', {'type': 'password'}))
            self.features['has_email_input'] = bool(self.soup.find('input', {'type': 'email'}))
            self.features['has_hidden_element'] = bool(self.soup.find(style='display:none;') or self.soup.find(type='hidden'))
            self.features['has_audio'] = bool(self.soup.audio)
            self.features['has_video'] = bool(self.soup.video)
            self.features['has_js_redirect'] = bool(self.soup.find('script', string='window.location.href'))
            self.features['has_meta_refresh_redirect'] = bool(self.soup.find('meta', {'http-equiv': 'refresh'}))
            self.features['has_onclick_event'] = bool(self.soup.find('[onclick]'))
            self.features['has_document_url_change'] = bool(self.soup.find('script', string='document.URL'))
            # Check if the script tag exists before accessing the string attribute
            script_tag = self.soup.find('script')
            self.features['has_inline_js'] = bool(script_tag and script_tag.string)
            self.features['has_external_link_new_tab'] = bool(self.soup.find('a', {'target': '_blank'}))
            self.features['has_cors'] = bool(self.soup.find_all('script', {'crossorigin': True}))
            self.features['has_js_obfuscation'] = bool(self.soup.find('script', string='eval(function'))
        except Exception as e:
            print(f"Error extracting binary features: {e}")

    def extract_quantitative_features(self):
        # Quantitative features
        try:
            self.features['num_input_tags'] = len(self.soup.find_all('input'))
            self.features['num_button_tags'] = len(self.soup.find_all('button'))
            self.features['num_img_tags'] = len(self.soup.find_all('img'))
            self.features['num_option_tags'] = len(self.soup.find_all('option'))
            self.features['num_list_tags'] = len(self.soup.find_all(['ul', 'ol']))
            self.features['num_th_tags'] = len(self.soup.find_all('th'))
            self.features['num_tr_tags'] = len(self.soup.find_all('tr'))
            self.features['num_href_attributes'] = len(self.soup.find_all('a', href=True))
            self.features['num_paragraph_tags'] = len(self.soup.find_all('p'))
            self.features['num_script_tags'] = len(self.soup.find_all('script'))
            self.features['num_external_domains'] = len(set(self.extract_external_domains()))
            self.features['num_external_resources'] = len(self.extract_external_resources())
            self.features['num_external_forms'] = len(self.extract_external_forms())
            self.features['num_external_links'] = len(self.extract_external_links())
            self.features['num_external_images'] = len(self.extract_external_images())
        except Exception as e:
            print(f"Error extracting quantitative features: {e}")

    def extract_heuristic_features(self):
        # Heuristic features
        try:
            self.features['url_length'] = len(self.soup.prettify())  # Replace with an appropriate length metric
            self.features['has_ip_in_url'] = None
            self.features['uses_url_shortener'] = None
            self.features['uses_https'] = None
            self.features['has_login_forms'] = bool(self.soup.find('input', {'type': 'password'}))
            self.features['percentage_external_resources'] = self.calculate_percentage_external_resources()
            self.features['percentage_external_forms'] = self.calculate_percentage_external_forms()
            self.features['percentage_external_links'] = self.calculate_percentage_external_links()
            self.features['percentage_js_content'] = self.calculate_percentage_js_content()
            self.features['has_non_standard_protocols'] = bool(self.soup.find_all(lambda tag: any(attr.startswith(('ftp:', 'telnet:')) for attr in tag.get('href', ''))))
            self.features['has_multiple_domain_redirects'] = None
            self.features['domain_name_similarity'] = None
        except Exception as e:
            print(f"Error extracting heuristic features: {e}")

    def extract_external_domains(self):
        try:
            return [urlparse(tag['src']).netloc for tag in self.soup.find_all(['script', 'link', 'img', 'a'], src=True, href=True)]
        except Exception as e:
            print(f"Error extracting external domains: {e}")
            return []

    def extract_external_resources(self):
        try:
            return [tag['src'] for tag in self.soup.find_all(['script', 'link', 'img'], src=True, href=True)]
        except Exception as e:
            print(f"Error extracting external resources: {e}")
            return []

    def extract_external_forms(self):
        try:
            return [form['action'] for form in self.soup.find_all('form', action=True) if urlparse(form['action']).netloc]
        except Exception as e:
            print(f"Error extracting external forms: {e}")
            return []

    def extract_external_links(self):
        try:
            return [link['href'] for link in self.soup.find_all('a', href=True) if urlparse(link['href']).netloc]
        except Exception as e:
            print(f"Error extracting external links: {e}")
            return []

    def extract_external_images(self):
        try:
            return [img['src'] for img in self.soup.find_all('img', src=True) if urlparse(img['src']).netloc]
        except Exception as e:
            print(f"Error extracting external images: {e}")
            return []

    def calculate_percentage_external_resources(self):
        try:
            total_resources = len(self.soup.find_all(['script', 'link', 'img'], src=True, href=True))
            external_resources = len(self.extract_external_resources())
            return (external_resources / total_resources) * 100 if total_resources > 0 else 0
        except Exception as e:
            print(f"Error calculating percentage of external resources: {e}")
            return 0

    def calculate_percentage_external_forms(self):
        try:
            total_forms = len(self.soup.find_all('form', action=True))
            external_forms = len(self.extract_external_forms())
            return (external_forms / total_forms) * 100 if total_forms > 0 else 0
        except Exception as e:
            print(f"Error calculating percentage of external forms: {e}")
            return 0

    def calculate_percentage_external_links(self):
        try:
            total_links = len(self.soup.find_all('a', href=True))
            external_links = len(self.extract_external_links())
            return (external_links / total_links) * 100 if total_links > 0 else 0
        except Exception as e:
            print(f"Error calculating percentage of external links: {e}")
            return 0

    def calculate_percentage_js_content(self):
        try:
            total_content = len(''.join([str(tag) for tag in self.soup.find_all()]))
            js_content = len(''.join([str(tag) for tag in self.soup.find_all('script')]))
            return (js_content / total_content) * 100 if total_content > 0 else 0
        except Exception as e:
            print(f"Error calculating percentage of JS content: {e}")
            return 0

    def detect_multiple_domain_redirects(self, url):
        try:
            redirect_urls = set()
            current_url = url
            for tag in self.soup.find_all(['meta', 'script'], {'http-equiv': 'refresh'}):
                content = tag.get('content', '')
                if 'url=' in content:
                    redirect_url = content.split('url=')[1].split(';')[0].strip()
                    if redirect_url:
                        absolute_url = urljoin(current_url, redirect_url)
                        current_url = absolute_url
                        redirect_urls.add(urlparse(absolute_url).netloc)
            return len(redirect_urls) > 1
        except Exception as e:
            print(f"Error detecting multiple domain redirects: {e}")
            return False

    def calculate_domain_name_similarity(self, url):
        try:
            if url:
                original_domain = urlparse(url).netloc.replace('www.', '')
                phishing_domain = urlparse(self.soup.head.find('meta', {'name': 'author'}).get('content', '')).netloc.replace('www.', '')
                return sum([1 for a, b in zip(original_domain, phishing_domain) if a == b]) / len(original_domain) * 100
            return None
        except Exception as e:
            print(f"Error calculating domain name similarity: {e}")
            return None

    def print_features(self):
        for feature, value in self.features.items():
            print(f"{feature}: {value}")

def main():
    # Example usage
    html_file_path = 'html_dataset/www.example.com.html'

    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Instantiate the HTMLFeatureExtractor class
        html_feature_extractor = HTMLFeatureExtractor(html_content)

        # Extract binary features
        html_feature_extractor.extract_binary_features()

        # Extract quantitative features
        html_feature_extractor.extract_quantitative_features()

        # Extract heuristic features
        html_feature_extractor.extract_heuristic_features()

        # Print all features
        html_feature_extractor.print_features()
    except Exception as e:
        print(f"Error processing HTML file: {e}")

if __name__ == "__main__":
    main()
