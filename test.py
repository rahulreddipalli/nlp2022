import requests
import json
from state_enum import STATE
state = STATE.RUNNING
data = {}
counter = 0

def get_response(url,data):
    response = requests.post(url,json=data)
    print(response.text)
    response = json.loads(response.text)
    return response["response"], response["state"]

def format_bot_response(response):
    print("Bot: {}".format(response))

data={"msg":None}
response, state= get_response('http://localhost:5000/start_greeting',data)
format_bot_response(response)


while not state == STATE.QUIT:
    data["msg"]=input("User: ")
    response, state= get_response('http://localhost:5000/get_response',data)
    format_bot_response(response)

print("Client closed")