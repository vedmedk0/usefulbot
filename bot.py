# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:25:18 2017

@author: VedMedk0
"""

import config
import telebot
s= None
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def handle_start(message):
     bot.send_message(message.chat.id, 'тут будет старт')

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if (message.chat.id==config.ID_vedmedk0):
        bot.send_message(message.chat.id, 'hello vedmedk0')
        #bot.send_message(config.ID_vedmedk0,str(message.from_user.username) +' написал ' + message.text)
        #print(message)
    else:
        bot.send_message(message.chat.id, 'ты кто?')
        bot.send_message(config.ID_vedmedk0,str(message.from_user.username) +' написал ' + message.text)
       
        


if __name__ == '__main__':
     bot.polling(none_stop=True)