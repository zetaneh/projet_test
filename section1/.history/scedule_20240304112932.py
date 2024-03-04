import schedule
import time

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