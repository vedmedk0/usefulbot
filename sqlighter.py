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
        
    def select_notif_specified(self, notif):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT telegram_id FROM helpers WHERE notification = {} '.format(notif)).fetchall()

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
        self.connection.close()