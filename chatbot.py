from unicodedata import name
from state_enum import STATE
import ner_handler


class Chatbot:
    def __init__(self,name):
        self.name = name
        self.state = STATE.GREETING
    
    def get_response(self,user_input):
        response = ""
        if self.state == STATE.ASKED_NAME:
            self.ask_name(user_input)
        #if intent_handler.get_intent(user_input)=="greeting":
            #name=ner_handler.get_entity(user_input,"PERSON")[0]
            #response = "Hi {}! What do you want to do today".format(name)
            #response = "Goodbye"
        
        #if intent_handler.get_intent(user_input)=="view_entry":
            #date = ner.show_last_entry(user_input)
            #use date to find entry
        return self._format_response(response)

    def ask_name(self,user_input):
        response = ""
        name=ner_handler.get_entity(user_input,"PERSON")[0]
        response = "Is {} your name?".format(name)
        if user_input.lower() == "yes":
            response = "Hi {}! What do you want to do today".format(name)
            self.state =STATE.RUNNING
        elif user_input.lower() == "no":
            response = "What is your name then? yes|no"
            self.state == STATE.ASKED_NAME
        return response

    def say_greeting(self):
        response = ""
        if self.state==STATE.GREETING:
            self.state = STATE.ASKED_NAME
            response = "Hey what's your name?"
        return self._format_response(response)
            
    
    def _format_response(self,response):
        return {"response":response,"state":self.state.value}