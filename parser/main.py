from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests


service = Service(executable_path='chromedriver.exe')
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=service, options=options)
with open('links.txt', 'r') as file:
    links = file.readlines()
    try:
        for link in links:
            driver.get(link)
            crop_type = link.split('=')[-1].strip()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'images'))
            )

            images_div = driver.find_element(By.CLASS_NAME, 'images')
            items = images_div.find_elements(By.CLASS_NAME, 'item')

            if not os.path.exists('downloaded_images'):
                os.makedirs('downloaded_images')

            for index, item in enumerate(items):
                img_tag = item.find_element(By.TAG_NAME, 'img')
                img_url = img_tag.get_attribute('src')
                description = item.find_element(By.TAG_NAME, 'div').text

                img_response = requests.get(img_url)

                if not os.path.exists(f'downloaded_images/{crop_type}'):
                    os.makedirs(f'downloaded_images/{crop_type}')

                filename = f'downloaded_images/{crop_type}/{description}.jpg'
                with open(filename, 'wb') as f:
                    f.write(img_response.content)

                print(f'Saved {filename} - Description: {description}')

    finally:
        driver.quit()
