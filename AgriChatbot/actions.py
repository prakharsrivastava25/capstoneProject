# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
import requests
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from flask import Flask, request
import requests
import json

class WeatherForm(FormAction):
    """Collects details run the weather api"""

    def name(self):
        return "weather_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "area",
            "dayshence",
            ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return{
            "area":self.from_text(),
            "dayshence":self.from_text()
        }
    
    def apply_to(self, tracker) -> None:
        tracker._reset_slots()

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
    
        area = tracker.get_slot('area')
        print(area)
        daysHence = int(tracker.get_slot('dayshence'))
        print(daysHence)
        url='http://api.openweathermap.org/data/2.5/forecast?appid=63fb79c416f18764ec7af193f1b6480c&units=metric&q={}'.format(area)
        res = requests.get(url)
        data = res.json()
        obj={}
        if(data['cod'] != '404'):
            timestampForDaysHence = int(data['list'][0]['dt'])+(daysHence*24*3600)
            index = -1
            for i, val in enumerate(data['list']):
                if(timestampForDaysHence<=val['dt'] and daysHence>=0 and daysHence<=5):
                    index = i
                    break
                continue
            if index == -1:
                return {'description':'could not find temperature beyond 4 days'}        
            else:

                obj['description'] = data['list'][index]['weather'][0]['description']
                obj['temperature'] = str(data['list'][index]['main']['temp'])+' degree celsius'
                obj['windSpeed'] = str(data['list'][index]['wind']['speed'])+' m/s'
                dispatcher.utter_message("{} with a temperature of {} and winspeed of {}".format(obj['description'], obj['temperature'], obj['windSpeed']))
                
        else:
            obj['description'] = 'city not found'
            dispatcher.utter_message("Sorry! Looks like the city you entered is not correct.")
            # dispatcher.utter_message("Api call for weather complete.")
        return []


class AgriForm(FormAction):
    """Answers agri based questions"""

    def name(self):
        return "agri_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "question",
            ]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return{
            "question":self.from_text(),
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
    
        query = tracker.get_slot('question')
        print('query entered',query)
        url = 'http://localhost:8080/getAnswer'

        data = {"question": str(query)}
        j_data = json.dumps(data)
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        res = requests.post(url, data=j_data, headers=headers)
        temp = res.json()
        temp = str(temp['answer'])
        dispatcher.utter_message(text=temp)
        return []

# class WelcomeForm(FormAction):
#     """Answers agri based questions"""

#     def name(self):
#         return "welcome_form"

#     @staticmethod
#     def required_slots(tracker):
#         return [
#             "option",
#             ]

#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         return{
#             "option":self.from_text(),
#         }

#     def submit(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict]:
    
#         option = tracker.get_slot('option')
#         print(option)
#         return [SlotSet("option",option)]

class ActionGreetUser(Action):
    """Revertible mapped action for utter greet"""
    def name(self):
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_greet", tracker)
        return [UserUtteranceReverted()]

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "fallback_action"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ):

    
        dispatcher.utter_message("Sorry! I did not understand what you said.")
        return [UserUtteranceReverted()]



