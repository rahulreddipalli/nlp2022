from transformers import pipeline
import chatbot_logger
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

classifier = pipeline("text-classification", model='model')

moods = {
    "happy": ":D",
    "sad": ":C",
    "anxious": ":z",
    "angry": ">:C",
    "tired": "(z_Z)",
    "bored": ":|",
    "neutral": ":L"}


prediction = classifier("I love using transformers. The best part is wide range of support and its easy to use", )


def predict_sentiment(user_input):
    sent_pred = classifier(user_input)
    sentiment = sent_pred[0]['label']
    chatbot_logger.log_prediction("Making Sentiment Prediction", user_input, sentiment)
    return sentiment


def get_emoticon(user_input):
    sentiment = predict_sentiment(user_input)
    emoticon = moods[sentiment]
    return sentiment, emoticon

