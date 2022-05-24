from state_enum import STATE
import chatbot_logger
import ner_handler
import intent_handler
import sentiment_handler
import pandas as pd
from os.path import exists
import os
import csv
from datetime import date, timedelta


class Chatbot:
    def __init__(self, name):
        self.name = name
        self.__change_state(STATE.GREETING)
        self.user_id = None
        self.users_name = None
        self.users_phrase = None
        self.new_entry = []

    def get_response(self, user_input):
        print(self.state)
        response = ""
        if self.state == STATE.CHECK_IF_NEW:
            response = self.confirm_profile(user_input)

        # PROFILE LOGIN
        elif self.state == STATE.LOGIN_NAME_ENTRY:
            response = self.ask_login_name(user_input)

        elif self.state == STATE.CONFIRM_LOGIN_NAME:
            response = self.confirm_login_name(user_input)

        elif self.state == STATE.LOGIN_PHRASE_ENTRY:
            response = self.ask_login_phrase(user_input)


        # PROFILE CREATION
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

        elif self.state == STATE.VIEW_ENTRY:
            response = self.view_entry(user_input)

        elif self.state == STATE.RUNNING:
            intent = intent_handler.predict_intent(user_input)
            # if intent_handler.get_intent(user_input)=="greeting":
            # name=ner_handler.get_entity(user_input,"PERSON")[0]
            # response = "Hi {}! What do you want to do today".format(name)
            # response = "Goodbye"

            print(intent)
            if intent == "add_entry":
                self.__change_state(STATE.ADD_ENTRY)
                response = "Sure, tell me about your day!"

            elif intent == "view_entry":
                response = self.view_entry(user_input)

            elif intent == "goodbye":
                response = self.goodbye()
            else:
                response = "Sorry I don't understand what you're trying to do."

        chatbot_logger.log_converstion(user_input, response)
        return self.__format_response(response)

    def confirm_profile(self, user_input):
        response = ""
        if user_input == "yes":
            self.__change_state(STATE.LOGIN_NAME_ENTRY)
            response = "Great! Please could you tell me your name?"

        if user_input == "no":
            self.__change_state(STATE.CREATE_PROFILE_NAME)
            response = "No worries, let's create a profile for you. What's your name?"

        return response

    def __get_names(self, user_input):
        names = ner_handler.get_entity(user_input, "PERSON")
        return names if len(names) > 0 else None

    def view_entry(self, user_input):
        date = ner_handler.get_date(user_input)
        user_data = pd.read_csv('csvs/user_csvs/{}.csv'.format(self.user_id))
        user_data = user_data.to_numpy()

        location = ""
        people = ""
        emotion = ""
        for row in user_data:
            if row[0] == date:
                location = row[2]
                people = row[3]
                emotion = row[4]

            return "On {}, you were at {}, you were with {} and you felt {}.\nIs there anything else you'd like to do?".format(date, location, people, emotion)
        return "It seems like you don't have an entry for that day. What else would you like to do?"

    def add_entry(self, user_input):
        response = ""
        entry_ner = ner_handler.predict_ner(user_input)

        for item in entry_ner:
            print(item)

        locations = []
        people = []
        emotion = []

        for key in entry_ner:
            if entry_ner[key] == 'GPE':
                locations.append(key)
            if entry_ner[key] == 'PERSON':
                people.append(key)

        with open('csvs/user_csvs/{}.csv'.format(self.user_id), 'a') as fd:
            writer = csv.writer(fd)
            writer.writerow([str(date.today()), user_input, locations, people, emotion])
            fd.close()

        response = "Thanks for telling me about your day. This was your entry:\n{}\n" \
                   "Is there anything else you'd like to do?".format(user_input)
        self.__change_state(STATE.RUNNING)
        return response

    def goodbye(self):
        self.__change_state(STATE.GREETING)
        return "Thanks for using {}! Goodbye!".format(self.name)

    def ask_login_name(self, user_input):
        names = self.__get_names(user_input)

        if names is None:
            return "Sorry I didn't recognise a name? What is your name?"

        if names != None:
            self.users_name = names[0]
        self.__change_state(STATE.CONFIRM_LOGIN_NAME)
        response = "Is {} your name?  yes|no".format(self.users_name)

        return response

    def confirm_login_name(self, user_input):
        response = ""
        if user_input.lower() == "yes":
            self.__change_state(STATE.LOGIN_PHRASE_ENTRY)
            response = "Hi {}! Can you please enter your special phrase?".format(
                self.users_name)

        elif user_input.lower() == "no":
            response = "What is your name then?"

        return response

    def ask_login_phrase(self, user_input):
        self.users_phrase = user_input

        if self.users_phrase is None:
            return "Sorry I didn't recognise a phrase? Can you give me a special phrase?"

        users = pd.read_csv('csvs/users.csv')
        users = users.to_numpy()
        for user in users:
            if self.users_name == user[1] and self.users_phrase == user[2]:
                self.user_id = user[0]
                self.__change_state(STATE.RUNNING)
                return "Hi {}! Nice to see you again! What would you like to do?".format(self.users_name)

        return "Sorry {}, but I don't think we've met before, or you may have given me the wrong details.".format(self.users_name)


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
                writer = csv.writer(fd)
                writer.writerow(["user_id", "user_name", "user_phrase"])
                writer.writerow([str(self.user_id), self.users_name, self.users_phrase])
                fd.close()

            with open('csvs/user_csvs/{}.csv'.format(self.user_id), 'a') as fd:
                writer = csv.writer(fd)
                writer.writerow(['date', 'entry', 'location', 'people', 'emotion'])
                fd.close()

            self.__change_state(STATE.RUNNING)
            response = "Thanks {}! Now that we've met, what would you like to do?".format(
                self.users_name)

        elif user_input.lower() == "no":
            response = "What would you like your phrase to be instead?"

        return response

    def ask_name(self, user_input):
        names = self.__get_names(user_input)

        if names is None:
            return "Sorry I didn't recognise a name? What is your name?"

        if names != None:
            self.users_name = names[0]
        self.__change_state(STATE.CONFIRM_NAME)
        response = "Is {} your name?  yes|no".format(self.users_name)

        return response

    def confirm_name(self, user_input):
        response = ""
        if user_input.lower() == "yes":
            self.__change_state(STATE.CREATE_PROFILE_PHRASE)
            response = "Hi {}! Can you please give me a special phrase that you'll use you access your diary?".format(
                self.users_name)

        elif user_input.lower() == "no":
            response = "What is your name then?"

        return response

    def choose_what_to_do(self, user_input):
        pass

    def say_greeting(self):
        response = ""
        if self.state == STATE.GREETING:
            self.__change_state(STATE.CHECK_IF_NEW)
            response = "Hey there! Have you used {} before?".format(self.name)
        return self.__format_response(response)

    def __format_response(self, response):
        return {"response": response, "state": self.state.value}

    def __change_state(self, state: STATE):
        self.state = state
        chatbot_logger.log_bot_state(self.state.name)
