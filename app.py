import os
import telebot
import requests
import urllib
from flask import Flask, request
from instaTools.instaAccess import InstaAccess
app = Flask(__name__)

IS_OFFLINE = os.environ.get('IS_OFFLINE', 0)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
bot = telebot.TeleBot(BOT_TOKEN)
instaAccess = InstaAccess()

@bot.message_handler(commands=['help'])
def Help(message):
    bot.send_message(message.chat.id, "Hi, I'm ready")

@bot.message_handler(commands=['start'])
def Start(message):
    payload = {'redirect_uri' : REDIRECT_URI, 'client_id' : CLIENT_ID\
               , 'state' : message.chat.id, 'response_type' : "code"}
    url = "https://api.instagram.com/oauth/authorize/?" + urllib.parse.urlencode(payload)
    bot.send_message(message.chat.id, url)

@app.route('/')
def hello():
    return "Hello world!"

@app.route('/redirect')
def redirect():
    code = request.args.get('code')
    chat_id = request.args.get('state')
    payload = {'redirect_uri': REDIRECT_URI, 'client_id': CLIENT_ID, 'code': code\
               , 'client_secret' : CLIENT_SECRET,  'grant_type' : 'authorization_code'}
    r = requests.post("https://api.instagram.com/oauth/access_token", data=payload)

    responseData = r.json()
    access_token = responseData["access_token"]
    user = responseData["user"]
    username = user["username"]
    user_id = user["id"]
    bot.send_message(chat_id, "Hi, {}, I am ready to search your data. token = {}".format(username, access_token))

    instaAccess.resetApi(access_token=access_token, client_secret=CLIENT_SECRET)

    recent_media = instaAccess.getMediaRecent(count=1)
    return "ok!", 200

@app.route("/{}".format(BOT_TOKEN), methods=["POST"])
def bot_main():
    update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    #print("bot request: " + str(update))
    return "ok!", 200

if __name__ == '__main__':
    app.run()