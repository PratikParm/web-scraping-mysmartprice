import os
import logging
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from utils.scraper_utils import scroll_and_load_more

# Set up logging
log_dir = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'specs_scraping.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_specs():
    # Load the basic data CSV
    basic_df = pd.read_csv('../data/basic_data.csv')

    # Set up Selenium with Edge
    driver = webdriver.Edge()
    details = []

    try:
        for link in basic_df['Link']:
            driver.get(link)

            # Wait for the page to load
            wait = WebDriverWait(driver, 2)

            scroll_and_load_more(driver, wait)

            # Wait a moment to ensure the last batch of data is fully loaded
            time.sleep(2)

            # Get the page source and parse it with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            specs_dict = {}

            for spec in soup.find_all('div', class_='detls-view w-f-100'):
                spec_name = spec.find('div', class_='specs_nme flt-l pos-rel pos-after').text.strip()
                spec_value = spec.find('div', class_='specs_dtls flt-l pos-rel').text.strip()
                specs_dict[spec_name] = spec_value

            details.append(specs_dict)

            logging.info(f"Scraped specs for {link}")

    except Exception as e:
        logging.error(f"Error occurred while scraping specs: {str(e)}")
    finally:
        # Close the browser
        driver.quit()

    # Create a DataFrame for the specs and merge it with the basic data
    specs_df = pd.DataFrame(details)
    final_df = pd.concat([basic_df, specs_df], axis=1)

    # Define the output directory and create it if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(output_dir, exist_ok=True)

    # Save the final data to a CSV file
    final_df.to_csv(os.path.join(output_dir, 'final_data.csv'), index=False)
    logging.info("Specifications scraping completed successfully. Data saved to 'final_data.csv'.")

if __name__ == "__main__":
    scrape_specs()
