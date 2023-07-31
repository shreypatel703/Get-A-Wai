import csv
import time
import argparse
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import logging as log

def scrape_flight_prices(location1,location2):
    URL = "https://www.google.com/search?q=" + location1 + "+to+" + location2 + "+flights&rlz=1C1CHBD_enUS889US891&oq=ann+a&aqs=chrome.0.69i59j46i131i433i512j0i131i433i512l3j69i61j69i60l2.1418j1j7&sourceid=chrome&ie=UTF-8"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(URL)
    time.sleep(5)

    button = driver.find_element(By.CSS_SELECTOR, ".S8ee5")
    driver.execute_script("arguments[0].click();", button)
    button2 = driver.find_element(By.CSS_SELECTOR, ".rfmBib")
    driver.execute_script("arguments[0].click();", button2)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    flight_price_string = soup.select(".NtS4zd")[0].text
    first_index = flight_price_string.find('–')
    second_index = flight_price_string.find('.')
    return int(flight_price_string[first_index + 1:second_index])

print(scrape_flight_prices("San Francisco", "Ann Arbor"))
