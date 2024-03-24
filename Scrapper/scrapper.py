import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import csv
from selenium.common.exceptions import NoSuchElementException

# URL = "https://www.google.com/maps/place/Restaurante+Braseria+meson+bernat/@41.3976686,2.1916818,
# 16z/data=!4m8!3m7!1s0x12a4a3177e442bdf:0x8a6fce9d4705cd4e!8m2!3d41.3976686!4d2.1942567!9m1!1b1!16s%2Fg%2F11cls7q7wj
# ?entry=ttu"
DriverLocation = "/Users/fuldeneceugur/PycharmProjects/pubCrawler/Scrapper/Driver/chromedriver"


def get_data(driver, place_name):
    """
    This function retrieves main text and score for each review.
    """
    print('Getting data...')

    more_elements = driver.find_elements("xpath", '//button[@class="w8nwRe kyuRq"]')
    for element in more_elements:
        element.click()
        time.sleep(1)

    translation_buttons = driver.find_elements("xpath", '//button[@class="kyuRq fontTitleSmall WOKzJe"]')
    for button in translation_buttons:
        button.click()
        time.sleep(1)

    elements = driver.find_elements("xpath", '//div[@class="jftiEf fontBodyMedium "]')
    lst_data = []
    for data in elements:
        try:
            text = data.find_element("xpath", './/div[@class="MyEned"]/span[@class="wiI7pd"]').text
        except NoSuchElementException:
            text = "No comment available"

        score = data.find_element("xpath", './/span[@class="kvMYJc"]')
        lst_data.append([place_name, text, score.get_attribute("aria-label")])
    return lst_data


def get_review_count(driver):
    """
    This function retrieves the total number of reviews.
    """
    driver.find_element("xpath", '//button[contains(@aria-label, "Reviews for")]').click()
    time.sleep(3)
    result = driver.find_element("xpath", "//div[@class='jANrlb ']/div[3]").text
    result = result.replace(',', '')
    result = result.split(' ')
    result = result[0].split('\n')
    return int(int(result[0]) / 10) + 1


def scroll_reviews(driver, scroll_count):
    """
    This function scrolls through the reviews based on the scroll count.
    """
    print('Scrolling through reviews...')
    scrollable_div = driver.find_element("xpath", "//div[@class='cVwbnc IlRKB']")
    for _ in range(scroll_count):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(3)


def write_to_csv(data, file_name):
    """
    This function writes the data to a CSV file.
    """
    print('Writing to CSV...')
    df = pd.DataFrame(data, columns=["place_name", "comment", 'rating'])
    df.to_csv(file_name, index=False)


if __name__ == "__main__":
    print('Starting...')
    service = Service(executable_path=r'/Users/fuldeneceugur/PycharmProjects/pubCrawler/Scrapper/Driver/chromedriver')

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # show browser or not
    options.add_argument("--lang=en-US")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

    driver = webdriver.Chrome(service=service, options=options)

    # Read URLs from CSV file
    with open('/Users/fuldeneceugur/PycharmProjects/pubCrawler/Scrapper/place_links.csv', 'r', newline='',
              encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        urls = [row[0] for row in reader]  # Assuming URLs are in the first column
    sc_data = []
    for url in urls:
        driver.get(url)
        time.sleep(5)
        try:
            driver.find_element("xpath",
                                '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button').click()
            time.sleep(5)
        except NoSuchElementException:
            pass
        place_name = driver.find_element("xpath", '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div')
        print(place_name.get_attribute("aria-label"))
        place_name = place_name.get_attribute("aria-label")
        scroll_count = get_review_count(driver)
        if scroll_count > 10:
            scroll_count = 10
        scroll_reviews(driver, scroll_count)

        data = get_data(driver, place_name)
        write_to_csv(data, 'data_ex.csv')
        sc_data.extend(data)

    write_to_csv(sc_data, 'scrapper_data.csv')
    print('Done!')
    driver.quit()
