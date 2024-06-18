import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# Prompt the user to enter the URL with query parameters and the date range
url_with_query = input("Enter the search query: ")
start_year = input("Enter the start year (e.g., 2014): ")
end_year = input("Enter the end year (e.g., 2024): ")
output_file_path = input("Enter the full path for the output CSV file (e.g., C:\\path\\to\\output.csv): ")
max_page_number = int(input("Enter the number of pages to scrape: "))

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-browser-side-navigation")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--headless")

user_agent = UserAgent().random
chrome_options.add_argument(f"user-agent={user_agent}")

# Set path to chromedriver as per your configuration
webdriver_service = Service('C:\\Users\\netko\\OneDrive\\Desktop\\chromedriver-win64\\chromedriver.exe')  # Update this path to the location of your chromedriver

# Function to get page source using Selenium
def get_page_source(url):
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver.get(url)
    try:
        # Wait for the main content to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        time.sleep(2)  # Wait for JavaScript to finish
        html = driver.page_source
    except Exception as e:
        print(f"Error loading page {url}: {e}")
        html = ""
    finally:
        driver.quit()
    return html

# Function to parse articles on a page
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a', class_='fw-bold')
    url_list = [a_tag['href'] for a_tag in a_tags]
    return url_list

# Function to scrape article details
def scrape_article(url, writer):
    full_url = f"https://ieeexplore.ieee.org{url}"
    print(" \nMaking request to:", full_url)
    
    html_sub = get_page_source(full_url)
    soup_sub = BeautifulSoup(html_sub, 'html.parser')

    # Extract the title of each article
    title_element = soup_sub.find('h1', class_='document-title text-2xl-md-lh')
    title = title_element.text.strip() if title_element else "Not Available"
    print("Title: ", title)

    # Extract the authors for each article 
    blue_tooltips = soup_sub.find_all('span', class_='blue-tooltip')
    authors_list = [tooltip.find('span').text.strip() for tooltip in blue_tooltips if tooltip.find('span')]
    print("Authors:", authors_list)

    # Extract abstract
    abstract_div = soup_sub.find('div', class_='abstract-text row g-0')
    abstract = abstract_div.text.strip().replace("Abstract:", "").strip() if abstract_div else "Not Available"
    print("Abstract: ", abstract)

    # Extract published in
    publication_div = soup_sub.find('div', class_='u-pb-1 stats-document-abstract-publishedIn')
    publication = publication_div.text.strip().replace("Published in:", "").strip() if publication_div else "Not Available"
    print("Publication: ", publication)

    # Extract date of conference
    date_conf_div = soup_sub.find('div', class_='u-pb-1 doc-abstract-confdate')
    date_conf = date_conf_div.text.strip().replace("Date of Conference:", "").strip() if date_conf_div else "Not Available"
    print("Date of Conference: ", date_conf)

    # Extract date added to IEEE
    date_ieee_div = soup_sub.find('div', class_='u-pb-1 doc-abstract-dateadded')
    date_ieee = date_ieee_div.text.strip().replace("Date Added to IEEE Xplore:", "").strip() if date_ieee_div else "Not Available"
    print("Date Added to IEEE Xplore: ", date_ieee)

    # Extract conference location
    conf_loc_div = soup_sub.find('div', class_='u-pb-1 doc-abstract-conferenceLoc')
    conf_loc = conf_loc_div.text.strip().replace("Conference Location:", "").strip() if conf_loc_div else "Not Available"
    print("Conference Location: ", conf_loc)

    # Write the scraped content to the CSV file
    writer.writerow({
        'Title': title,
        'Authors': authors_list,
        'Abstract': abstract,
        'Published In': publication,
        'Date of Conference': date_conf,
        'Date Added to IEEE Xplore': date_ieee,
        'Conference Location': conf_loc,
        'Document URL': full_url
    })

# Open CSV file for writing
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Authors', 'Abstract', 'Published In', 'Date of Conference', 'Date Added to IEEE Xplore', 'Conference Location', 'Document URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each page and scrape articles
    for page_number in range(1, max_page_number + 1):
        page_url = f'https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&queryText={url_with_query}&ranges={start_year}_{end_year}_Year&pageNumber={page_number}'
        print(f"Scraping page {page_number}: {page_url}")
        
        page_html = get_page_source(page_url)
        article_urls = parse_page(page_html)
        
        for article_url in article_urls:
            scrape_article(article_url, writer)

print("Scraping completed.")
