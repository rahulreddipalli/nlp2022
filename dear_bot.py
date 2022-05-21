from flask import Flask, render_template, request, redirect, url_for
from chatbot import Chatbot

if __name__ == '__main__' :
    app = Flask(__name__)
    bot = Chatbot("DearBot")

    @app.post('/get_response')
    def get_response():
        data = request.json
        user_input = request.form['chat']
        predictions=bot.get_response(user_input)

        return str(predictions)


    app.run(debug=True)
