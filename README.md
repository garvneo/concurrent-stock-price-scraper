# Concurrent Stock Scraper

## Description

**This repository contains a set of scrapers designed to run concurrently using multithreading. The scrapers gather stock names from various Wikipedia pages and simultaneously retrieve their prices from Yahoo Finance. The collected data is then stored in a PostgreSQL database for further analysis and usage.**

## Features

- **Concurrent Scraping:** Scrapers run concurrently using multithreading to efficiently collect data from multiple sources simultaneously.
- **Data Collection:** Stock names are extracted from Wikipedia pages, while corresponding prices are fetched from Yahoo Finance.
- **Database Integration:** Scraped data is stored in a PostgreSQL database, allowing for easy access, querying, and analysis.

## Functionality

- **Scraping:** Scrapers extract stock names from designated Wikipedia pages and retrieve their prices from Yahoo Finance in parallel.
- **Concurrency:** Multithreading enables efficient and simultaneous data collection, reducing scraping time.
- **Database Storage:** Scraped data, including stock names and prices, is stored in a PostgreSQL database for future reference.

## Usage

1. Ensure PostgreSQL is installed and running on your system.
2. Run the main script to initiate the concurrent scraping process.
3. Monitor the progress of the scrapers as they gather stock data.
4. Access the PostgreSQL database to analyze the collected data as needed.

## Note

- Make sure to configure the Wikipedia URLs and Yahoo Finance endpoints in the scraper scripts to target the desired stock data.
- Customize the PostgreSQL database connection settings to match your environment.
- Consider optimizing the scrapers further for performance and scalability, depending on the scale of data collection.
