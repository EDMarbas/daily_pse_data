# daily_pse_data

Automated scraper for capturing daily price changes of all stocks listed on the Philippine Stock Exchange. Ideal for tracking market trends, performing financial analysis, and integrating with data-driven applications.

## Project Overview

This project leverages the Scrapy framework to scrape stock market data from the Philippine Stock Exchange. To handle web pages that rely on JavaScript for dynamic content rendering, Scrapy is integrated with Scrapy-Splash, a tool that enables effective scraping of JavaScript-rendered pages. This combination ensures accurate capture of all relevant data, even from complex web pages.

After scraping, Python's Pandas library is used for data cleaning and manipulation. Pandas offers the tools needed to transform raw, unstructured data into a clean, organized format, making it ready for analysis or integration with other applications. This step is crucial for producing reliable, accurate, and easy-to-use data, whether for financial analysis, web app integration, or other data-driven tasks.
