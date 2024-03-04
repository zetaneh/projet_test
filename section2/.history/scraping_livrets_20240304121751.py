import requests
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from pymongo import MongoClient
import uvicorn

# Constants and Global Variables
urls = [
    "https://www.creditmutuel.fr/fr/particuliers/epargne/livret-de-developpement-durable.html",
    "https://www.monabanq.com/fr/produits-bancaires/livret-developpement-durable/enresume.html",
    "https://www.banquepopulaire.fr/bpaura/epargner/livret-transition-energetique/"
]

# Define a Pydantic model for the data structure
class BankData(BaseModel):
    bank_name: str
    data: str

# Class Definitions
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
    for doc in collection.find():
        data.append(BankData(bank_name=doc['bank_name'], data=doc['data']))
    return data

# Main Execution
if __name__ == "__main__":
    # Web scraping and MongoDB insertion
    scraper = WebScraper()
    extracted_data = scraper.scrape_data()

    for data_entry in extracted_data:
        # Insert each data entry into MongoDB
        collection.insert_one(data_entry.dict())

    # Start FastAPI server
    uvicorn.run(app, host="127.0.0.1", port=8000)
