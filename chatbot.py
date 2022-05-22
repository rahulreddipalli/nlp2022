from unicodedata import name
from state_enum import STATE
import ner_handler
import intent_handler

class Chatbot:
    def __init__(self,name):
        self.name = name
        self.state = STATE.GREETING
        self.users_name = None
        self.new_entry = []
    def get_response(self,user_input):
        response = ""
        if self.state == STATE.ASKED_NAME:
            response=self.ask_name(user_input)

        if self.state == STATE.ADD_ENTRY:
            response= self.add_entry(user_input)

        if self.state == STATE.RUNNING:
            intent = intent_handler.get_intent(user_input)
            #if intent_handler.get_intent(user_input)=="greeting":
                #name=ner_handler.get_entity(user_input,"PERSON")[0]
                #response = "Hi {}! What do you want to do today".format(name)
                #response = "Goodbye"
            
            if intent_handler.get_intent(user_input)=="view_entry":
                self.state = STATE.ADD_ENTRY
                response="Tell me about your day!"

            if intent =="goodbye":
                response = intent_handler.get_response_by_intent(intent)
                response = response.format(self.users_name)
                self.state == STATE.QUIT
        return self._format_response(response)


    def _get_names(self,user_input):
        names = ner_handler.get_entity(user_input,"PERSON")
        return names if len(names)>0 else None
    
    def add_entry(self,user_input):
        response = ""
        if user_input.lower() =="yes":
            #call database update function here maybe?
            response = "Thanks for telling me about your day" 
            self.state=STATE.RUNNING
            return response

        self.new_entry = user_input        

        response = "Today, you said you did this:\n"+"You also said you did this:".join(self.new_entry)

        return response
    def ask_name(self,user_input):
        response = ""

        names = self._get_names(user_input)
        
        if names ==None and not user_input.lower() in ["yes","no"]: return "Sorry I didnt recognise a name? What is your name?"
        if names != None: self.users_name=names[0]
        name=self.users_name
        response = "Is {} your name?  yes|no".format(name)
        if user_input.lower() == "yes":
            response = "Hi {}! What do you want to do today".format(name)
            self.users_name=name
            self.state =STATE.RUNNING
        elif user_input.lower() == "no":
            response = "What is your name then?"
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