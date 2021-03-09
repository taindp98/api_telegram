
import json
#import telebot
import requests

import re
from flask import Flask, request
import telegram
#from telebot.credentials import bot_token, bot_user_name,URL

bot_token = "1607480015:AAFRjjzwhq5FLcwTFgde1gBzjc5v-g5Imck"
bot_user_name = "BKBot"
URL = "https://telegram-hcmut.herokuapp.com/"


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   print('update',update)
   
   # if update.message:
   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   
   chatbot_sys_api_url = 'https://chatbot-hcmut.herokuapp.com/api/convers-manager'
   input_data = {}
   input_data['message'] = str(text)
   input_data['state_tracker_id'] = chat_id
   r = requests.post(url=chatbot_sys_api_url, json=input_data)
   chatbot_respose = r.json()
   mess_response = chatbot_respose['message'].replace('\n', r'').replace(r'"',r'')
   
   bot.sendMessage(chat_id=chat_id, text=mess_response, reply_to_message_id=msg_id)

   return 'ok'
   # else:
   		# return 'fail'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)
# get_bot_response()
#
# if __name__ == '__main__':
#     app.run(threaded=True)

