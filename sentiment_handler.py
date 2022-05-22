import random as rand
import chatbot_logger
moods = {"happy":":D","sad":":C","anxious":":z","angry":">:C","tired":"(z_Z)","bored":":|"}

class Model:
    def predict(self,user_input):
        return rand.choice(list(moods.keys()))

model = Model()

def predict_sentiment(user_input):
    sentiment = model.predict(user_input)
    chatbot_logger.log_prediction("Making Sentiment Prediction",user_input,{sentiment:0.58})
    return sentiment

def get_emoticon(user_input):
    sentiment = predict_sentiment(user_input)
    emoticon = moods[sentiment]
    return sentiment,emoticon


sentiment ,emoticon= get_emoticon("test")

print("You seemed {}: {}".format(sentiment,emoticon))