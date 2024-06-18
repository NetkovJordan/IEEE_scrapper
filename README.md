# IEEE Article Scraper

## Overview

This script is designed to scrape article details from the IEEE Xplore Digital Library based on user-defined search queries and date ranges. The collected data is saved into a CSV file, which includes detailed information about each article such as title, authors, abstract, publication details, and more.

## Features

- **Dynamic Search Query Input**: Users can input the search query and the date range for the articles to be scraped.
- **Concurrency Support**: Optimized for performance using threading to handle multiple article requests simultaneously.
- **Headless Browser Operation**: Utilizes Chrome in headless mode to avoid UI overhead, speeding up the scraping process.

## Installation

Ensure you have the following Python packages installed:

- `selenium`
- `beautifulsoup4`
- `fake_useragent`
- `concurrent.futures`

You can install them using pip:

```bash
pip install selenium beautifulsoup4 fake-useragent concurrent.futures
```
## Script Explanation
### Input Prompts
The script prompts the user to enter the following details:

- **Search Query**: Keywords for searching articles.
- **Start Year**: Beginning year of the search range.
- **End Year**: Ending year of the search range.
- **Output File Path**: Path where the output CSV file will be saved.
- **Max Page Number**: Number of pages to scrape.
## Setup Chrome Options
### The script sets up Chrome options to ensure:

- No extensions, plugins, or unnecessary browser features are enabled.
- Chrome runs in headless mode to improve performance.
- A random user agent is used to mimic a real browser.

```python
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-browser-side-navigation")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--headless")
```
## Functions
```python 
get_page_source(url)
```
1. Opens the URL using Selenium, waits for the page to load, and returns the HTML content.
2. Exception Handling: Catches errors if the page fails to load.
``` python
parse_page(html)
```
3. Parses the HTML to extract article URLs from the page.
```python
scrape_article(url, writer)
```
4. Extracts detailed information from each article's page, such as title, authors, abstract, publication details, and conference location.
Writes the extracted data to the CSV file.

## Data Retrieved
### The script collects and saves the following data for each article:

- **Title**: The title of the article.
- **Authors**: List of authors.
- **Abstract**: The abstract of the article.
- **Published In**: The journal or conference name.
- **Date of Conference**: The date when the conference took place.
- **Date Added to IEEE Xplore**: The date when the article was added to IEEE Xplore.
- **Conference Location**: The location of the conference.
- **Document URL**: The direct URL to the article.

## Performance Enhancement

To enhance the script's performance, several optimizations were made to handle requests more efficiently. Initially, the script executed requests sequentially, which led to high CPU utilization, often reaching 100%, as Chrome WebDriver sessions were queued up and not released promptly. To mitigate this, Chrome options were fine-tuned to disable unnecessary browser features, ensuring smoother operation in headless mode. The get_page_source function was also improved by adding exception handling to manage errors if a page fails to load, thus preventing the script from crashing and allowing it to continue processing other requests. These adjustments helped streamline the script's execution, reducing processing time and minimizing resource consumption. As of now, CPU utilization is max 45% per request and diminishes after request ends.

## Example Input:
``` Enter the search query: AI helping people
Enter the start year (e.g., 2014): 2020
Enter the end year (e.g., 2024): 2021
Enter the full path for the output CSV file (e.g., C:\path\to\output.csv): C:\\Users\\netko\\OneDrive\\Desktop\\IEEE_Output_Dir\\ai_helping_people.csv
Enter the number of pages to scrape: 6
```

## Example Output Data

| Title                                                      | Authors                                                                                                              | Abstract                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Published In                                              | Date of Conference | Date Added to IEEE Xplore | Conference Location | Document URL                                                                                                      |
|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|--------------------|--------------------------|---------------------|---------------------------------------------------------------------------------------------------------------------|
| Jollity Chatbot- A contextual AI Assistant                  | ['Kanakamedala Deepika', 'Veeranki Tilekya', 'Jatroth Mamatha', 'T Subetha']                                             | Chatbot is a software application that can stimulate a conversation via text, instead of direct contact with a live human through messaging applications, websites and mobile applications. Chatbot applications help to make interactions between people and services by enhancing the customer experience. Chatbot is widely used in the areas of food ordering, ecommerce and transportation, etc. Practically it is not possible to find a permanent companion to make us happy all the time. Hence, this paper has planned to design a jollity chatbot to talk with the human users and make sure that it entertains and give suggestion and motivation in tough times. The jollity chatbot is implemented in Rasa, an open -source conversational AI framework and it is easy to customize. The proposed method has added 12 intents with each more than 8 text examples constituting a total of 100 input samples in nlu.md and their response in domain.yml. The flow of interactions is given in stories.md. The jollity chatbot is deployed in Telegram using ngrok and the server URL details and the access token are given in the credentials.yml. The system is experimented with various evaluation measures like accuracy of the intents, accuracy of the stories and the confusion matrix to shows that the proposed jollity chatbot system is more robust and can identify the user intents appropriately.                                                                                                                                                                                                  | 2020 Third International Conference on Smart Systems and Inventive Technology (ICSSIT) | 20-22 August 2020 | 6-Oct-20                   | Tirunelveli, India    | [Link](https://ieeexplore.ieee.org/document/9214076/)                                                       |
| Application of Artificial Intelligence in Electronic Product Design | ['Beibei Li']                                                                                                          | In recent years, computer AI technology has been used in various aspects and has been noticed by many research electronics products. Many of these researchers have experts linking and combine computer AI technology and electronic design. Therefore, it enables many researchers to further study the more advanced development path of computer AI technology in other aspects. It further studies the characteristics and significance of computer AI technology in electronic product design and proposes the difficulty of computer AI application to electronic product design. In addition, this paper also points out the relevant ways and strategies for the design of electronic products with the help of AI. This can also more enrich the application scope of computer AI technology, and computer AI technology has gradually become the foundation of electronic product design research.                                                                                                                                                                                                                                                                                                                                                                          | 2021 2nd International Conference on Artificial Intelligence and Education (ICAIE) | 18-20 June 2021   | 15-Sep-21                | Dali, China          | [Link](https://ieeexplore.ieee.org/document/9534616/)                                                       |
| Applying Faster R-CNN in Extremely Low-Resolution Thermal Images for People Detection | ['Diego M. Jiménez-Bravo', 'Pierre Masala Mutombo', 'Bart Braem', 'Johann M. Marquez-Barja']                          | In today's cities, it is increasingly normal to see different systems based on Artificial Intelligence (AI) that help citizens and government institutions in their daily lives. This is possible thanks to the Internet of Things (IoT). In this paper we present a solution using low-resolution thermal sensors in combination of deep learning to detect people in the images generated by those sensors. To verify whether the deep learning techniques are appropriate for this type of images of such low resolution, we have implement a Faster Region-Convolutional Neural Network. The results obtained are hopeful and undoubtedly encourage to continue improving this research line. With a perception of 72.85% and given the complexity of the problem presented we consider the results obtained to be highly satisfactory and it encourages us to continue improving the work presented in this article. | 2020 IEEE/ACM 24th International Symposium on Distributed Simulation and Real Time Applications (DS-RT) | 14-16 September 2020 | 6-Oct-20                   | Prague, Czech Republic | [Link](https://ieeexplore.ieee.org/document/9213609/)                                                        |
|

### Reponse time: 25 mins, 20 secs.
Entries: 6 X 25 = 150
