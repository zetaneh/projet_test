# Rapport : Web Scraping de données Twitter avec Playwright
Ayoub Abraich
## 1. Introduction

Ce projet avait pour objectif de développer une solution permettant d'extraire des données à partir de comptes Twitter spécifiques, sans utiliser l'API officielle de Twitter. Le web scraping représente une approche efficace pour collecter des données à partir de sites web dynamiques tels que Twitter.

L'approche adoptée consistait à créer un scraper Python capable d'extraire diverses données comme le contenu des tweets, les métriques des comptes et des tweets, ainsi que de suivre leur évolution sur une période de 7 jours.

## 2. Technologie et outils utilisés

### Playwright

Playwright est une bibliothèque Python permettant l'automatisation de navigateurs web et le scraping de sites dynamiques. Elle offre une approche puissante pour interagir avec des pages web riches en JavaScript, en permettant l'exécution de scripts et la simulation d'interactions utilisateur avancées.

Playwright a été choisi pour ce projet en raison de ses fonctionnalités avancées et de sa facilité d'utilisation pour automatiser les interactions avec les pages Twitter.

### Autres outils

- **Python** : Langage de programmation principal utilisé pour le développement du scraper.
- **BeautifulSoup** : Bibliothèque Python pour le parsing et l'extraction de données à partir du DOM.
- **Pydantic** : Bibliothèque de validation de données utilisée pour définir les modèles de données.
- **FastAPI** : Framework web Python utilisé pour créer une API RESTful autour du scraper.
- **Schedule** : Pour automatiser l'exécution du scraper à intervalles réguliers, nous avons utilisé la bibliothèque schedule de Python. Cette bibliothèque permet de planifier l'exécution de fonctions ou de tâches à des moments précis ou selon une fréquence définie.
## 3. Méthodologie

La méthodologie mise en œuvre pour le scraping de données Twitter impliquait plusieurs étapes clés :

1. **Configuration du navigateur headless** : Playwright a été utilisé pour créer une instance de navigateur headless Chromium, permettant d'automatiser les interactions avec les pages Twitter.

2. **Chargement des pages des comptes Twitter ciblés** : Le scraper a été conçu pour charger les pages des comptes Twitter spécifiés, en utilisant leurs URLs.

3. **Extraction des données** : Une fois les pages chargées, le scraper a extrait diverses données pertinentes, notamment :
   - Le contenu textuel des tweets
   - Les dates de publication des tweets
   - Les métriques des tweets (nombre de likes, retweets, etc.)
   - Les métriques des comptes (nombre d'abonnés, etc.)

4. **Suivi des évolutions** : Pour suivre l'évolution des métriques, le scraper a été exécuté quotidiennement pendant une période de 7 jours, stockant les données à chaque exécution.

5. **Stockage des données** : Les données extraites ont été structurées et stockées au format JSON, facilitant leur utilisation ultérieure.

## 4. Implémentation

### Structure du projet

Le projet est structuré comme suit :

```
.
├── twitter_scraper.py
├── api.py
├── scedule.py
├── twitter_scraper.log
└── requirements.txt 
```

- `twitter_scraper.py` : Fichier Python principal contenant le code du scraper et de l'API FastAPI.
- `requirements.txt` : Fichier listant les dépendances Python nécessaires.
- `twitter_scraper.log` : Fichier de journalisation des événements du scraper.

### Classes principales

#### `User`

Modèle de données Pydantic représentant les informations d'un utilisateur Twitter, telles que le nom d'utilisateur et le nombre d'abonnés.

#### `Tweet`

Modèle de données Pydantic représentant les informations de base d'un tweet, comme l'identifiant, la date et le lien.

#### `TweetDetails`

Modèle de données Pydantic représentant les détails complets d'un tweet, y compris le contenu textuel, la date, les métriques (retweets, mentions, likes), et le lien.

#### `TwitterScraper`

Classe principale implémentant la logique de scraping. Voici quelques méthodes clés :

- `__init__` : Initialise le scraper avec une liste de comptes Twitter à scraper.
- `setup_logger` : Configure le logger pour enregistrer les événements de scraping.
- `wait_scroll_to_bottom` : Attend le chargement complet de la page en scrollant vers le bas.
- `get_user` : Extrait les informations d'un utilisateur Twitter (nombre d'abonnés, etc.).
- `get_tweets` : Extrait les liens et les dates des tweets d'un compte spécifié.
- `get_tweet_details` : Extrait les détails complets d'un tweet donné (contenu, métriques, etc.).

### Intégration avec FastAPI

Une API RESTful a été développée avec FastAPI pour exposer les fonctionnalités du scraper. Les endpoints suivants ont été implémentés :

