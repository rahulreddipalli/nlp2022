import chatbot_logger

import torch
import string
import os

import numpy as np

import tensorflow as tf
import pickle

from keras.models import load_model
from keras.layers import TextVectorization

cuda_available = torch.cuda.is_available()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

model = load_model("intent classifier/intents.h5")

from_disk = pickle.load(open("intent classifier/vectoriser.pkl", "rb"))

vectoriser = TextVectorization.from_config(from_disk['config'])
vectoriser.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))  # call adapt on dummy data
vectoriser.set_weights(from_disk['weights'])
encoder = pickle.load(open("intent classifier/encoder.pkl", "rb"))

class_names = encoder.classes_

input_str = tf.keras.Input(shape=(1,), dtype="string")
x = vectoriser(input_str)  # vectorize
output = model(x)
intent_classifier = tf.keras.Model(input_str, output)


def clean(message):
    message = " ".join([word.lower() for word in message.split()])

    remove = str.maketrans((string.punctuation + '£' + string.digits), ' '*len((string.punctuation + '£' + string.digits)))
    result = message.translate(remove)
    return result


def predict_intent(user_input):
    user_input = clean(user_input)
    prediction = intent_classifier.predict([[user_input]])
    intent = class_names[np.argmax(prediction[0])]
    chatbot_logger.log_prediction("Predicting user intent", user_input, intent)
    return intent
