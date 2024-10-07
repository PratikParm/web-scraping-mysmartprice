import os
import logging
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils.scraper_utils import scroll_and_load_more

# Set up logging
log_dir = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'scraping.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_earbuds():
    # Set up Selenium with Edge
    driver = webdriver.Edge()  # Ensure you have the driver in your PATH
    url = "https://www.mysmartprice.com/audio/pricelist/earbuds-price-list-in-india.html"

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        # Run the function to scroll and load more results
        scroll_and_load_more(driver, wait)

        # Wait a moment to ensure the last batch of data is fully loaded
        time.sleep(2)

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        earbuds_list = []

        # Extract earbuds data
        for card in soup.find_all('div', class_="spec_card white_bg w-100 br-all br8 d-flex j-c pos-rel"):
            name = card.find('h2', class_='txt-heading')
            price = card.find('span', class_='price')
            rating = card.find('p', class_='r_value')
            specs = [li.text.strip() for li in card.find_all('li', class_='pos-rel trunk pos-after spec_bullt')]
            link = card.find('a', class_='v_a_t blk_heading ga_event_cls')

            if name and price and rating:
                earbuds_list.append({
                    'Name': name.text.strip(),
                    'Price': price.text.strip(),
                    'Rating': rating.text.strip()[-5:-2],
                    'Specifications': ', '.join(specs),
                    'Link': link['href'] if link else None
                })

        for card in soup.find_all('div', class_='spec_card white_bg w-100 br-all br8 d-flex j-c pos-rel m-t-top'):
            name = card.find('h2', class_='txt-heading')
            price = card.find('span', class_='price')
            rating = card.find('p', class_='r_value')
            specs = [li.text.strip() for li in card.find_all('li', class_='pos-rel trunk pos-after spec_bullt')]
            link = card.find('a', class_='v_a_t blk_heading ga_event_cls')

            if name and price and rating:
                earbuds_list.append({
                    'Name': name.text.strip(),
                    'Price': price.text.strip(),
                    'Rating': rating.text.strip()[-5:-2],
                    'Specifications': ', '.join(specs),  # Join all specs into a single string
                    'Link': link['href']
                })

        # Define the data directory and create it if it doesn't exist
        data_dir = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(data_dir, exist_ok=True)

        # Save the data to a CSV file
        earbuds_df = pd.DataFrame(earbuds_list)
        earbuds_df.to_csv(os.path.join(data_dir, 'basic_data.csv'), index=False)
        logging.info("Scraping completed successfully. Data saved to 'basic_data.csv'.")

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    scrape_earbuds()
