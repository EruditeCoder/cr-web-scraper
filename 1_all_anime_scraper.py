from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

# Set up the webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--user-agent=MyUserAgent')
driver = webdriver.Chrome(chrome_options=chrome_options)

# Request the HTML page and wait for it to load
driver.get('https://www.crunchyroll.com/videos/alphabetical')
wait = WebDriverWait(driver, 180)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'erc-browse')))

cards = []

while True:
  driver.execute_script("window.scrollBy(0, 140);")
  # wait for the page to load
  time.sleep(2)

  wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'horizontal-card-static__link--q268E')))
  elems = driver.find_element(By.XPATH, '//a[@class="horizontal-card-static__link--q268E"]')
  
  # obtain all attributes of elems
  print(elems.get_attribute('title'))
  print(elems.get_attribute('href'))

# Print the number of horizontal cards found
print(f'Found {len(horizontal_cards)} horizontal cards')

# Close the webdriver
driver.close()