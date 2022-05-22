from unicodedata import name
from state_enum import STATE
import ner_handler
import intent_handler
import pandas as pd
from os.path import exists
import os


class Chatbot:
    def __init__(self, name):
        self.name = name
        self.state = STATE.GREETING
        self.user_id = None
        self.users_name = None
        self.users_phrase = None
        self.new_entry = []

    def get_response(self, user_input):
        response = ""
        if self.state == STATE.CHECK_IF_NEW:
            response = self.confirm_profile(user_input)

        elif self.state == STATE.CREATE_PROFILE_NAME:
            response = self.ask_name(user_input)

        elif self.state == STATE.CONFIRM_NAME:
            response = self.confirm_name(user_input)

        elif self.state == STATE.CREATE_PROFILE_PHRASE:
            response = self.ask_phrase(user_input)
            self.state = STATE.CONFIRM_PHRASE

        elif self.state == STATE.CONFIRM_PHRASE:
            response = self.confirm_phrase(user_input)

        elif self.state == STATE.ADD_ENTRY:
            response = self.add_entry(user_input)

        elif self.state == STATE.RUNNING:
            intent = intent_handler.get_intent(user_input)
            # if intent_handler.get_intent(user_input)=="greeting":
            # name=ner_handler.get_entity(user_input,"PERSON")[0]
            # response = "Hi {}! What do you want to do today".format(name)
            # response = "Goodbye"

            if intent_handler.get_intent(user_input) == "add_entry":
                self.state = STATE.ADD_ENTRY
                response = "Tell me about your day!"

            if intent_handler.get_intent(user_input) == "view_entry":
                self.state = STATE.VIEW_ENTRY
                response = "Tell me about your day!"

            if intent == "goodbye":
                response = intent_handler.get_response_by_intent(intent)
                response = response.format(self.users_name)
                self.state == STATE.QUIT
        return self._format_response(response)

    def confirm_profile(self, user_input):
        response = ""
        if user_input == "yes":
            self.state = STATE.ASKED_NAME
            response = "Great! Please could you tell me your name?"

        if user_input == "no":
            self.state = STATE.CREATE_PROFILE_NAME
            response = "No worries, let's create a profile for you. What's your name?"

        return response

    def _get_names(self, user_input):
        names = ner_handler.get_entity(user_input, "PERSON")
        return names if len(names) > 0 else None

    def add_entry(self, user_input):
        response = ""
        if user_input.lower() == "yes":
            # call database update function here maybe?
            response = "Thanks for telling me about your day"
            self.state = STATE.RUNNING
            return response

        self.new_entry = user_input

        response = "Today, you said you did this:\n" + "You also said you did this:".join(self.new_entry)

        return response

    def ask_phrase(self, user_input):
        response = ""
        self.users_phrase = user_input

        if self.users_phrase is None:
            return "Sorry I didn't recognise a phrase? Can you give me a special phrase?"

        response = "Is {} the phrase you'd like to use?  yes|no".format(self.users_phrase)

        return response

    def confirm_phrase(self, user_input):
        response = ""

        if user_input.lower() == "yes":
            if exists('csvs/users.csv'):
                users = pd.read_csv('csvs/users.csv')
                users = users.to_numpy()

                for user in users:
                    if self.users_name == user[1] and self.users_phrase == user[2]:
                        return "Sorry {}, please could you use a different phrase?".format(self.users_name)
            else:
                users = []
                os.mkdir("csvs")
                os.mkdir("csvs/user_csvs")

            self.user_id = len(users)

            with open('csvs/users.csv', 'a') as fd:
                fd.write(str(self.user_id) + "," + self.users_name + "," + self.users_phrase)
                fd.close()

            with open('csvs/user_csvs/{}.csv'.format(self.user_id), 'a') as fd:
                fd.write('date' + "," + 'entry' + "," + 'location' + "," + 'people' + "," + 'emotion')
                fd.close()

            self.state = STATE.RUNNING
            response = "Thanks {}! Now that we've met, what would you like to do?".format(
                self.users_name)

        elif user_input.lower() == "no":
            response = "What would you like your phrase to be instead?"

        return response

    def ask_name(self, user_input):
        names = self._get_names(user_input)

        if names is None:
            return "Sorry I didn't recognise a name? What is your name?"

        if names != None:
            self.users_name = names[0]
        self.state = STATE.CONFIRM_NAME
        response = "Is {} your name?  yes|no".format(self.users_name)

        return response

    def confirm_name(self, user_input):
        response = ""
        if user_input.lower() == "yes":
            self.state = STATE.CREATE_PROFILE_PHRASE
            response = "Hi {}! Can you please give me a special phrase that you'll use you access your diary?".format(
                self.users_name)

        elif user_input.lower() == "no":
            response = "What is your name then?"

        return response

    def choose_what_to_do(self,user_input):
        pass

    def say_greeting(self):
        response = ""
        if self.state == STATE.GREETING:
            self.state = STATE.CHECK_IF_NEW
            response = "Hey there! Have you used DiaryBot before?"
        return self._format_response(response)

    def _format_response(self, response):
        return {"response": response, "state": self.state.value}
