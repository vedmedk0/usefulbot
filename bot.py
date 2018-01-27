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

class User:
    def __init__(self, name):
        self.name = name
        self.taglist=[]
        self.telegram_id = None
        self.telegram_usernane = None
        self.notif = None
    
    def Userinfo (self):
        return 'имя: {} \n username: {} \n notif: {} \n taglist: {}'.format(self.name, self.telegram_username,self.notif,self.taglist)
#словарь, для того чтобы хранить данные между вызовами функций диалога    
user_dict = {}

#команда старт
@bot.message_handler(commands=['start'])
def handle_start(message):
     bot.send_message(message.chat.id, 'тут будет старт')
     
#получить свой айди
@bot.message_handler(commands=['myid'])
def handle_myid(message):
     bot.send_message(message.chat.id, str(message.from_user.id))
     
#новая строк
@bot.message_handler(commands=['newline'])
def new_line(message):
    bot.send_message(message.chat.id, 'Как к тебе обращаться?')

    bot.register_next_step_handler(message, new_line_notif)
    
def new_line_notif(message):
    Newhelper=User(message.text)
    Newhelper.telegram_id=message.from_user.id
    Newhelper.telegram_username=message.from_user.username    
    user_dict[message.chat.id]=Newhelper
    bot.send_message(message.chat.id, 'Выбери способ оповещений. 2 - юзер видит твое имя и пишет тебе сам, 1 - тебя оповещает бот, и ты отзываешься если можешь')
    bot.register_next_step_handler(message, new_line_taglist)
    
def new_line_taglist(message):
    Newhelper=user_dict[message.chat.id]
    Newhelper.notif=message.text
    bot.send_message(message.chat.id, 'Теги через пробел (потом тут будут кнопки(наверное))')
    bot.register_next_step_handler(message, end_of_procedure)
    
def end_of_procedure(message):
    Newhelper=user_dict[message.chat.id]
    Newhelper.taglist=message.text.split()
    #новые строчки в ббазе данных
    #проверка вывода
    bot.send_message(message.chat.id, Newhelper.Userinfo() )

     
#список людей - обязательно с параметром 1 или 2
@bot.message_handler(commands=['base2'])
def handle_base(message):
    com=message.text.split()
    if com[1] in ["1","2"] and len(com)>1:
        bot.send_message(message.chat.id, str(DB.select_notif_specified(com[1])))
        
#список людей по тегу и нотиф
@bot.message_handler(commands=['base4'])
def extract_by_tag_notif(message):
    com=message.text.split(maxsplit=2)
    if len(com)==3:
        bot.send_message(message.chat.id, str(DB.select_tag_notif(com[1],com[2])))
        #bot.send_message(message.chat.id, str(com[1]))

#список людей по тегу       
@bot.message_handler(commands=['base3'])
def extract_by_tag(message):
    com=message.text.split(maxsplit=2)
    if len(com)==2:
        bot.send_message(message.chat.id, str(DB.select_tag_specified(com[1])))
        #bot.send_message(message.chat.id, str(com[1]))

     
#кол-во строчек в базе данных
@bot.message_handler(commands=['base1'])
def how_many_rows(message):
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
            #bot.send_sticker(message.chat_id, "CAADAgAD2QADsJjjA7RvJme9sLMQAg")
        if message.text == 'пики':
            bot.send_message(message.chat.id, 'тут мог быть стикер с пиками')
            #bot.send_sticker(message.chat_id, "CAADAgAD2gADsJjjA6aBdBwtR50XAg")
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
        #bot.send_message(config.ID_vedmedk0,str(message.from_user.username) +' написал ' + message.text)
        pass
       
        


if __name__ == '__main__':
     bot.polling(none_stop=True)