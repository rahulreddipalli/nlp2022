import chatbot_logger

import torch
import string
import os
import numpy as np
import pickle

from keras.models import load_model

cuda_available = torch.cuda.is_available()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model = load_model("intent_classifier")

encoder = pickle.load(open("intent_classifier/encoder.pkl", "rb"))

class_names = encoder.classes_


def clean(message):
    message = " ".join([word.lower() for word in message.split()])

    remove = str.maketrans((string.punctuation + '£' + string.digits), ' '*len((string.punctuation + '£' + string.digits)))
    result = message.translate(remove)
    return result


def predict_intent(user_input):
    user_input = clean(user_input)
    prediction = model.predict([[user_input]])
    intent = class_names[np.argmax(prediction[0])]
    chatbot_logger.log_prediction("Predicting user intent", user_input, intent)
    return intent
