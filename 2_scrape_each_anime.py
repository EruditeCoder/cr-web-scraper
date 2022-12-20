import csv
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def scrape_anime():
    # Open the CSV file and read the titles and URLs
    with open('anime.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        data = list(reader)

    ratings = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--user-agent=MyUserAgent')
    driver = webdriver.Chrome(options=chrome_options)

    for title, url in data:
        driver.get(url)
        wait = WebDriverWait(driver, 180)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                   'content-image__figure--7vume')))

        try:
            mature_info_wrapper = driver.find_element(By.CLASS_NAME, 'mature-info-wrapper')
            button = mature_info_wrapper.find_element(By.CLASS_NAME, 'button--is-type-one-weak--KLvCX')
            button.click()
            driver.execute_script("window.scrollBy(0, 300)")
        except NoSuchElementException:
            pass

        wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                   'star-rating-average-data__label--TdvQs')))

        rating_element = driver.find_element(By.XPATH,
                                             '//span[@class="text--gq6o- text--is-heavy--2YygX text--is-m--pqiL- '
                                             'star-rating-average-data__label--TdvQs"]')

        print(rating_element.text)
        rating_text = rating_element.text

        if rating_text.__contains__('—'):
            time.sleep(1.3)
            rating_element = driver.find_element(By.XPATH,
                                                 '//span[@class="text--gq6o- text--is-heavy--2YygX '
                                                 'text--is-m--pqiL- '
                                                 'star-rating-average-data__label--TdvQs"]')
            rating_text = rating_element.text

        rating = rating_text.split(' ')[0]
        rating_count = rating_text.split('(')[1][:-1]

        print("{}: {} ({})".format(title, rating, rating_count))

        ratings.append((title, rating, rating_count))

    with open('ratings.csv', 'w') as csv_file:
        csv_file.write('title,rating,rating_count' + '\n')
        writer = csv.writer(csv_file)
        writer.writerows(ratings)

    driver.quit()


if __name__ == '__main__':
    scrape_anime()
