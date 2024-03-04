import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.base_url = self.get_base_url(url)
        self.information = {}

    def get_base_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.scheme + "://" + parsed_url.netloc

    def extract_content(self):
        try:
            # Make the HTTP request
            response = requests.get(self.url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, "html.parser")

                # Extract documents
                links = soup.find_all("a", href=True)
                documents = [l for l in links if 'pdf' in l.get("href")]
                self.information['documents'] = list(set([urljoin(self.base_url, document.get("href")) for document in documents]))
                # Extract paragraphs
                paragraphs = soup.find_all("p")
                self.information['taux'] = []
                self.information['conditions'] = [ l for l in self.information['documents'] if 'condition' in l   ]
                for paragraph in paragraphs:
                    text = paragraph.text.strip().lower()
                    if 'taux' in text:
                        self.information['taux'].append(paragraph.text.strip())
                    
            else:
                print("The request failed with status code:", response.status_code)

        except requests.RequestException as e:
            print("A network error occurred:", e)

    def to_dict(self):
        return self.information



# Example usage
    

    