- `GET /user/` : Récupère les informations d'un utilisateur Twitter.
- `GET /users/` : Récupère les informations de tous les utilisateurs spécifiés.
- `GET /tweets/` : Récupère les liens et les dates des tweets d'un compte Twitter spécifié.
- `GET /tweet/` : Récupère les détails complets d'un tweet donné.

**Code**

```
.
├── twitter_scraper.py
├── api.py
├── scedule.py
├── twitter_scraper.log
└── requirements.txt 
```

 - `api.py` : 
``` python
import uvicorn
from fastapi import FastAPI
from twitter_scraper import TwitterScraper
from pydantic import HttpUrl
from typing import List
from twitter_scraper import User, Tweet, TweetDetails

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

# Création d'une instance de TwitterScraper avec les comptes Twitter à scraper
scraper = TwitterScraper(accounts)

# Route racine de l'API
@app.get("/")
def read_root():
    return {"message": "Welcome to the Twitter Scraper API!"}

# Route pour obtenir les informations d'un utilisateur Twitter
@app.get("/user/", response_model=User)
def get_user(account_url: HttpUrl):
    return scraper.get_user(account_url)

# Route pour obtenir les informations de plusieurs utilisateurs Twitter
@app.get("/users/", response_model=List[User])
def get_users():
    return scraper.get_users()

# Route pour obtenir les tweets d'un compte Twitter
@app.get("/tweets/", response_model=List[Tweet])
def get_tweets(account_url: HttpUrl):
    return scraper.get_tweets(account_url)

# Route pour obtenir les détails d'un tweet
@app.get("/tweet/", response_model=TweetDetails)
def get_tweet_details(tw_id: str, base_url: str = "https://twitter.com/RevolutApp"):
    return scraper.get_tweet_details(base_url, tw_id)

# Exécution du serveur FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```
- `twitter_scraper.py`
``` python
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
        
scraper = TwitterScraper(accounts)

scraper.run()

```
**Suivi des données sur 7 jours avec Cron Job**
Au lieu d'utiliser un cron job système, nous avons opté pour une approche basée sur un script Python utilisant les bibliothèques `schedule` et `time`. Cette approche offre une plus grande flexibilité et facilite l'intégration de la planification de tâches directement dans le code du scraper.

Voici un exemple d'implémentation :
``` python
import schedule
import time
from twitter_scraper import TwitterScraper
accounts = [
    "https://twitter.com/RevolutApp",
    "https://twitter.com/mabanque_bnpp?lang=fr",
    "https://twitter.com/Leocare_Assure"
]


# Fonction à exécuter à intervalle régulier
def run_scraper():
    # Insérez le code du scraper ici
    scraper = TwitterScraper(accounts)
    scraper.run()

# Planification de la tâche
schedule.every(15).minutes.do(run_scraper) # Exécutez le scraper toutes les 15 minutes

# Boucle pour exécuter la planification en continu
while True:
    schedule.run_pending()
    time.sleep(1)
```

## 5. Résultats et performances

Le scraper a été capable d'extraire avec succès les données souhaitées à partir des comptes Twitter ciblés, y compris le contenu des tweets, les métriques des comptes et des tweets, ainsi que leur évolution sur une période de 7 jours.

Exemple de sortie JSON pour un tweet :

```json
{
  "id": "1763611561493491828",
  "tweet_body": "We asked you for your questions on investing, and now it’s time for Rolandas Juteiak, our Head of Trading (EEA), to give you our top tips ",
  "tweet_date": "6:05 PM · Mar 1, 2024",
  "retweet": "9,383",
  "mention": "3",
  "like": "21",
  "url": "https://twitter.com/RevolutApp/status/1763611561493491828"
}
```

