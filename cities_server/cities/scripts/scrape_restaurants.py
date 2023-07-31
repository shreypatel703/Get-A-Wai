# https://github.com/LaskasP/TripAdvisor-Python-Scraper-Restaurants-2021/blob/main/Scraper.py
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import argparse
from selenium.webdriver.common.by import By
import bs4_actions as bs
import re

pathToReviews = "TripReviews.csv"
pathToStoreInfo = "TripStoresInfo.csv"

#webDriver init


def scrapeRestaurantsUrls(tripURLs):
    urls =[]
    for url in tripURLs:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        time.sleep(5)
        page = driver.page_source

        soup = BeautifulSoup(page, 'html.parser')
        categories = soup.find_all('div', class_='jqzUO Gh _T')
        # print(len(categories))
        for category in categories:
            r = category.find('div', class_='POAVt f aMdKg _h _T')
            # print("results:", len(r))
            stores = r.find_all('div', class_='AlmEJ H I HfuLL')
            # print(len(stores))
            for store in stores:
                s = store.find('div', class_='zjwAK Gi _Z')
                unModifiedUrl = str(s.find('a', href=True)['href'])
                # print("Store:", unModifiedUrl)
                urls.append('https://www.tripadvisor.com' + unModifiedUrl)
    return urls



def scrapeRestaurantInfo(url,counter, sql_restaurants, cuisines_list, restaurant_id):
    print(url)
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(5)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    contents = None
    filtered_cuisines = []

    sql_line = f"INSERT INTO City_Restaurants (city_id, cuisine_id, restaurant_id, restaurant_name, rating, number_ratings, weighted_rating)"
    
    # soup = BeautifulSoup(open('soup.html', encoding="utf8"), "html.parser")
    elements = bs.find_elems_by_class(soup, 'div', 'jqzUO Gh _T')
    restaurant_names = []
    for element in elements:
        cards = bs.find_elems_by_class(element, 'div', 'zjwAK Gi _Z')
        for card in cards:
            card_info = bs.find_elem_by_class(card, 'div', 'nyfKs', False)
            title = bs.find_elem_by_class(card, 'a', 'oHGMl')
            # title = title.replace("'", "\'")
            if title in restaurant_names:
                continue
            else:
                restaurant_names.append(title)

            rating = card.find('div',{'class': 'jVDab o W f u w JqMhy'})['aria-label']
            rating = float(re.search(r'\d+\.\d+', rating).group())
            num_rating = card.find('span',{'class': 'yyzcQ'}).text
            if rating and num_rating:
                num_rating = num_rating.replace(',', '')
                weighted_rating = float(rating)* float(num_rating)
            else:
                weighted_rating = -1
            try:
                cuisines = card.find('span',{'class': 'hCoKk o W q'}).text.split(', ')
            except Exception as ex:
                cuisines = []
                pass
            flag = 0
            for index, cuisine in enumerate(cuisines_list):
                if flag == 1:
                    break
                for cuisine_ in cuisines:
                    if flag == 1:
                        break
                    if cuisine == cuisine_.lower():
                        flag = 1
                        filtered_cuisines.append(cuisine)
                        sql_line2 = f"VALUES ({counter}, {index}, {restaurant_id}, \"{title}\", {rating}, {num_rating}, {weighted_rating});\n"
                        sql_restaurants.write(sql_line + '\n' + sql_line2 + '\n')
                        restaurant_id = restaurant_id + 1
            if flag == 0:
                print(cuisines)

                sql_line2 = f"VALUES ({counter}, \"NA\", {restaurant_id},\"{title}\", {rating}, {num_rating}, {weighted_rating});\n"
                sql_restaurants.write(sql_line + '\n' + sql_line2 + '\n')
                restaurant_id = restaurant_id + 1
    return restaurant_id
            # print([title, rating, num_rating, cuisines])

    

def main():
    cuisines_list = ["american", "italian", "korean", "italian", "mexican", "japanese", "indian", "chinese", "thai", "vietnamese", "filipino", "turkish", "french", "german" "israeli", "hawaiian", "cuban", "brazilian", "Venezuelan", "latin", "mediterranean", "caribbean", "international", "cafe", "fast-food", "seafood", "steakhouse", "bar", "pizza", "contemporary"]
    sql_cuisines = open('cuisines.sql', 'w')
    sql_line = f"INSERT INTO Cuisines (cuisine_id, cuisine_name)"
    for i in range(len(cuisines_list)):
        sql_line2 = f"VALUES ({i}, '{cuisines_list[i]}');"
        sql_cuisines.write(sql_line + '\n' + sql_line2 + '\n')
    sql_cuisines.close()

    restaurant_id = 0
    with open('scrapelist.csv') as input:
        csv_reader = csv.reader(input, delimiter=',')
        sql_restaurants = open('specific_restaurants.sql', 'w')
        
        for i, row in enumerate(csv_reader):
            print(row[2])
            restaurant_id = scrapeRestaurantInfo(row[2], i, sql_restaurants, cuisines_list, restaurant_id)
        
        sql_restaurants.close()
        input.close()


    
    # make_sql(output)


if __name__ == "__main__":
    main()
