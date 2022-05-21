from unicodedata import name

import ner_handler

class Chatbot:
    def __init__(self,name):
        self.name = name
    
    def get_response(self,user_input):

        return user_input