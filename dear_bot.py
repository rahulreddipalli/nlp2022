from flask import Flask, render_template, request, redirect, url_for
#from chatbot import Chatbot

if __name__ == '__main__' :
    app = Flask(__name__)
    # bot = Chatbot("DearBot")

    @app.post('/get_response')
    def get_response():
        data = request.json
        print(data)
        user_input = data['msg']
        predictions="t" #bot.get_response(user_input)

        return user_input

    app.run(debug=True)
