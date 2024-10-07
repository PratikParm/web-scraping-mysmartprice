from src.basic_scraper import scrape_earbuds
from src.specs_scraper import scrape_specs

if __name__ == '__main__':
    scrape_earbuds()  # Step 1: Scrape the basic data
    scrape_specs()    # Step 2: Scrape the detailed specifications
