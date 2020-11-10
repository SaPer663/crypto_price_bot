#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy
import telebot
from config import token, chat_id, path_to_cert,\
     url_server, first_currency_name, second_currency_name,\
     port
from api_db import read_file


BOT_TOKEN = token
WEBHOOK_SSL_CERT = path_to_cert
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = chat_id
PORT = port


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, "Привет! Я crypto_price_bot")

@bot.message_handler(commands=[first_currency_name])
def command_first(message):
    load_price = read_file()
    print(load_price)
    price = load_price[0]["data"]["last"]
    bot.send_message(message.chat.id, f'{first_currency_name}: {price}')

@bot.message_handler(commands=[second_currency_name])
def command_second(message):
    load_price = read_file()
    price = load_price[1]["data"]["last"]
    bot.send_message(message.chat.id, f'{second_currency_name}: {price}')
    

def send_message(text, id=CHAT_ID):
    bot.send_message(id, text)

class WebhookServer(object):
    # index равнозначно /, т.к. отсутствию части после ip-адреса (грубо говоря)
    @cherrypy.expose
    def index(self):
        length = int(cherrypy.request.headers['content-length'])
        json_string = cherrypy.request.body.read(length).decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

if __name__ == '__main__':

    bot.remove_webhook()
    bot.set_webhook(url=url_server,
                    certificate=open(WEBHOOK_SSL_CERT, 'r')) 
 
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': PORT,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
