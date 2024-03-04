import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

list_of_urls = [
    "https://www.creditmutuel.fr/fr/particuliers/epargne/livret-de-developpement-durable.html",
    "https://www.monabanq.com/fr/produits-bancaires/livret-developpement-durable/en-resume.html",
    "https://www.banquepopulaire.fr/bpaura/epargner/livret-transition-energetique/"
]

class WebScraper:
    def __init__(self, list_of_urls):
        self.list_of_urls = list_of_urls
        self.information = {}

    def get_base_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.scheme + "://" + parsed_url.netloc

    def extract_content(self, url):
        try:
            # Make the HTTP request
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content, "html.parser")

                # Extract documents
                links = soup.find_all("a", href=True)
                documents = [l for l in links if 'pdf' in l.get("href")]
                self.information['documents'] = list(set([urljoin(self.get_base_url(url), document.get("href")) for document in documents]))
                # Extract paragraphs
                paragraphs = soup.find_all("p")
                self.information['taux'] = []
                self.information['conditions'] = [l for l in self.information['documents'] if 'condition' in l]
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

    def get_data_all_urls(self):
        d = {}
        for url in self.list_of_urls:
            self.extract_content(url)
            d[url] = self.to_dict()

        return d
        
# Example usage
if __name__ == "__main__":
    url = "https://www.monabanq.com/fr/produits-bancaires/livret-developpement-durable/en-resume.html"
    scraper = WebScraper([url])
    scraper.extract_content(url)
    output_dict = scraper.to_dict()
    print(output_dict)


