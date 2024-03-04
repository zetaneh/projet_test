import requests
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from pymongo import MongoClient
"""
pip install fastapi

pip install pymongo

pip install uvicorn

"""
# Define a Pydantic model for the data structure
class BankData(BaseModel):
    bank_name: str
    data: str

app = FastAPI()

class WebScraper:
    def __init__(self):
        self.urls = [
            "https://www.creditmutuel.fr/fr/particuliers/epargne/livret-de-developpement-durable.html",
            "https://www.monabanq.com/fr/produits-bancaires/livret-developpement-durable/enresume.html",
            "https://www.banquepopulaire.fr/bpaura/epargner/livret-transition-energetique/"
        ]

    def scrape_data(self):
        data = []
        for url in self.urls:
            response = requests.get(url)
            # Code to extract specific data from each site
            # Add the extracted data to the list 'data'
        return data

# Initialize the MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['web_data']
collection = db['bank_data']

@app.get("/api/data/", response_model=List[BankData])
async def get_data():
    # Fetch data from MongoDB
    data = []
    for doc in collection.find():
        data.append(BankData(bank_name=doc['bank_name'], data=doc['data']))
    return data

if __name__ == "__main__":
    # Web scraping and MongoDB insertion
    scraper = WebScraper()
    extracted_data = scraper.scrape_data()

    for data_entry in extracted_data:
        # Insert each data entry into MongoDB
        collection.insert_one(data_entry.dict())

    # Start FastAPI server
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
