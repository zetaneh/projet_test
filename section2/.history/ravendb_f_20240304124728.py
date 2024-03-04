from ravendb import DocumentStore


class RavenDB:
    def __init__(self, urls, database):
        self.store = DocumentStore(urls=urls, database=database)
        self.store.initialize()

    def open_session(self):
        return self.store.open_session()
    
    def close(self):
        self.store.disposed()
# Example usage
if __name__ == "__main__":
    urls = ["http://localhost:8080"]
    database = "BankData"
    raven = RavenDB(urls, database)
    with raven.open_session() as session:
        # Perform operations with the session
        print("Session opened")
        #example usage
        session.store({"bank_name": "Credit Mutuel", "data": "Some data"},"BankData")
        session.save_changes()
    

    #load data
        
    with raven.open_session() as session:
        data = session.query(collection_name="BankData").all()
        print(data)








        