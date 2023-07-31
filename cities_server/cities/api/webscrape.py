from bs4 import BeautifulSoup

import requests
import re
import csv
import time
import math
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def update_oa_param(url, offset):
    # Find the index of the string "oa" in the URL
    oa_index = url.find("oa")
    if oa_index == -1:
        # If "oa" is not found in the URL, return the original URL
        return url
    
    # Find the index of the next "-" character after "oa"
    dash_index = url.find("-", oa_index)
    if dash_index == -1:
        # If "-" is not found after "oa", set the end index to the end of the string
        end_index = len(url)
    else:
        # Otherwise, set the end index to the dash index
        end_index = dash_index
    
    # Extract the current offset from the URL and convert it to an integer
    current_offset = int(url[oa_index+2:end_index])
    
    # Calculate the new offset by adding the input offset to the current offset
    new_offset = current_offset + offset
    
    # Build the new URL string with the new offset
    new_url = url[:oa_index+2] + str(new_offset) + url[end_index:]
    
    return new_url


cities = []
urls = []
activities = ["skiing", "hiking", "beaches", "museums", "sightseeing", "clubs", "parks", "shopping",
               "amusements", "zoos", "casinos", "theares", "aquariums"]
sql_activities = open('activities.sql', 'w')
for i in range(len(activities)):
    sql_line = f"INSERT INTO Activities (activity_id, activity_name)"
    sql_line2 = f"VALUES ({i}, '{activities[i]}');"
    sql_activities.write(sql_line + '\n' + sql_line2 + '\n')
sql_activities.close()

with open('scrapelist.csv') as input:
    csv_reader = csv.reader(input, delimiter=',')
    for row in csv_reader:
        cities.append(row[0])
        urls.append(row[1])
    input.close()

sql = open('specific_activites.sql', 'w')

for counter in range(len(urls)):
    original_url = urls[counter]
    current_city = cities[counter]
    names = []
    ratings = []
    number_ratings = []
    activity_types = []
    filtered_activities = []

    print('Starting', current_city)

    for i in range(4):
        offset = i * 30
        url = update_oa_param(original_url, offset)
        print("accessing url:", url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
        }
        timeout = 20  # set the timeout to 10 seconds

        current_city_activities = [0] * 17
        response = requests.get(url, headers=headers, timeout=timeout)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'lxml')
        elements = soup.select('.jemSU[data-automation="WebPresentation_SingleFlexCardSection"]')
        sql_line = f"INSERT INTO Specific_Activities (city_id, activity_id, activity_name, rating, number_ratings, weighted_rating)"
        for element in elements :
            title = re.sub(r'^\d+\.\s', '',element.find('span',{'class': 'title'}).text)
            names.append(title)
            num_rating_element = element.find('span', {'class': 'biGQs _P pZUbB osNWb'})
            if num_rating_element is None:
                # Handle the case where the element is not found
                number_rating = 1  # or some other default value
            else:
                number_rating = int(num_rating_element.text.replace(',', ''))
            number_ratings.append(number_rating)
            rating_element = element.find('svg',{'class': 'UctUV d H0 hzzSG'})
            rating = 0
            if rating_element is None:
                # Handle the case where the element is not found
                rating = 0  # or some other default value
            else:
                rating = rating_element.get('aria-label')
                rating = float(re.search(r'\d+\.\d+', rating).group())
            ratings.append(rating)
            activity_type = element.find('div',{'class': 'biGQs _P pZUbB hmDzD'}).text
            split_activity_types = activity_type.split()
            flag = 0
            sql_line2 = ''
            weighted_rating = rating * math.log(number_rating, 10)
            for index, activity in enumerate(activities):
                if flag == 1:
                    break
                for split_activity_type in split_activity_types:
                    if flag == 1:
                        break
                    if activity == split_activity_type.lower():
                        flag = 1
                        filtered_activities.append(activity)
                        sql_line2 = f'VALUES ({counter}, {index}, "{title}", {rating}, {number_rating}, {weighted_rating});\n'
                        current_city_activities[index] += weighted_rating
            if flag == 0:
                filtered_activities.append('sightseeing')
                sql_line2 = f'VALUES ({counter}, {4}, "{title}", {rating}, {number_rating}, {weighted_rating});\n'
                current_city_activities[4] += weighted_rating
            activity_types.append(activity_type)
            print("#", len(names), "collected")
            sql.write(sql_line + '\n' + sql_line2 + '\n') #end of loop
        time.sleep(0.5)
    sql_line = f"INSERT INTO City_Activities (city_id, activity_id, rating)"
    for index,temp in enumerate(current_city_activities):
        if temp != 0:
            sql_line2 = f"VALUES ({counter}, {index}, {temp});\n"
            sql.write(sql_line + '\n' + sql_line2 + '\n')

    # saves to CSV file
    filename = current_city + ".csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(names)):
            writer.writerow([names[i], ratings[i], number_ratings[i], filtered_activities[i], activity_types[i]])
    file.close()
    print('\033[32mCSV file saved for\033[0m', current_city)
sql.close()
