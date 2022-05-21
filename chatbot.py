from unicodedata import name

#import ner_handler

class Chatbot:
    def __init__(self,name):
        self.name = name
        self.state = "GREETING"
    
    def get_response(self,user_input):
        response = ""
        if self.state == "ASKED_NAME":
            response = "Hi {}! What do you want to do today".format(user_input)
        return self._format_response(response)

    def say_greeting(self):
        if self.state=="GREETING":
            self.state = "ASKED_NAME"
            return self._format_response("Hey what's your name?")
            
    
    def _format_response(self,response):
        return {"response":response,"state":self.state}