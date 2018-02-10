# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 00:00:51 2018

@author: VedMedk0
"""

import recommend
bot=recommend.bot
#код части с уведомлениями

@bot.message_handler(commands=['inote'])
def handle_inote(message):
     bot.send_message(message.chat.id, 'я сообщенька из части со второй части')