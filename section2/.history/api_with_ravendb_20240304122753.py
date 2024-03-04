from fastapi import FastAPI
from pydantic import BaseModel
from ravendb import DocumentStore
f
app = FastAPI()

# Se connecter à la base de données RavenDB
store = DocumentStore(urls=["http://localhost:8080"], database="WebData")
store.initialize()

# Define a Pydantic model for the data structure
class BankData(BaseModel):
    bank_name: str
    data: str

# Fonction FastAPI pour récupérer les données extraites depuis RavenDB
@app.get("/api/data/")
async def get_data():
    with store.open_session() as session:
        # Interroger la base de données RavenDB pour récupérer les données extraites
        data = session.query(collection_name="WebData").all()
        return data



#exemple d'utilisation
    
if __name__ == "__main__":
    # Web scraping and RavenDB insertion
    scraper = WebScraper()
    extracted_data = scraper.scrape_data()

    with store.open_session() as session:
        for data_entry in extracted_data:
            # Insert each data entry into RavenDB
            session.store(data_entry)
        session.save_changes()
