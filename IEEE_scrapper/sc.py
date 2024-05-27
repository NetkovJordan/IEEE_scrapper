import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from fake_useragent import UserAgent 
from bs4 import BeautifulSoup

# Prompt the user to enter the URL with query parameters
url_with_query = input("Enter the URL with query parameters: ")

# Define the URL to scrape
url = f'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={url_with_query}'

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure headless is set to True.
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

user_agent = UserAgent().random
chrome_options.add_argument(f"user-agent={user_agent}")

# Set path to chromedriver as per your configuration
webdriver_service = Service('C:\\Users\\jordan.netkov\\Desktop\\chromedriver-win64\\chromedriver.exe')  # Update this path to the location of your chromedriver

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Access the URL
driver.get(url)

# Wait for the JavaScript to load (adjust the wait time as needed)
time.sleep(10)

# Get the page source after waiting for JavaScript to load
html = driver.page_source

# Quit the driver
driver.quit()

#Using BeautifulSoup to parse HTML content, first step is to get all the URLs loaded on the page
soup = BeautifulSoup(html, 'html.parser')
a_tags = soup.find_all('a', class_='fw-bold')

# Store URLs in a list
url_list = []

for a_tag in a_tags:
    url_list.append(a_tag['href'])

# Now we have a list of URLs. We can loop through each URL to scrape additional content
with open('scraped_content.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Authors', 'Abstract', 'Published In', 'Date of Conference', 'Date Added to IEEE Xplore', 'Conference Location']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for url in url_list:
        # Make a request for each URL
        full_url = f"https://ieeexplore.ieee.org{url}"
        print(" \nMaking request to:", full_url)
        
        # Set up Chrome options for the sub-request
        chrome_options_sub = Options()
        chrome_options_sub.add_argument("--headless")  # Ensure headless is set to True.
        chrome_options_sub.add_argument("--disable-gpu")
        chrome_options_sub.add_argument("--no-sandbox")

        user_agent_sub = UserAgent().random
        chrome_options_sub.add_argument(f"user-agent={user_agent_sub}")

        # Choose Chrome Browser for the sub-request
        driver_sub = webdriver.Chrome(service=webdriver_service, options=chrome_options_sub)

        # Access the sub-URL
        driver_sub.get(full_url)

        # Wait for the JavaScript to load (adjust the wait time as needed)
        time.sleep(10)

        # Get the page source after waiting for JavaScript to load
        html_sub = driver_sub.page_source

        # Quit the sub-driver
        driver_sub.quit()

        # Parse the sub-HTML content
        soup_sub = BeautifulSoup(html_sub, 'html.parser')
        
        #1. Extract the title of each article
        title_element = soup_sub.find('h1', class_='document-title text-2xl-md-lh')

        title = title_element.text.strip()

        #Print to validate
        print("Title: ", title)

        # 2. Extract the authors for each article 
        blue_tooltips = soup_sub.find_all('span', class_='blue-tooltip')

        #
        authors_list = []

        # Loop through each 'blue-tooltip' element to extract author name
        for blue_tooltip in blue_tooltips:
            # Find the 'span' element inside 'blue-tooltip' containing author name
            author_span = blue_tooltip.find('span')
            if author_span:
                author = author_span.text.strip()  # Extract the text of the author
                authors_list.append(author)  # Append the author to the authors list

        # Print to validate
        print("Authors:", authors_list)

        # 3. Extract abstract

        abstract_div = soup_sub.find('div', class_='abstract-text row g-0')
        
        abstract = abstract_div.text.strip()

        # Removing extra added text because it it irrelevant

        abstract = abstract.replace("Abstract:", "").strip()

        # Print to validate

        print("Abstract: ", abstract)

        # 4. Extract published in

        publication_div = soup_sub.find('div', class_='u-pb-1 stats-document-abstract-publishedIn')

        publication = publication_div.text.strip()

        # Removing extra added text because it it irrelevant
        publication = publication.replace("Published in:", "").strip()

        # Print to validate
        print("Publication: ", publication)

        # 5. Extract date of conference

        date_conf_div = soup_sub.find('div', class_='u-pb-1 doc-abstract-confdate')

        if date_conf_div:

            date_conf = date_conf_div.text.strip()

            # Removing extra added text because it it irrelevant
            date_conf = date_conf.replace("Date of Conference:", "").strip()

            # Print to validate
            print("Date of Conference: ", date_conf)
        
        else:
            print("This article does not have Date of Conference tag. Continuing with script...")
            date_conf = "Not Available"

        # 6. Extract date added to IEEE
        date_ieee_div = soup_sub.find('div', class_='u-pb-1 doc-abstract-dateadded')
       
        if date_ieee_div:
            date_ieee = date_ieee_div.text.strip()

            # Removing extra added text because it is irrelevant
            date_ieee = date_ieee.replace("Date Added to IEEE Xplore:", "").strip()

            # Print to validate
            print("Date Added to IEEE Xplore: ", date_ieee)
        else:
            print("This article does not have Date Added to IEEE Xplore tag. Continuing with script...")
            date_ieee = "Not Available"

        # 7. Extract conference location
        conf_loc_div = soup_sub.find('div', class_='u-pb-1 doc-abstract-conferenceLoc')

        if conf_loc_div:
            conf_loc = conf_loc_div.text.strip()

            # Removing extra added text because it it irrelevant
            conf_loc = conf_loc.replace("Conference Location:","").strip()
        
            # Print to validate
            print("Conference Location: ", conf_loc)
        else:
            print("This article does not have Conference Location tag. Continuing with script...")
            conf_loc = "Not Available"

        # Write the scraped content to the CSV file
        writer.writerow({
            'Title': title,
            'Authors': authors_list,
            'Abstract': abstract,
            'Published In': publication,
            'Date of Conference': date_conf,
            'Date Added to IEEE Xplore': date_ieee,
            'Conference Location': conf_loc
        })
        
        # Save the HTML content parsed from each URL in a text file
      #  with open(f'html_content_{url.replace("/", "_")}.txt', 'w', encoding='utf-8') as file:
         #   file.write(html_sub)
