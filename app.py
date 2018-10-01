import os
import telebot
import requests
import urllib
from flask import Flask, jsonify, request
app = Flask(__name__)

IS_OFFLINE = os.environ.get('IS_OFFLINE', 0)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
print("BOT_TOKEN is " + BOT_TOKEN)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['help'])
def Help(message):
    bot.send_message(message.chat.id, "Hi, I'm ready")

@bot.message_handler(commands=['start'])
def Start(message):
    payload = {'redirect_uri' : REDIRECT_URI, 'client_id' : CLIENT_ID, 'response_type' : "code"}
    url = "https://api.instagram.com/oauth/authorize/?" + urllib.parse.urlencode(payload)

    #r = requests.get("https://api.instagram.com/oauth/authorize", payload)
    bot.send_message(message.chat.id, url)

@app.route('/')
def hello():
    return "Hello world!"

@app.route('/redirect')
def redirect():
    code = request.args.get('code')
    print("redirect request code: " + code)
    return "Hello redirect!"

@app.route("/{}".format(BOT_TOKEN), methods=["POST"])
def bot_main():
    update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    print("bot request: " + str(update))
    return "ok!", 200

if __name__ == '__main__':
    app.run()