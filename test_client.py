import requests
import json
data = {}
counter = 0

goodbye_phrases = ["Goodbye!", "Okay, see you soon!", "Okay, no worries, see you soon!",
                   "Sorry, I can't help without your name.. See you next time.", "Okay :( See you soon.", "Okay. See you next time."]

def get_response(url,data):
    response = requests.post(url,json=data)
    response = json.loads(response.text)
    return response["response"], response["state"]

def format_bot_response(response):
    print("Bot: {}".format(response))

data={"msg":None}
response, state= get_response('http://localhost:5000/start_greeting',data)
format_bot_response(response)


while state > 0:
    data["msg"] = input("User: ")
    response, state = get_response('http://localhost:5000/get_response', data)
    format_bot_response(response)
    if response[-8:] == "Goodbye!":
        break
    if response in goodbye_phrases:
        break

print("Client closed")