import csv
import time
import os
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def scrape_anime():
    data = []
    ratings = []

    ratings_cols = 'title,rating,rating_count'

    last_line = False

    if os.path.exists('ratings.csv'):
        with open('ratings.csv', 'r') as f:
            for line in f:
                if line.strip() and line.strip() != ratings_cols:
                    last_line = line
    else:
        with open('ratings.csv', 'w') as csv_file:
            csv_file.write(ratings_cols + '\n')

    with open('anime.csv', 'r', encoding='utf-8') as csv_file:
        catched_up = False

        for line in csv_file.readlines():
            if line.__contains__('title,url'):
                continue

            if last_line and line.__contains__(last_line.split(',')[0]):
                catched_up = True
                continue

            if catched_up or not last_line:
                title, url = line.rsplit(',', 1)

                title = title.strip()
                url = url.strip()

                data.append([title, url])

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--user-agent=MyUserAgent')
    driver = webdriver.Chrome(options=chrome_options)

    for title, url in data:
        driver.get(url)
        wait = WebDriverWait(driver, 180)

        try:
            driver.find_element(By.CLASS_NAME, "error-text")
        except NoSuchElementException:
            pass
        else:
            print('error-text class found...resetting')
            raise Exception("Error text element found")

        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                       'content-image__figure--7vume')))
        except NoSuchElementException or TimeoutError:
            time.sleep(3)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME,
                                                       'content-image__figure--7vume')))
            pass

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

        with open('ratings.csv', 'a') as csv_file:
            csv_file.write(title + ',' + rating + ',' + rating_count + '\n')

    driver.quit()


# if __name__ == '__main__':
#     keep_going = True
#
#     while keep_going:
#         try:
#             scrape_anime()
#             keep_going = False
#         except Exception as e:
#             print('error...')
#             print(e)
