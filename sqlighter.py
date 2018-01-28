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
            return self.cursor.execute('SELECT DISTINCT helptags FROM helpers ').fetchall()
        
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
        



        
    def select_ids_when_notif_is_one(self, tag):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute("SELECT DISTINCT Telegram_id FROM helpers WHERE helptags = '{}' AND notification = 1 ".format(tag)).fetchall()
        
        
    def select_usernames_when_notif_is_two(self, tag):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute("SELECT DISTINCT Telegram_username FROM helpers WHERE helptags = '{}' AND notification = 2 ".format(tag)).fetchall()





       
    def select_single(self, rownum):
        """ Получаем одну строку с номером rownum """
        with self.connection:
            return self.cursor.execute('SELECT * FROM helpers WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        """ Считаем количество строк """
        with self.connection:
            result = self.cursor.execute('SELECT * FROM helpers').fetchall()
            return len(result)
        

    def close(self):
        """ Закрываем текущее соединение с БД """
        #self.connection.commit()
        self.connection.close()