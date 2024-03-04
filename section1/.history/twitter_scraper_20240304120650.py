# Importation des librairies nécessaires

import logging
import time
from playwright.sync_api import sync_playwright
from pydantic import BaseModel
from typing import List


# ------------------
#  Partie Scraper
# ------------------
# Liste des comptes Twitter à scraper
accounts = [
    "https://twitter.com/RevolutApp",
    "https://twitter.com/mabanque_bnpp?lang=fr",
    "https://twitter.com/Leocare_Assure"
]


# Définition de la classe User
class User(BaseModel): 
    username: str 
    follower_count: str

# Définition de la classe Tweet
class Tweet(BaseModel):
    id: int
    date: str
    link: str

# Définition de la classe TweetDetails
class TweetDetails(BaseModel):
    id: str
    tweet_body: str
    tweet_date: str
    retweet: str
    mention: str
    like: str
    url: str

# Définition de la classe TwitterScraper
class TwitterScraper:
    def __init__(self, accounts):
        self.accounts = accounts
        self.logger = self.setup_logger()
        self.page = None

    # Méthode pour configurer le logger
    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler('twitter_scraper.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    # Méthode pour attendre le scroll jusqu'en bas de la page
    def wait_scroll_to_bottom(self):
        time.sleep(5)  # Wait for page to load  
        for _ in range(5): 
            self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(5)

    # Méthode pour obtenir les données d'un utilisateur
    def get_user(self, account_url: str) -> User:
        username = account_url.split("/")[-1]

        with sync_playwright() as p:
            self.logger.info(f"Scraping data for {account_url}")
            browser = p.chromium.launch()
            self.page = browser.new_page()
            self.page.goto(account_url)

            follower_count_element = self.page.wait_for_selector("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span")
            follower_count = follower_count_element.inner_text().strip() 

            browser.close()
            user = User(username=username, follower_count=follower_count)  

            self.logger.info(f"Data scraped for {account_url}: {user}")

            return user
    
    # Méthode pour obtenir les données de plusieurs utilisateurs
    def get_users(self) -> List[User]:
        users = []
        for account in self.accounts:
            user = self.get_user(account)
            users.append(user)
        return users

    def get_followers(self, account_url: str) -> List[User]:
        pass

    def get_following(self, account_url: str) -> List[User]:
        pass

    def get_tweets(self, account_url: str) -> List[str]:
        with sync_playwright() as p:
            self.logger.info(f"Scraping tweets for {account_url}")
            browser = p.chromium.launch()
            self.page = browser.new_page()
            self.page.goto(account_url)
            self.wait_scroll_to_bottom()

            tweet_elements = self.page.query_selector_all("a[href*='/status']")
            tweet_elements = [tweet for tweet in tweet_elements if "analytics" not in tweet.get_attribute("href")]
            tweets = []
            for tweet_element in tweet_elements:
                try:
                    tweet_link = 'https://twitter.com' + tweet_element.get_attribute("href")
                    tweet_id = tweet_link.split("/")[-1]
                    tweet_date = tweet_element.inner_text().strip()
                    tweet = Tweet(id=tweet_id, date=tweet_date, link=tweet_link)
                    tweets.append(tweet)
                except Exception as e:
                    self.logger.error(f"Error scraping tweet: {e}")
            browser.close()
            self.logger.info(f"Scraped {len(tweets)} tweets for {account_url}")
            return tweets

    def get_tweet_details(self, base_url: str, tw_id: str):
        url = f"{base_url}/status/{str(tw_id)}"

        with sync_playwright() as p:
            self.logger.info(f"Scraping data for {url}")
            browser = p.chromium.launch()
            self.page = browser.new_page()
            self.page.goto(url)

            tweet_body = self.page.query_selector("div[lang='en'] > span").inner_text()
            tweet_date = self.page.query_selector("time").inner_text()

            inf = self.page.query_selector_all("span[data-testid='app-text-transition-container']")
            try:
                retweet = inf[0].inner_text()
                mention = inf[1].inner_text()
                like = inf[2].inner_text()
            except IndexError:
                retweet, mention, like = 0, 0, 0

            tweet_details = TweetDetails(id=tw_id, tweet_body=tweet_body, tweet_date=tweet_date, retweet=retweet, mention=mention, like=like, url=url)

            self.logger.info(f"Data scraped for {url}: {tweet_details}")

            return tweet_details

    def get_hashtags(self, account_url: str) -> List[str]:
        pass

    def get_media(self, account_url: str) -> List[str]:
        pass
        
    def get_likes(self, account_url: str) -> List[str]:
        pass

    def run(self):
        self.get_users()
        self.get_tweets(self.accounts[0])
        self.get_tweet_details(self.accounts[0], "1763611561493491828")


# Exécution du scraper
        
if 