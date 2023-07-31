# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ActionSetCityInterestedSlot(Action):
    def name(self) -> Text:
        return "set_city_interest_slot"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        interested_city = next(tracker.get_latest_entity_values("GPE"), None)
        
        if not interested_city:
            msg = f"What city are you interested in?"
            dispatcher.utter_message(text=msg)
            return []
        
        dispatcher.utter_message(text=f"We have information on both restaurants and specifc activities in {interested_city}. Which would you like to know more about?")
        return [SlotSet("interested_city", interested_city)]


class ActionGetCityCusines(Action):
    def name(self) -> Text:
        return "action_get_restaurants_info"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        interested_city = tracker.get_slot("interested_city")
        interested_cuisine = next(tracker.get_latest_entity_values('cuisine'), None)
        if not interested_cuisine:
            interested_cuisine = next(tracker.get_latest_entity_values('NORP'), None)
        
        if not interested_city:
            msg = f"Hmm I didn't detect a interested city. What city are you interested in?"
            dispatcher.utter_message(text=msg)
            return []
        if not interested_cuisine:
            msg = f"Hmm I didn't detect any specified cuisine. Here are the cuisine options for {interested_city}:"
            dispatcher.utter_message(text=msg)
            payload = {'city_name': interested_city}
            re = requests.get("http://localhost:8000/api/getCuisines/", params=payload)
            cuisines = re.json()
            msg2 = ''
            for cuisine in cuisines['cuisines_list']:
                msg2 += cuisine + ", "
            dispatcher.utter_message(text=msg2)
            return []
        
        payload = {'city_name': interested_city, 'cuisines': interested_cuisine }
        r = requests.get('http://localhost:8000/api/getRestaurantsByCityCuisines/', params=payload)
        specific_rest = r.json()
        for idx, rest in enumerate(specific_rest['restaurants']):
            msg = f"#{idx + 1} {rest['restaurant_name']}"
            dispatcher.utter_message(text=msg)
        if not len(specific_rest['restaurants']):
            dispatcher.utter_message(text=f"Sorry, we couldn't find any resturants that have {interested_cuisine} in {interested_city}")
            
        return []
    

class ActionGetSpecificActivities(Action):
    
    def name(self) -> Text:
        return "action_get_specific_activities"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        interested_city = tracker.get_slot("interested_city")
        interested_general_activity = next(tracker.get_latest_entity_values('activities'), None)
        
        if not interested_city:
            msg = f"Hmm I didn't detect a interested city. What city are you interested in?"
            dispatcher.utter_message(text=msg)
            return []
        if not interested_general_activity:
            msg = f"Hmm I didn't detect a interested general activity. What general activity are you interested in for {interested_city}?"
            dispatcher.utter_message(text=msg)
            return []
        
        
        payload = {'city_name': interested_city, 'activity_name': interested_general_activity }
        r = requests.get('http://localhost:8000/api/getCity/', params=payload)
        specific_activites = r.json()
        for idx, activity in enumerate(specific_activites):
            msg = f"#{idx} {activity['activity_name']}"
            dispatcher.utter_message(text=msg)
        
            
        
        
        return []


class ValidateVacationDataForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_vacation_data_form"
    
    def validate_liked_activity_1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict               
        ) -> Dict[Text, Any]:

        return {"liked_activity_1": slot_value}

    def validate_liked_activity_2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict               
        ) -> Dict[Text, Any]:
    
        return {"liked_activity_2": slot_value}
    
    def validate_liked_activity_3(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict               
        ) -> Dict[Text, Any]:
        return {"liked_activity_3": slot_value}
    
    def validate_preferred_climate(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict               
        ) -> Dict[Text, Any]:
        return {"preferred_climate": slot_value}
    
    def validate_preferred_travel_method(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict               
        ) -> Dict[Text, Any]:
        return {"preferred_travel_method": slot_value}
    
    def validate_preferred_trip_length(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict               
        ) -> Dict[Text, Any]:
        return {"preferred_trip_length": slot_value}
    
    def validate_preferred_budget(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict               
        ) -> Dict[Text, Any]:
        return {"preferred_budget": slot_value}
    
    def validate_user_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict               
        ) -> Dict[Text, Any]:
        return {"user_city": slot_value}
    
    def validate_user_state(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict               
        ) -> Dict[Text, Any]:
        return {"user_state": slot_value}
    
    

