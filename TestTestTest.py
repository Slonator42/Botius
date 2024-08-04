import telebot
import threading
import time
from telebot import types
import sqlite3
import os
import datetime

TOKEN = '7348645445:AAHB1wjJz5tqDcqOxZNxipYtprbRdohJRyA'
bot = telebot.TeleBot(TOKEN)

# def send_welcome(message):
#     # Создаем клавиатуру
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     start_button = types.KeyboardButton("Старт")
#     keyboard.add(start_button)

#     # Отправляем приветственное сообщение с кнопкой
#     bot.send_message(message.chat.id, "Добро пожаловать! Нажмите 'Старт' для продолжения.", reply_markup=keyboard)

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     if message.text == "Старт":
#         bot.send_message(message.chat.id, "Вы нажали кнопку 'Старт'. Бот готов к работе!")
#     else:
#         bot.send_message(message.chat.id, "Пожалуйста, нажмите 'Старт' для начала.")

@bot.message_handler(commands=["start"])
def start(m, res=False):
        # Добавляем две кнопки
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Запрос")
        markup.add(item1)
        bot.send_message(m.chat.id, 'Нажмите кнопку "Запрос" для получения информации о днях рождениях на сегодня.',  reply_markup=markup)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Если юзер прислал 1, выдаем ему случайный факт
    if message.text.strip() == 'Запрос' :
            
        # узнаем текущую дату и месяц
        date = '{date:%d.%m}'.format( date=datetime.datetime.now() )

        # обращаемся к базе данных и создаем курсор
        prj_dir = os.path.abspath(os.path.curdir) 
        base_name = 'People.sqlite3'
        connect = sqlite3.connect(prj_dir + '/' + base_name)
        cursor = connect.cursor()

        # чтение данных
        sqlite_select_query = """SELECT * from People"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()


        #print(records)
        #print("Всего строк:  ", len(records))
        #print("Вывод каждой строки")
        #date = "13.11"

        #Бот проверяет есть ли 
        for row in records:
            have_a_birthday = 0
            #print("Имя:", row[0])
            #print("Дата:", row[1])
            birthday = row[1][:5]
            #print(birthday)
            if birthday == date:
                #print(row[0])
                answer = row[0]
                have_a_birthday = 1
                bot.send_message(message.chat.id, answer) 
        if have_a_birthday == 0:
            #print('Сегодня дней рождений нет :(')
            answer = 'Сегодня дней рождений нет :('
            bot.send_message(message.chat.id, answer)
        # закрытие базы
        cursor.close()



    # Отсылаем юзеру сообщение в его чат
    #bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)

