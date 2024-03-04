from ravendb import DocumentStore


class RavenDB:
    def __init__(self, urls, database):
        self.store = DocumentStore(urls=urls, database=database)
        self.store.initialize()

    def open_session(self):
        return self.store.open_session()
    
    def close(self):
        self.store.disposed
# Example usage
if __name__ == "__main__":
    urls = ["http://localhost:8080"]
    database = "YourDatabase"
    raven = RavenDB(urls, database)
    with raven.open_session() as session:
        # Perform operations with the session
        print("Session opened")
        pass
    raven.close()
    print("Session closed")




        