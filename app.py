import os
import telebot
import sys
from flask import Flask, jsonify, request
app = Flask(__name__)

IS_OFFLINE = os.environ.get('IS_OFFLINE', 0)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
print("BOT_TOKEN is " + BOT_TOKEN)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['help'])
def Help(message):
    bot.send_message(message.chat.id, "Hi, I'm ready")

@app.route('/')
def hello():
    return "Hello world!"

@app.route('/redirect')
def redirect():
    update = request.get_json()
    print("redirect request: " + str(update))
    return "Hello redirect!"

@app.route("/{}".format(BOT_TOKEN), methods=["POST"])
def bot_main():
    update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    print("bot request: " + str(update))
    return "ok!", 200

if __name__ == '__main__':
    app.run()