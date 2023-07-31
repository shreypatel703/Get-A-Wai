from bs4 import BeautifulSoup

import requests
import re
import math

def scrape_flight_prices(location1,location2):
    URL = "https://www.google.com/search?q=" + location1 + "+to+" + location2 + "+flights"
    print(URL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
    }
    timeout = 10
    response = requests.get(URL, headers=headers, timeout=timeout)

    
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.select('div.BNeawe.DwrKqd.s3v9rd.AP7Wnd')
    prices = []
    for element in elements:
        price = element.text.replace('$', '')
        if price.isdigit():
            prices.append(int(price))
    average = 0
    for price in prices:
        average += price / len(prices)
    return math.ceil(average)


def get_distance(location1,location2):
    URL = "https://www.google.com/search?q=distance+between+" + location1 + "+and+" + location2
    print(URL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
    }
    timeout = 10
    response = requests.get(URL, headers=headers, timeout=timeout)

    
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    #BNeawe deIvCb AP7Wnd
    element = soup.select_one('div.BNeawe.deIvCb.AP7Wnd')
    text = element.text
    pattern = r'\d{1,3}(?:,\d{3})*\.\d+'
    matches = re.findall(pattern, text)
    if matches:
        distance = float(matches[0].replace(',', ''))
        return(math.ceil(distance*4.011/24.2))
    else:
        return(0)
