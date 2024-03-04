# Importation des librairies nécessaires
import requests
import logging
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
impo
# Configure logging
logging.basicConfig(filename='web_scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a Pydantic model for the data structure
class BankData(BaseModel):
    bank_name: str
    data: dict

# Class Definitions
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
                self.information['taux'] = [p.text.strip() for p in paragraphs if 'taux' in p.text.strip().lower()]
                self.information['conditions'] = [p.text.strip() for p in paragraphs if 'condition' in p.text.strip().lower()]
                
                logging.info(f"Content extracted from {self.url}")
            else:
                logging.error(f"The request failed with status code: {response.status_code}")

        except requests.RequestException as e:
            logging.error(f"A network error occurred: {e}")

    def to_dict(self):
        return self.information

# Initialize the MongoDB client
app = FastAPI()

client = MongoClient('mongodb://localhost:27017/')
db = client['web_data']
collection = db['bank_data']

# Function Definitions
# root 
@app.get("/")
async def root():
    return {"message": "This is the root of the API of the web scraper."}

@app.get("/api/data/", response_model=List[BankData])
async def get_data():
    # Fetch data from MongoDB
    data = []
    try:
        for doc in collection.find():
            data.append(BankData(bank_name=doc['bank_name'], data=doc['data']))
    except Exception as e:
        logging.error(f"An error occurred while fetching data from MongoDB: {e}")
        # Handle the exception appropriately

    return data

if __name__ == "__main__":
    # Extraction de données
    urls = [
        "https://www.creditmutuel.fr/fr/particuliers/epargne/livret-de-developpement-durable.html",
        "https://www.monabanq.com/fr/produits-bancaires/livret-developpement-durable/en-resume.html",
        "https://www.banquepopulaire.fr/bpaura/epargner/livret-transition-energetique/"
    ]

    for url in urls:
        scraper = WebScraper(url)
        scraper.extract_content()
        data = scraper.to_dict()

        # Enregistrement des données dans MongoDB
        try:
            collection.insert_one({'bank_name': url, 'data': data})
            logging.info(f"Data saved to MongoDB for URL: {url}")
        except Exception as e:
            logging.error(f"An error occurred while saving data to MongoDB: {e}")

    # Exécution du serveur FastAPI 
    uvicorn.run(app, host="127.0.0.1", port=8000)
