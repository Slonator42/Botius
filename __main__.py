import os
import sqlite3
from datetime import datetime

import telebot
from telebot import types

TOKEN = os.getenv("TOKEN")

if isinstance(TOKEN, str):
    bot = telebot.TeleBot(TOKEN)
else:
    print("Токен не найден")

@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Запрос")
    markup.add(item1)
    bot.send_message(
        m.chat.id,
        'Нажмите кнопку "Запрос" для получения информации о днях рождениях на сегодня.',
        reply_markup=markup,
    )

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == "Запрос":
        # Узнаем текущую дату и месяц
        date = datetime.now().strftime("%d.%m")

        # Обращаемся к базе данных и создаем курсор
        prj_dir = os.getcwd()
        base_name = "People.sqlite3"
        connect = sqlite3.connect(os.path.join(prj_dir, base_name))
        cursor = connect.cursor()

        # Чтение данных
        sqlite_select_query = """SELECT * from People"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        count_people = 0
        birthday_list = []

        # Бот проверяет, есть ли день рождения
        for row in records:
            birthday = row[1][:5]  # Предполагается, что дата в формате 'dd.mm.yyyy'
            if birthday == date:
                count_people += 1
                birthday_list.append(row[0])  # Добавляем имя в список

        if count_people > 0:
            # Формируем сообщение с именами, каждое с новой строки и с нумерацией
            names_with_numbers = "\n".join(f"{i + 1}. {name}" for i, name in enumerate(birthday_list))
            bot.send_message(message.chat.id, f"Сегодня дней рождений {count_people}:\n{names_with_numbers}")
        else:
            bot.send_message(message.chat.id, "Сегодня дней рождений нет :(")

        # Закрытие базы
        cursor.close()

bot.polling(none_stop=True)