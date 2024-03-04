import schedule
import time
from twitter_scraper import TwitterScraper

accounts = [
    "https://twitter.com/RevolutApp",
    "https://twitter.com/mabanque_bnpp?lang=fr",
    "https://twitter.com/Leocare_Assure"
]

# Function to be executed at regular intervals
def run_scraper():
    # Insert your scraper code here
    scraper = TwitterScraper(accounts)
    #you shoul 
    scraper.run()

# Schedule the task
schedule.every(15).minutes.do(run_scraper) # Execute the scraper every 15 minutes

# Loop to continuously run the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
