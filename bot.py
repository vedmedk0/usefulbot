# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:25:18 2017

@author: VedMedk0
"""

import config
import telebot
import sqlighter
bot = telebot.TeleBot(config.token)
DB=sqlighter.SQLighter(config.database_name)

#команда старт
@bot.message_handler(commands=['start'])
def handle_start(message):
     bot.send_message(message.chat.id, 'тут будет старт')
     
#список людей - обязательно с параметром 1 или 2
@bot.message_handler(commands=['base2'])
def handle_base(message):
    com=message.text.split()
    if com[1] in ["1","2"] and len(com)>1:
        bot.send_message(message.chat.id, str(DB.select_notif_specified(com[1])))

     
#кол-во строчек в базе данных
@bot.message_handler(commands=['base1'])
def handle_base(message):
     bot.send_message(message.chat.id, str(DB.count_rows()))
     
#элементарный диалог
@bot.message_handler(commands=['dial'])
def handle_dialog(message):
     bot.send_message(message.chat.id, 'пики точеные или хуи дроченые?')
     bot.register_next_step_handler(message, pikes_or_dicks)
     
def pikes_or_dicks(message):
    try:
        if message.text == 'хуи':
            bot.send_message(message.chat.id, 'тут мог быть стикер с хуями')
        if message.text == 'пики':
            bot.send_message(message.chat.id, 'тут мог быть стикер с пиками')
    except Exception as e:
        bot.reply_to(message, 'oooops')
#не знаю зачем
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if (message.chat.id==config.ID_vedmedk0):
        #bot.send_message(message.chat.id, 'hello vedmedk0')
        #bot.send_message(config.ID_vedmedk0,str(message.from_user.username) +' написал ' + message.text)
        #print(message)
        pass
    else:
        #bot.send_message(message.chat.id, 'ты кто?')
        bot.send_message(config.ID_vedmedk0,str(message.from_user.username) +' написал ' + message.text)
       
        


if __name__ == '__main__':
     bot.polling(none_stop=True)