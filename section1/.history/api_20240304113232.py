





# ------------------
#  Partie API FastAPI
# ------------------
# Création d'une instance de FastAPI
app = FastAPI()

# Liste des comptes Twitter à scraper
accounts = [
    "https://twitter.com/RevolutApp",
    "https://twitter.com/mabanque_bnpp?lang=fr",
    "https://twitter.com/Leocare_Assure"
]

scraper = TwitterScraper(accounts)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Twitter Scraper API!"}

@app.get("/user/", response_model=User)
def get_user(account_url: HttpUrl):
    return scraper.get_user(account_url)

@app.get("/users/", response_model=List[User])
def get_users():
    return scraper.get_users()

@app.get("/tweets/", response_model=List[Tweet])
def get_tweets(account_url: HttpUrl):
    return scraper.get_tweets(account_url)

@app.get("/tweet/", response_model=TweetDetails)
def get_tweet_details(tw_id: str, base_url: str = "https://twitter.com/RevolutApp"):
    return scraper.get_tweet_details(base_url, tw_id)

# Exécution du serveur FastAPI 
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
