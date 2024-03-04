from ravendb import DocumentStore
from fastapi import FastAPI
from pydantic import BaseModel
from web_scraper import WebScraper
import uvicorn
app = FastAPI()

class RavenDB:
    def __init__(self, urls, database):
        self.store = DocumentStore(urls=urls, database=database)
        self.store.initialize()

    def open_session(self):
        return self.store.open_session()
    
    def close(self):
        self.store.dispose()

class BankData(BaseModel):
    bank_name: str
    data: str

# Initialize RavenDB
urls = ["http://localhost:8080"]
database = "BankData"
raven = RavenDB(urls, database)
scraped_data = WebScraper(["https://www.creditmutuel.fr/fr/particuliers/epargne/livret-de-developpement-durable.html",
                            "https://www.monabanq.com/fr/produits-bancaires/livret-developpement-durable/en-resume.html",
                            "https://www.banquepopulaire.fr/bpaura/epargner/livret-transition-energetique/"]).get_data_all_urls()





# FastAPI endpoint to scrape data from URLs and store in RavenDB
@app.post("/scrape/")
async def scrape_and_store_data(data: BankData):
    with raven.open_session() as session:
        session.store(data.dict(),"BankData")
        session.save_changes()
        return {"message": "Data scraped and stored successfully"}

# FastAPI endpoint to retrieve data from RavenDB
@app.get("/data/")
async def get_data():
    with raven.open_session() as session:
        data = session.query("BankData").all()
        return data




# Exécution du serveur FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)