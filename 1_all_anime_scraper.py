from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

anime_list = {}

url = 'https://www.crunchyroll.com/videos/alphabetical'


def print_anime_info(anime: dict):
    # iterate over the dictionary
    for key, value in anime.items():
        print(key + ' || ' + value)


def save_to_file(anime: dict):
    with open('anime.csv', 'w') as f:
        f.write('title,url' + '\n')

        for key, value in anime.items():
            f.write(key + ',' + value + '\n')


def scrape_anime():
    # Set up the webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--user-agent=MyUserAgent')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # Request the HTML page and wait for it to load
    driver.get(url)
    wait = WebDriverWait(driver, 180)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'erc-browse')))

    while True:
        driver.execute_script("window.scrollBy(0, 200)")
        # wait for the page to load
        time.sleep(0.1)

        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'horizontal-card-static__link--q268E')))

        elems = driver.find_element(
            By.XPATH, '//a[@class="horizontal-card-static__link--q268E"]')

        title = elems.get_attribute('title')
        href = elems.get_attribute('href')

        anime_list[title] = href

        # check if no more scrolling is possible
        if driver.execute_script("return document.body.scrollHeight") == driver.execute_script(
                "return window.innerHeight + window.scrollY"):
            break

    print('finished scraping')

    # Close the webdriver
    driver.close()


scrape_anime()

# print_anime_info(anime)

# save_to_file(anime_list)
