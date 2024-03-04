# fast api 


from fastapi import FastAPI

app = FastAPI()
# scraping livret bank

@app.get("/")

def read_root():

    return {"This is the root of the API of scraping livret bank"}


