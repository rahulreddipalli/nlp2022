from flask import Flask, render_template, request, redirect, url_for
from chatbot import Chatbot
import json

app = Flask(__name__)
@app.post('/get_response')
def get_response():
    data = request.json
    print(data)
    user_input = data['msg']
    response=bot.get_response(user_input)
    return json.dumps(response)

@app.post('/start_greeting')   
def start_greeting():
    response=bot.say_greeting()
    print(response)
    return json.dumps(response)
    
if __name__ == '__main__' :
    bot = Chatbot("DearBot")  
    app.run(debug=True)
