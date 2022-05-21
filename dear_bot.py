from flask import Flask, render_template, request, redirect, url_for
from chatbot import Chatbot
import json

if __name__ == '__main__' :
    app = Flask(__name__)
    bot = Chatbot("DearBot")

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
        return json.dumps(response)
        
    app.run(debug=True)
