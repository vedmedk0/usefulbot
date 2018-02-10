# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 01:40:42 2017

@author: VedMedk0
"""

import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread = False)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM helpers ').fetchall()
        
    def select_all_tags(self):
        """ Получаем все теги """
        with self.connection:
            a = self.cursor.execute('SELECT DISTINCT helptags FROM helpers ').fetchall()
            return sorted([i[0] for i in a])
        
    def new_entry(self, User):
        with self.connection:
            for tag in User.taglist:
                self.cursor.execute("INSERT INTO helpers (Telegram_id, Telegram_username, Name, helptags, notification) VALUES ({},'{}','{}','{}',{}); ".format(User.telegram_id, User.telegram_username, User.name, tag.capitalize(), User.notif))
        
    def select_notif_specified(self, notif):
        """ Получаем юзернейм тех, у кого 1 или 2"""
        with self.connection:
            return self.cursor.execute('SELECT DISTINCT Telegram_username FROM helpers WHERE notification = {} '.format(notif)).fetchall()
        
    def select_tag_specified(self, tag):
        """ Получаем по тегу """
        with self.connection:
            return self.cursor.execute("SELECT DISTINCT Telegram_username FROM helpers WHERE helptags = '{}'".format(tag)).fetchall()
        
    def select_tag_notif(self, tag, notif):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute("SELECT DISTINCT Telegram_id FROM helpers WHERE helptags = '{}' AND notification = {} ".format(tag,notif)).fetchall()
        
        
    def top_ten_tags(self):
        """десятка самых популярных тегов"""
        with self.connection:        
            a = self.cursor.execute('SELECT helptags FROM helpers group by helptags ORDER BY COUNT(helptags) desc').fetchall()    
            return [i[0] for i in a][:10]
    #Информация обо мне    
        
    def mytags_list(self, userid):
        """теги по ид """
        with self.connection:
            a=self.cursor.execute("SELECT DISTINCT helptags FROM helpers WHERE Telegram_id = '{}'".format(userid)).fetchall()
            return sorted([i[0] for i in a])

    def mynotif(self, userid):
        """ notif по ид """
        with self.connection:
            return self.cursor.execute("SELECT DISTINCT notification FROM helpers WHERE Telegram_id = '{}'".format(userid)).fetchall()[0][0]
        
    def myname(self, userid):
        """ имя по ид """
        with self.connection:
            return self.cursor.execute("SELECT DISTINCT Name FROM helpers WHERE Telegram_id = '{}'".format(userid)).fetchall()[0][0]
        
    def is_in_base(self, userid):
        with self.connection:
            return 0 != len(self.cursor.execute("SELECT DISTINCT helptags FROM helpers WHERE Telegram_id = '{}'".format(userid)).fetchall())
        
        
    #Изменения в таблице
    def change_notif(self, userid,notif):
        """ изменить notif по ид """
        with self.connection:
            return self.cursor.execute("UPDATE helpers SET notification = {} WHERE Telegram_id = '{}'".format(notif,userid))
        
    def del_tag(self, userid,tag):
        """ удалить тег """
        with self.connection:
            return self.cursor.execute("DELETE FROM helpers WHERE Telegram_id='{}' AND helptags = '{}'".format(userid,tag))
        
        
        
        
    


    #Используются для отбора двух типов людей  
    def select_ids_when_notif_is_one(self, tag):
        """ Получаем все строки """
        with self.connection:
            a = self.cursor.execute("SELECT DISTINCT Telegram_id FROM helpers WHERE helptags = '{}' AND notification = 1 ".format(tag)).fetchall()
            return sorted([i[0] for i in a])

        
    def select_usernames_when_notif_is_two(self, tag):
        """ Получаем все строки """
        with self.connection:
            a = self.cursor.execute("SELECT DISTINCT Telegram_username FROM helpers WHERE helptags = '{}' AND notification = 2 ".format(tag)).fetchall()
            return sorted([i[0] for i in a])
        
    def select_usernames_names_when_notif_is_two(self, tag):
        """ Получаем все строки """
        with self.connection:
            a = self.cursor.execute("SELECT DISTINCT Telegram_username, Name FROM helpers WHERE helptags = '{}' AND notification = 2 ".format(tag)).fetchall()
            a = sorted(a,key = lambda x:x[0])
            return [i[0]+' - '+i[1] for i in a]


    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM helpers').fetchall()
            return len(result)
        

    def close(self):
        """ Закрываем текущее соединение с БД """
        #self.connection.commit()
        self.connection.close()