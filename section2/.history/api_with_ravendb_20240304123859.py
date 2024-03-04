from fastapi import FastAPI
from pydantic import BaseModel
from ravendb.client.documents.session import DocumentSession

app = FastAPI()

# Initialize RavenDB DocumentStore
store = DocumentSession(urls=["http://localhost:8080"], database="YourDatabase")
store.initialize()

# Define Pydantic model for your data
class BankData(BaseModel):
    bank_name: str
    data: str

# FastAPI endpoint to retrieve data from RavenDB
@app.get("/api/data/")
async def get_data():
    with store.open_session() as session:
        data = session.query(collection_name="BankData").all()
        return data

# FastAPI endpoint to insert data into RavenDB
@app.post("/api/data/")
async def insert_data(data: BankData):
    with store.open_session() as session:
        session.store(data.dict(), collection_name="BankData")
        session.save_changes()
        return {"message": "Data inserted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
