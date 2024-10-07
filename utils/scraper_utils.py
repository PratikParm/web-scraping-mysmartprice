from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def scroll_and_load_more(driver, wait=None, load_wait_time=5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        try:
            load_more_button = driver.find_element(By.XPATH, '//span[contains(@class, "js-load-more-prdcts")]')
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(load_wait_time)
        except (TimeoutException, NoSuchElementException):
            break

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
