import logging

logging.basicConfig(filename='chatbot.log', encoding='utf-8', level=logging.INFO)


def log_prediction(title,user_input,prediction):
    logging.info("\n {}\n  User input: {}\n Prediction:{}".format(title,user_input,prediction))

def log_database_action(info):
    logging.info("Database action: ",info)

def log_info(info):
    logging.info(info)

def log_bot_state(state):
    logging.info("Chatbot State: ".format(state))

def log_converstion(user_input,bot_response):
    logging.info("\nUser-Chatbot Interaction\nUser said: {}\nChatbot response: {}".format(user_input,bot_response))