# daily_pse_data

Automated scraper for capturing daily price changes of all stocks listed on the Philippine Stock Exchange. Ideal for tracking market trends, performing financial analysis, and integrating with data-driven applications.

## Project Overview

This project leverages the powerful Scrapy framework to scrape stock market data from the Philippine Stock Exchange. Since many web pages rely on JavaScript to render content dynamically, we integrate Scrapy with Scrapy-Splash, an essential tool that enables Scrapy to handle JavaScript-rendered pages effectively. This combination ensures that we capture all the relevant data accurately, even from the most complex web pages.

Once the data is scraped, we employ Python's Pandas library for robust data cleaning and manipulation. Pandas provides the necessary tools to transform raw, unstructured data into a clean, well-organized format, ready for analysis or integration with other applications. This step is crucial for ensuring that the final output is reliable, accurate, and easy to work with, whether for financial analysis, web app integration, or other data-driven tasks.
