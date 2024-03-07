import requests

class WebScraper:
    def __init__(self):
        pass

    def get_html(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_html(self, url):
        html_content = self.get_html(url)
        return html_content if html_content else None
