import logging

logging.basicConfig(filename='chatbot.log', encoding='utf-8', level=logging.INFO)


def log_prediction(title,user_input,prediction):
    logging.info("\n {}\n  User input: {}\n Prediction:{}".format(title,user_input,prediction))

def log_database_action(info):
    logging.info("Database action: ",info)
def log_info(info):
    logging.info(info)