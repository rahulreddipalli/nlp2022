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
            name=ner_handler.get_entity(user_input,"PERSON")[0]
            response = "Hi {}! What do you want to do today".format(name)
            self.state =STATE.RUNNING
        

        #if intent_handler.get_intent(user_input)=="goodbye":
            #self.state = "QUIT"
            #response = "Goodbye"
        return self._format_response(response)

    def say_greeting(self):
        response = ""
        if self.state==STATE.GREETING:
            self.state = STATE.ASKED_NAME
            response = "Hey what's your name?"
        return self._format_response(response)
            
    
    def _format_response(self,response):
        return {"response":response,"state":self.state.value}