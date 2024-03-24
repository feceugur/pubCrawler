import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import csv

URL = "https://www.google.com/maps/@41.3903651,2.1941609,15z?entry=ttu"
DriverLocation = "/Users/fuldeneceugur/PycharmProjects/pubCrawler/Scrapper/Driver/chromedriver"


def scroll_reviews(driver, scroll_count):
    """
    This function scrolls through the reviews based on the scroll count.
    """
    print('Scrolling through reviews...')
    scrollable_div = driver.find_element("xpath", "//div[@class='L1xEbb']")
    for _ in range(scroll_count):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(3)


def get_data(driver):
    """
    This function retrieves main text and score for each review.
    """
    print('Getting data...')

    place_links = []
    links = driver.find_elements("xpath", './/div[@class="Nv2PK THOPZb CpccDe "]/a')
    for link in links:
        place_links.append(link.get_attribute("href"))
    print(place_links)
    return place_links


def select_restaurants(driver):
    """
    This function selects the restaurant from the list of search results.
    """
    print('Selecting restaurant...')
    select_rest = driver.find_elements("xpath", '//button[@class="e2moi "][@aria-label="Restaurantes"]')
    for element in select_rest:
        element.click()
        time.sleep(1)


def write_to_csv(data):
    """
    This function writes the data to a CSV file.
    """
    print('Writing to CSV...')
    df = pd.DataFrame(data, columns=["link"])
    df.to_csv('place_links.csv', index=False)


if __name__ == "__main__":
    print('Starting...')
    service = Service(executable_path=r'/Users/fuldeneceugur/PycharmProjects/pubCrawler/Scrapper/Driver/chromedriver')

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # show browser or not
    options.add_argument("--lang=en-US")
    # options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)
    time.sleep(10)

    select_restaurants(driver)
    scroll_reviews(driver, 45)
    place_links = get_data(driver)
    write_to_csv(place_links)
