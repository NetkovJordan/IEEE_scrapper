# IEEE Xplore Web Scraper

This project is an automated web scraper designed to extract research paper details from IEEE Xplore. The tool utilizes Selenium for handling dynamic content loading and BeautifulSoup for HTML parsing. This combination ensures efficient and accurate data extraction from web pages that rely heavily on JavaScript.

## Features

Users simply input a URL with query parameters, and the script retrieves the corresponding page, extracts URLs of individual research papers, and gathers key details including:

- **Title**
- **Authors**
- **Abstract**
- **Published In**
- **Date of Conference**
- **Date Added to IEEE Xplore**
- **Conference Location**

The collected data is neatly organized and saved into a CSV file, facilitating efficient and structured data analysis. 

## Exception Handling

The scraper includes robust exception handling to manage missing elements and other abnormalities gracefully. For instance, if a particular data block is missing, the script assigns a value of "Not Available" to ensure the CSV file remains structured and complete. This enhances the reliability of the data extraction process.

## Development and Testing

To run this scraper, you need the Chrome WebDriver that matches your local Chrome browser version. You can download the appropriate version from [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/). Ensure that the WebDriver version aligns with your installed Chrome browser to avoid compatibility issues.
My current driver (Subject to change): 125.0.6422.113

Direct link to download executable file:
https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.113/win64/chromedriver-win64.zip

## Why Selenium?

Selenium is used in this project to handle dynamic web content that relies on JavaScript. Many modern web pages, including IEEE Xplore, load content dynamically, which requires a tool capable of interacting with the web page as a real user would. Selenium provides this capability, allowing the scraper to wait for the necessary elements to load before extracting data.

## How It Works

1. **User Input**: Enter a URL with query parameters.
2. **Dynamic Content Handling**: Selenium accesses the URL and waits for the JavaScript content to load.
3. **HTML Parsing**: BeautifulSoup parses the loaded HTML content.
4. **Data Extraction**: The script extracts relevant details from each research paper's page.
5. **Exception Handling**: Missing elements are managed by assigning "Not Available" to maintain data integrity.
6. **CSV Output**: The extracted data is saved into a CSV file for easy analysis.

This tool is ideal for researchers and analysts who need to collect large volumes of structured data from IEEE Xplore efficiently.


