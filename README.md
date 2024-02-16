# Scrapy Spider for Collecting Urdu Stories

## Overview
This Scrapy spider is designed to collect Urdu stories from the website UrduZone while removing HTML tags and non-Urdu words. It scrapes multiple pages of the website to gather a wide range of Urdu stories and stores them in a CSV file for further analysis.

## Objective
The primary objective of this spider is to extract Urdu stories, clean the text, and store them in a structured CSV format. The spider performs the following key tasks:

### 2.1 Story Extraction
- The spider begins its crawl by starting from the UrduZone homepage. It generates URLs for multiple pages (1 to 226) to scrape a large collection of stories.
- On each page, it extracts the links to individual story pages along with their titles using CSS selectors. It follows these links and collects the Urdu story text from paragraphs with the `dir="rtl"` attribute, which signifies right-to-left Urdu text.

### 2.2 Text Cleaning
- The spider cleans the collected text by removing HTML entities, extra spaces, and any HTML tags. It replaces English numbers with Urdu numbers using a predefined mapping dictionary. Non-Urdu characters are removed using regular expressions.

### 2.3 Data Storage
The spider stores the cleaned Urdu stories in a structured CSV file named `urdu_stories.csv` within the Scrapy project directory. Each row of the CSV contains the title and cleaned Urdu story text.

## Approach Used in the Code
The spider follows this approach to accomplish its tasks:
1. The spider begins its crawl by visiting a series of URLs generated based on page numbers from 1 to 226. This allows it to scrape multiple pages of Urdu stories.
2. In the `parse` method, it extracts links to individual story pages and their titles from the main page. CSS selectors are used to locate the elements (`h3 a::attr(href)` and `h3 a::text`), and a loop is created to send requests for each story page.
3. In the `parse_story` method, it extracts the title and Urdu text from an individual story page. CSS selectors are used to locate the Urdu text (`p[dir="rtl"]::text`).
4. The extracted text is then cleaned using the `clean_urdu_text` method. This method takes a text input and performs several cleaning operations: it removes HTML entities, replaces them with spaces, removes extra spaces, and replaces English numbers with their Urdu counterparts using the number mapping dictionary. Finally, non-Urdu characters are removed using a regular expression.

## Additional Information
- **CSV File Configuration:** Configuring the spider to save data in CSV format required changes in the `settings.py` file. Specifically, the following lines were added:
    ```
    FEED_FORMAT = 'csv'
    FEED_URI = 'urdu_stories.csv'
    ```
- **Time-Consuming Scraping:** Scraping the website [UrduZone](https://www.urduzone.net) was a time-consuming process due to the large number of stories and pages.
- **URL Generation:** Initially, the starting URL didn’t contain all the stories. To ensure comprehensive scraping, the starting URL was set as `"https://www.urduzone.net/page/{}/?s"`, and a loop was implemented to navigate through pages until reaching page 226.
- **Mapping Dictionary:** A mapping dictionary was used to convert English numbers to Urdu numbers, enhancing the quality of the text.
