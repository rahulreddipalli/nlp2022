import requests
import json
STATE = "RUNNING"
data = {}
counter = 0

def get_response(url,data):
    response = requests.post(url,json=data)
    response = json.loads(response.text)
    print(response["response"])
    return response["response"], response["state"]

def format_bot_response(response):
    print("Bot: {}".format(response))

data={"msg":None}
response, STATE= get_response('http://localhost:5000/start_greeting',data)
format_bot_response(response)


while not STATE == "QUIT":
    data["msg"]=input("User: ")
    response, STATE= get_response('http://localhost:5000/get_response',data)
    format_bot_response(response)

print("Client closed")