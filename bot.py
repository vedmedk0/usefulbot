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

class User: #Класс для сбора информации о новом хелпере, все поля селфэксплейнинг
    def __init__(self, name):
        self.name = name
        self.taglist=[]
        self.telegram_id = None
        self.telegram_usernane = None
        self.notif = None
    
    def Userinfo (self): # Метод для вывода строки с инфой из вышеперечисленных полей
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
     
@bot.message_handler(commands=['talktoved'])
def talktoved(message):
     bot.send_message(config.ID_vedmedk0, 'hello ved')
     
#диалог для новой строки
@bot.message_handler(commands=['newline'])
def new_line(message):
    bot.send_message(message.chat.id, 'Как к тебе обращаться?')
    bot.register_next_step_handler(message, new_line_notif)#следующий шаг диалога
    
def new_line_notif(message):
    Newhelper=User(message.text)#создаем нового юзера
    Newhelper.telegram_id=message.from_user.id
    Newhelper.telegram_username=message.from_user.username #заполняем поля известной инфой   
    user_dict[message.chat.id]=Newhelper #сохраняем в словаре по ключу-айди
    bot.send_message(message.chat.id, 'Выбери способ оповещений. 2 - юзер видит твое имя и пишет тебе сам, 1 - тебя оповещает бот, и ты отзываешься если можешь')
    bot.register_next_step_handler(message, new_line_taglist)#следующий шаг диалога
    
def new_line_taglist(message):
    if message.text not in ["1","2"]: # на случай если юзер написал что-то кроме 1 или 2
        bot.send_message(message.chat.id, 'Что-то пошло не так, напишите 1 или 2!')
        bot.register_next_step_handler(message, new_line_taglist)
        return
    Newhelper=user_dict[message.chat.id]#вызываем из словаря недозаполненного юзера
    Newhelper.notif=int(message.text) #добавляем метку нотификации
    bot.send_message(message.chat.id, 'Теги через пробел (потом тут будут кнопки(наверное))')
    bot.register_next_step_handler(message, end_of_procedure)#следующий шаг диалога
    
def end_of_procedure(message):
    Newhelper=user_dict[message.chat.id]#вызываем из словаря недозаполненного юзера
    Newhelper.taglist=message.text.split() #заполняем теглист листом строк-тегов
    #новые строчки в ббазе данных
    DB.new_entry(Newhelper) #метод для добавления новых строк
    #проверка вывода
    bot.send_message(message.chat.id, Newhelper.Userinfo() )#только для дебага

     
#список людей по метке нотификации например /base2 2
@bot.message_handler(commands=['base2'])
def handle_base(message):
    com=message.text.split(maxsplit=1) #Превратили строку в лист строк, чтобы отделить команду от параметров
    if com[1] in ["1","2"] and len(com)==2: #проверка формата команды - вдруг там не 1/2, или лишнего написано
        bot.send_message(message.chat.id, str(DB.select_notif_specified(com[1])))
        
#список людей по тегу и нотиф, например /base4 Вышмат 1
#Эта, как и те что ниже, работает примерно так же как и  handle_base (Какие-то не очень говорящие имена)
@bot.message_handler(commands=['base4'])
def extract_by_tag_notif(message):
    com=message.text.split(maxsplit=2)
    if len(com)==3:
        bot.send_message(message.chat.id, str(DB.select_tag_notif(com[1],com[2])))
        #bot.send_message(message.chat.id, str(com[1]))

#список людей по тегу например /base3 Вышмат
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
     
@bot.message_handler(commands=['halp'])
def halp(message):
    list_of_all_tags(message)
    bot.send_message(message.chat.id, 'Напиши мне тег, который тебя интересует')
    bot.register_next_step_handler(message, halp_step_two)
    
def halp_step_two(message):
    tags=sorted(DB.select_all_tags(),key= lambda x:x[0])
    tagslist=list()
    for tag in tags:
        tagslist.append(tag[0])
    if message.text.capitalize() in tagslist:
        bot.send_message(message.chat.id, 'Сейчас тебе всех сдам')
        return_by_tag(message)
    else:
        bot.send_message(message.chat.id, 'Такого тега нет, попробуйте еще раз!')
        bot.register_next_step_handler(message, halp_step_two)
        return

def return_by_tag(message):
    tag=message.text
    #bot.send_message(message.chat.id, 'Этим сам напишешь!')
    bot.send_message(message.chat.id, output_of_list(DB.select_usernames_when_notif_is_two(tag),'Можешь им написать сам \n',usernames=True))
    #пока так
    bot.send_message(message.chat.id, 'Эти тебе напишут (наверное)!')
    #bot.send_message(message.chat.id, str(DB.select_ids_when_notif_is_one(tag)))
    send_notifications(tag,message.from_user.username)

#код оповещения    
def send_notifications(tag,username):
    output='Привет! @'+username+' требуется помощь по теме "'+tag+'"! Напиши ему'
    users_id_list=DB.select_ids_when_notif_is_one(tag)
    for user_id in users_id_list:
        bot.send_message(int(user_id[0]), output)
    

#кол-во строчек в базе данных
@bot.message_handler(commands=['basetags'])
def list_of_all_tags(message):
    bot.send_message(message.chat.id, output_of_list(DB.select_all_tags(),'Вот список всех гендеров. \n','не мисгендерь!'))
"""  output='Вот список всех гендеров. \n'
    tags=sorted(DB.select_all_tags(),key= lambda x:x[0])#выдает таплы, поэтому сортируем хитро
    for tag in tags:
        output+='{} \n'.format(tag[0])
    output+='не мисгендерь!'"""
    
    
#функция для формирования строки со списком из запроса
#Необходима потому что запрос выдает данные как несортированный лист таплов, что не очень удобно
#Чтобы не повторять код, лучше написать отдельную функцию
#стр1 и стр2 - строки до и после уже сортированного списка
def output_of_list(dbresult,str1='',str2='',usernames= False):
    res=str1
    items=sorted(dbresult,key= lambda x:x[0])#выдает таплы, поэтому сортируем хитро
    for item in items:
        if usernames == True:
            res+='@'
        res+='{} \n'.format(item[0])
    res+=str2
    return res
'''
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
#чтобы мне в личку стучал если кто-то пишет
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
       
'''        


if __name__ == '__main__':
     bot.polling(none_stop=True)