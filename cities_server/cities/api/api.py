"""frontend langing page"""
import flask
import cities
import spacy
from operator import itemgetter, attrgetter

from cities_server.cities.api import scrape_prices as sp

@cities.app.route('/api/testing/', methods=['GET'])
def get_services():
    """return list of avalible services"""
    input = flask.request.args.get('query')
    # intent names needs to match the json key entry in main.js
    context = {
        "intent": "activities",
        "items": ["fishing"],
        "input": input
    }
    response = flask.jsonify(**context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@cities.app.route("/api/getCity/", methods=['GET'])
def get_cities_by_name():
    connection = cities.model.get_db()
    city_name = flask.request.args.get('city_name')
    activity_name = flask.request.args.get('activity_name')
    city_name = filter_cities(connection, city_name)
    activity_name = filter_single_activity(connection, activity_name)
    print(f"value: {city_name} type: {type(city_name)}")
    print(f"value: {activity_name} type: {type(activity_name)}")
    
    
    curr = connection.execute(
        "SELECT DISTINCT SA.activity_name, SA.weighted_rating FROM Cities C, "
        "Activities A, Specific_Activities SA "
        "WHERE C.city_id = SA.city_id AND SA.activity_id = A.activity_id "
        "AND C.city_name = ? AND A.activity_name = ? ", 
        (city_name, activity_name)
    )
    
    city_activity_id_dict = curr.fetchall()
    print(city_activity_id_dict)
    # TODO sort list above by weighted rating. With best raiting as the first element
    city_activity_id_dict.sort(reverse=True, key = sorting_ratings)
    
    
    
    response = flask.jsonify(city_activity_id_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
    
    # ignore below
        
        
    
    
    
    
@cities.app.route("/api/getCuisines/", methods=['GET'])
def get_cuisines_by_city():
    city_name = flask.request.args.get('city_name')
    connection = cities.model.get_db()
    cur = connection.execute("SELECT DISTINCT CU.cuisine_name "
                             "FROM Cities C "
                             "INNER JOIN City_Restaurants CR "
                             "ON C.city_id = CR.city_id "
                             "INNER JOIN Cuisines CU "
                             "ON CR.cuisine_id = CU.cuisine_id "
                             "WHERE C.city_name = ?", (city_name,))
    results = cur.fetchall()
    cuisines_list = []
    for result in results:
        cuisines_list.append(result["cuisine_name"])
    context = {
        "cuisines_list": cuisines_list
    }
    response = flask.jsonify(**context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@cities.app.route("/api/getRestaurantsByCityCuisines/", methods=['GET'])
def getRestaurantsByCityCuisines(): 
    city_name = flask.request.args.get('city_name')   
    cuisine = flask.request.args.get("cuisines")
    filtered_cuisine = filter_cuisines(cuisine)
    connection = cities.model.get_db()
    cur = connection.execute("SELECT DISTINCT CR.restaurant_name, CR.weighted_rating "
                             "FROM City_Restaurants CR "
                             "INNER JOIN Cities C "
                             "ON CR.city_id = C.city_id "
                             "INNER JOIN Cuisines CU "
                             "ON CR.cuisine_id = CU.cuisine_id "
                             "WHERE CU.cuisine_name = ? AND C.city_name = ? "
                             "ORDER BY CR.weighted_rating ",(filtered_cuisine,city_name,))
    results = cur.fetchall()
    results.sort(reverse = True, key = sorting_ratings)
    context = {
        "restaurants": results
    }
    response = flask.jsonify(**context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@cities.app.route('/recommendCities/', methods=['POST',"OPTIONS"])
def get_recommended_cities():
    """return list of avalible services"""
    if flask.request.method == "OPTIONS": # CORS preflight
        return _build_cors_preflight_response()
    input_json = flask.request.json
    # intent names needs to match the json key entry in main.js
    connection = cities.model.get_db()
    activities_list = input_json['activities']['list']
    act1, act2, act3 = filter_activities(connection,activities_list)
    new_activities = [act1, act2, act3]
    first_set_cities, activities = get10Cities(new_activities)
    input_climate = input_json['climate']['list'][0]
    next_city_filter = []
    filtered_climate = filter_climate(connection,input_climate)
    print(filtered_climate)
    climate = filtered_climate
    print(climate)
    print(type(climate))
    next_city_filter = []
    
    for city in first_set_cities:
        print(type(city))
        cur = connection.execute("SELECT C.city_id, C.city_name "
                                 "FROM Cities C "
                                 "WHERE C.climate = ? AND C.city_name = ? ",
                                 (climate, city["city_name"]))
        # cur = connection.execute("SELECT city_id, city_name "
        #                          "FROM Cities "
        #                          "WHERE city_name = ? ",
        #                          (city))
        result = cur.fetchall()
        print("RESULT1:", result)
        if(len(result) > 0):
            result[0]['num_match_acts'] = city['num_act']
            next_city_filter.append(result[0])
    if(len(next_city_filter) == 0):
        for city in first_set_cities:
            city_object = {'city_id': city['city_id'],'city_name':city['city_name'], 'num_match_acts': city['num_act']}
            next_city_filter.append(city_object)
    print("CLimate Filtered Cities: ", next_city_filter)
    starting_location = input_json['location']['list'][0] + " " + input_json['location']['list'][1]
    preferred_travel_method = input_json['travelMethod']['list'][0]
    travel_method = get_travel_method(preferred_travel_method)
    budget = filter_budget(input_json['budget']['list'][0])
    trip_duration = filter_trip_duration(input_json['tripDuration']['list'][0])
    citiesList = []
    for city in next_city_filter:
        cost = get_expenses_travel_duration(travel_method,starting_location, city['city_name'],trip_duration,budget)
        city_specific_activity_list = get_specific_city_activities_list(city['city_id'])
        cityObject = {"name":city['city_name'],
                      "id":city['city_id'],
                      'num_match_acts': city['num_match_acts'],
                      "travel_method":travel_method,
                      "estimated_cost": cost,
                      "absolute_difference_to_budget": abs(cost - budget),
                      "cityActivityList": city_specific_activity_list}
        citiesList.append(cityObject)
    citiesList =  sorted(citiesList, key=sorting_costs, reverse=False)
    citiesList = sorted(citiesList, key=sorting_num_acts, reverse=True)
    context = {
        "nights":trip_duration,
        "citiesList":citiesList,
        "userBudget":budget,
        "userActivities":activities

    }
    response = flask.jsonify(**context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def _build_cors_preflight_response():
    response = flask.make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
    


def filter_single_activity(con, act_name):
    nlp = spacy.load('en_core_web_md')
    activites_dict = get_all_activites(con)
    print(type(activites_dict))
    act_string = ''
    for entry in activites_dict:
        act_string += entry['activity_name'] + " "
    
    temp_sim_list = []
    input_word = nlp(act_name)
    db_words = nlp(act_string)
    
    for token in db_words:
        temp_sim_list.append(
            {
                "activity": token.text,
                "similarity": input_word.similarity(token)
            }
        )
    temp_sim_list.sort(reverse=True, key=sorting_sims)
    return temp_sim_list[0]['activity']

    

def filter_budget(input):
    words = input.split()
    amount = 1000
    multiplier = 1
    for word in words:
        if word.isnumeric():
            amount = int(word)
        else:
            word = word.lower()
            if (word == "thousand" or word == "grand" or word == "k"):
                multiplier = 1000
    return (amount * multiplier)
            




def filter_trip_duration(string_duration):
    word_list = string_duration.split()
    extracted_num = 1
    multiplier = 1
    is_day = 0
    for word in word_list:
        if word.isnumeric():
            extracted_num = int(word)
        if word.strip().lower() == "week" or word.strip().lower() == "weeks" :
            multiplier = 7
        if word.strip().lower() == "month" or word.strip().lower() == "months":
            multiplier = 30
        if word.strip().lower() == "day" or word.strip().lower() == "days":
            is_day = 1
            
    return (extracted_num - is_day) * multiplier
# @cities.app.route('/api/cities/<int:cityid>', methods=['GET'])
# def city_activities(cityid):
#     """Return a cities and its activities by ID
#     Example:
#     {
#         cityid: 1,
#         city_name: Miami,
#         state: Florida,
#         latitude: 25.7617,
#         longitude: 80.1918,
#         activites: [
#             {
#                 activityid: 1,
#                 activity_name: beach,s
#                 raiting: 5
#             },
#             {
#                 activityid: 2,
#                 activity_name: clubbing
#                 raiting: 5
#             }
#         ]
#     }
#     """
    
    
    
#     #creates connection to database
#     con = cities.model.get_db()
#     city_info = get_city_info_by_id(con, cityid)
#     activity_list = get_city_activities_by_id(con, cityid)
    
#     context = {
#         "cityid": city_info[cityid],
#         "city_name": city_info['city_name'],
#         "state": city_info['state'],
#         "latitude": city_info['latitude'],
#         "longitude": city_info['longitude'],
#         "activites": activity_list
#     }
    
#     return flask.jsonify(**context)
    

def get_city_info_by_id(con, cityid):
    curr = con.execute(
        "SELECT * FROM Cities "
        "WHERE cityid = ? ",
        (cityid, )  
    )
    return curr.fetchone()


def get_city_activities_by_id(con, cityid):
    
    curr = con.execute(
        "SELECT A.activityid, A.activity_name, A.raiting "
        "FROM CityActivites CA, Activities A "
        "WHERE CA.activityid = A.activityid "
        "AND CA.cityid = ? ",
        (cityid, ) 
    )
    
    return curr.fetchall()

    

def getCities(activity_list):
    print(activity_list)
    connection = cities.model.get_db()
    act1, act2, act3 = filter_activities(connection, activity_list)
    print(act1 + " " + act2 + " " + act3 )
    curr = connection.execute(
        "SELECT * FROM ("
        "SELECT C.city_id, C.city_name, COUNT(*) as num_act "
        "FROM Cities C, City_Activities CA, Activities A "
        "WHERE C.city_id = CA.city_id AND CA.activity_id = A.activity_id "
        "AND (A.activity_name = ? OR A.activity_name = ? OR A.activity_name = ?) "
        "GROUP BY C.city_id, C.city_name) "
        "ORDER BY num_act desc LIMIT 3",
        (act1, act2, act3,)
    )  
    
    
    city_dic = curr.fetchall()    
    return city_dic, [act1, act2, act3]

def get10Cities(activity_list):
    print(activity_list)
    connection = cities.model.get_db()
    act1, act2, act3 = filter_activities(connection, activity_list)
    print(act1 + " " + act2 + " " + act3 )
    curr = connection.execute(
        "SELECT * FROM ("
        "SELECT C.city_id, C.city_name, COUNT(*) as num_act "
        "FROM Cities C, City_Activities CA, Activities A "
        "WHERE C.city_id = CA.city_id AND CA.activity_id = A.activity_id "
        "AND (A.activity_name = ? OR A.activity_name = ? OR A.activity_name = ?) "
        "GROUP BY C.city_id, C.city_name) "
        "ORDER BY num_act desc ",
        (act1, act2, act3,)
    )  
    
    
    city_dic = curr.fetchall()
    print(city_dic)    
    return city_dic, [act1, act2, act3]

def filter_activities(con, act_list):
    nlp = spacy.load('en_core_web_md')
    activites_dict = get_all_activites(con)
    print(type(activites_dict))
    act_string = ''
    for entry in activites_dict:
        act_string += entry['activity_name'] + " "
    
    filtered_acts = []
    for usr_act in act_list:
        temp_sim_list = []
        input_word = nlp(usr_act)
        db_words = nlp(act_string)
        
        for token in db_words:
            temp_sim_list.append(
                {
                    "activity": token.text,
                    "similarity": input_word.similarity(token)
                }
            )
        temp_sim_list.sort(reverse=True, key=sorting_sims)
        filtered_acts.append(temp_sim_list[0])
    filtered_acts.sort(reverse=True, key=sorting_sims)
    return filtered_acts[0]['activity'], filtered_acts[1]['activity'], filtered_acts[2]['activity']

def filter_cities(con, usr_city):
    nlp = spacy.load('en_core_web_md')
    cities_dict = get_all_cities(con)
    print(type(cities_dict))
    city_string = ''

    for entry in cities_dict:
        city_string += entry['city_name'] + " "
 
    

    temp_sim_list = []
    input_word = nlp(usr_city)

    print(f"{type(input_word)}")

    db_words = nlp(city_string)
    
    for token in db_words:
        temp_sim_list.append(
            {
                "city": token.text,
                "similarity": input_word.similarity(token)
            }
        )
    temp_sim_list.sort(reverse=True, key=sorting_sims)
    return temp_sim_list[0]['city']

        
def sorting_sims(sim_entry):
    return sim_entry['similarity']   

def sorting_ratings(entry):
    return entry['weighted_rating']  

def sorting_num_acts(entry):
    return entry['num_match_acts']


        
def filter_climate(con, climate):
    print("CLim In:", climate)
    nlp = spacy.load('en_core_web_md')
    climates_dict = get_all_climates(con)
    print(climates_dict)
    temp_sim_list = []
    
    input_word = climate
    input_nlp = nlp(input_word)
    print(input_nlp)
    for entry in climates_dict:
        mapped_climate = entry['climate']
        db_words = nlp(mapped_climate)
        temp_sim_list.append(
            {
                "climate": mapped_climate,
                "similarity": input_nlp.similarity(db_words)
            }
        )
    temp_sim_list.sort(reverse=True, key=sorting_sims)
    print(temp_sim_list)
    return temp_sim_list[0]['climate']

def sorting_sims(sim_entry):
    return sim_entry['similarity']

def sorting_ratings(rating_entry):
    return rating_entry['weighted_rating']   

def sorting_costs(entry):
    return entry["absolute_difference_to_budget"] 

def get_all_activites(con):
    curr = con.execute(
        "SELECT DISTINCT A.activity_name "
        "FROM Activities A"
    )
    return curr.fetchall()

def get_all_cities(con):
    curr = con.execute(
        "SELECT DISTINCT C.city_name "
        "FROM Cities C"
    )
    return curr.fetchall()


def filter_cuisines(cuisine):
    nlp = spacy.load('en_core_web_md')
    all_cuisines = get_all_cuisines()
    cuisines_string = ''
    for entry in all_cuisines:
        cuisines_string += entry + " "
    
    input_word = nlp(cuisine)
    db_words = nlp(cuisines_string)
    temp_sim_list = []
    for token in db_words:
        temp_sim_list.append(
            {
                "cuisine": token.text,
                "similarity": input_word.similarity(token)
            }
        )
    temp_sim_list.sort(reverse=True, key=sorting_sims)
    print(temp_sim_list[0]["cuisine"])
    return temp_sim_list[0]["cuisine"]

def get_all_cuisines():
    connection = cities.model.get_db()
    cur = connection.execute("SELECT cuisine_name "
                             "FROM Cuisines")
    results = cur.fetchall()
    cuisine_list = []
    for result in results:
        cuisine_list.append(result["cuisine_name"])
    return cuisine_list

def get_all_climates(con):
    curr = con.execute(
        "SELECT DISTINCT C.climate "
        "FROM Cities C"
    )
    return curr.fetchall()
    
    
def convert(lst):
    return str(lst).translate(None, '[],\'')

def get_travel_method(usr_travel_method):    
    nlp = spacy.load('en_core_web_md')
    methods_list = ["flight","drive"]
    methods_string = ''
    for entry in methods_list:
        methods_string += entry + " "
    
    temp_sim_list = []
    input_word = nlp(usr_travel_method)
    db_words = nlp(methods_string)
        
    for token in db_words:
        temp_sim_list.append(
            {
                "method": token.text,
                "similarity": input_word.similarity(token)
            }
        )
    temp_sim_list.sort(reverse=True, key=sorting_sims)
    print(temp_sim_list)
    return temp_sim_list[0]['method']

def get_expenses_travel_duration(travel_method, starting_location, city, trip_duration, budget):
    travel_duration = 0
    if(travel_method == 'flight'):
        closest_airport = get_closest_airport(city)
        flight_price = sp.scrape_flight_prices(starting_location,closest_airport)
        print(flight_price)
        #travel_duration = sp.get_flight_duration(starting_location,closest_airport)
        connection = cities.model.get_db()
        cur = connection.execute("SELECT C.Avg_Hotel_Price "
                                    "FROM Cities C "
                                    "WHERE C.City_Name = ?",
                                    (city,))
        results = cur.fetchall()
        hotel_price = results[0]['Avg_Hotel_Price'] * trip_duration
        total_price = hotel_price + flight_price


    elif(travel_method == 'drive'):
        distance = sp.get_distance(starting_location,city) * 2
        
        connection = cities.model.get_db()
        cur = connection.execute("SELECT C.Avg_Hotel_Price "
                                    "FROM Cities C "
                                    "WHERE C.City_Name = ?",
                                    (city,))
        results = cur.fetchall()
        hotel_price = results[0]['Avg_Hotel_Price'] * trip_duration
        total_price = hotel_price + distance
    
        
    return total_price

def get_specific_city_activities_list(city_id):
    connection = cities.model.get_db()
    cur = connection.execute("SELECT A.activity_name, A.activity_id "
                             "FROM Activities A "
                             "INNER JOIN City_Activities CA "
                             "ON A.activity_id = CA.activity_id "
                             "WHERE CA.city_id = ?",(city_id,))
    city_general_activities = cur.fetchall()
    
    activity_list = []
    for activity in city_general_activities:
        activity_list.append(activity['activity_name'])
    
    """
    activity_map = {}
    for activity in city_general_activities:
        general_activity = activity['activity_name']
        connection = cities.model.get_db()
        cur = connection.execute("SELECT SA.activity_name, SA.weighted_rating "
                                "FROM Specific_Activities SA "
                                "WHERE SA.city_id = ? AND SA.activity_id = ?",(city_id,activity['activity_id']))
        results = cur.fetchall()
        print("RESULTS:", results)
        results.sort(reverse=True, key=sorting_ratings)
        activity_map[general_activity] = results
    """
    return activity_list

def get_closest_airport(city_name):
    connection = cities.model.get_db()
    cur = connection.execute("SELECT C.closest_airport "
                            "FROM Cities C "
                            "WHERE C.city_name = ?",(city_name,))
    results = cur.fetchall()
    return results[0]['closest_airport']

if __name__ == '__main__':
    connection = cities.model.get_db()
    print(filter_activities(connection, ["gambling", "beaches", "clubbing", "shopping"]))
    get_all_cuisines()
