# Web Scraping and Data Processing Project
**Ayoub Abraich**
This repository contains a Python project focused on web scraping and data processing. The project includes the following components:

1. Web Scraper
The web_scraper.py module contains a Python class called WebScraper that can extract data from various websites related to bank products, such as savings accounts and sustainable development accounts. The scraper utilizes the requests, BeautifulSoup, and urllib.parse libraries to retrieve and parse HTML content from web pages.

2. FastAPI Web Service
The main.py module implements a RESTful API using the FastAPI framework. The API provides endpoints for scraping and storing data from bank websites in a RavenDB database. It also allows retrieving the scraped data and executing the scraping process for specific URLs or all predefined URLs.

3. NoSQL Database Integration
This project uses RavenDB as the NoSQL database for storing the scraped data. RavenDB is a document-oriented database suitable for storing semi-structured data like the one obtained from web scraping.

4. Twitter Scraper
The twitter_scraper.py module contains a scraper built with Playwright that can extract data from specific Twitter accounts, including tweet content, account metrics, and tweet metrics. The scraper follows the evolution of these metrics over a 7-day period and stores the data in a structured JSON format.

The Twitter scraper also includes a FastAPI integration, providing endpoints to retrieve user information, tweets, and tweet details.