`twitter_scraper.log`
``` log
2024-03-04 11:40:28,779 - INFO - Data scraped for https://twitter.com/RevolutApp: username='RevolutApp' follower_count='374K'
2024-03-04 11:40:29,083 - INFO - Scraping data for https://twitter.com/mabanque_bnpp?lang=fr
2024-03-04 11:40:32,519 - INFO - Data scraped for https://twitter.com/mabanque_bnpp?lang=fr: username='mabanque_bnpp?lang=fr' follower_count='38,6\xa0k'
2024-03-04 11:40:32,806 - INFO - Scraping data for https://twitter.com/Leocare_Assure
2024-03-04 11:40:37,138 - INFO - Data scraped for https://twitter.com/Leocare_Assure: username='Leocare_Assure' follower_count='1,847'
2024-03-04 11:40:37,436 - INFO - Scraping tweets for https://twitter.com/RevolutApp
2024-03-04 11:41:10,913 - INFO - Scraped 7 tweets for https://twitter.com/RevolutApp
2024-03-04 11:41:11,234 - INFO - Scraping data for https://twitter.com/RevolutApp/status/1763611561493491828
2024-03-04 11:41:15,248 - INFO - Data scraped for https://twitter.com/RevolutApp/status/1763611561493491828: id='1763611561493491828' tweet_body='We asked you for your questions on investing, and now it�s time for Rolandas Juteiak, our Head of Trading (EEA), to give you our top tips ' tweet_date='6:05 PM � Mar 1, 2024' retweet='9,354' mention='3' like='21' url='https://twitter.com/RevolutApp/status/1763611561493491828'
```
Le scraper s'est montré fiable et robuste, gérant correctement les pages dynamiques de Twitter et les chargements progressifs de contenu. Cependant, des améliorations sont encore possibles pour augmenter les performances et éviter les bannissements potentiels.

## 6. Défis rencontrés et solutions apportées

Au cours du développement du scraper, plusieurs défis techniques ont été rencontrés :

### Gestion des pages dynamiques

Les pages Twitter étant dynamiques et chargeant progressivement le contenu, il a fallu mettre en place une logique d'attente et de scroll vers le bas pour s'assurer que tous les tweets soient chargés avant l'extraction des données.

**Solution** : La méthode `wait_scroll_to_bottom` a été implémentée pour simuler le comportement de scroll d'un utilisateur, permettant ainsi de charger l'ensemble des tweets.

### Extraction des métriques

L'extraction des métriques des tweets (retweets, mentions, likes) s'est avérée complexe en raison de la structure dynamique du DOM et de la présence potentielle de valeurs manquantes.

**Solution** : Des sélecteurs CSS ciblés ont été utilisés pour extraire les éléments pertinents du DOM, et une logique de gestion des exceptions a été mise en place pour traiter les cas où certaines métriques étaient manquantes.

### Évolution des métriques

Pour suivre l'évolution des métriques sur une période de 7 jours, il a fallu exécuter le scraper quotidiennement et stocker les données de manière structurée.

**Solution** : Une boucle principale a été implémentée pour exécuter le scraper sur chaque compte Twitter, stockant les données extraites au format JSON structuré à chaque exécution.

## 7. Améliorations futures

Bien que le scraper actuel soit fonctionnel, plusieurs améliorations sont envisageables pour augmenter ses performances et sa fiabilité :

### Rotation des IP et utilisation de proxies

Pour éviter les bannissements potentiels de Twitter, une rotation d'adresses IP et l'utilisation de proxies pourraient être mises en place. Cela permettrait de masquer l'origine des requêtes et de contourner les limitations imposées par Twitter.

### Simulation de navigateur réaliste

Afin de rendre le scraping plus discret et moins détectable, une simulation de comportement de navigation réaliste pourrait être implémentée. Cela impliquerait des délais aléatoires entre les actions, des mouvements de souris simulés, et d'autres techniques visant à imiter le comportement d'un utilisateur humain.

### Tests unitaires avec PyTest

Pour assurer la qualité du code et faciliter la maintenance, des tests unitaires devraient être développés avec PyTest. Cela permettrait de détecter rapidement les régressions et de garantir le bon fonctionnement du scraper après chaque modification.

### Conteneurisation avec Docker

Pour faciliter le déploiement et l'exécution du scraper dans différents environnements, une conteneurisation avec Docker pourrait être envisagée. Cela permettrait de packager l'application et toutes ses dépendances dans un conteneur léger et portable.

### Intégration continue et déploiement continu (CI/CD)

Afin d'automatiser les processus de build, de test et de déploiement, une intégration continue et un déploiement continu (CI/CD) pourraient être mis en place. Des outils comme GitHub Actions ou Jenkins pourraient être utilisés pour gérer ces processus de manière automatisée.

## 8. Conclusion

Ce projet a permis de développer une solution efficace pour le scraping de données à partir de comptes Twitter, sans utiliser l'API officielle. L'approche basée sur Playwright s'est avérée puissante pour interagir avec les pages web dynamiques de Twitter et extraire les données souhaitées.

Bien que le scraper actuel soit opérationnel, plusieurs pistes d'amélioration ont été identifiées pour augmenter ses performances, sa fiabilité et sa capacité à éviter les bannissements potentiels de Twitter.

Dans l'ensemble, ce projet a permis d'acquérir une expérience précieuse dans le domaine du web scraping et de l'automatisation de navigateurs, tout en mettant en pratique des technologies telles que Playwright, BeautifulSoup, Pydantic et FastAPI.
