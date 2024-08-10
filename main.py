import os
import sqlite3
from datetime import datetime

import telebot
from telebot import types

TOKEN = os.getenv("TOKEN")
if TOKEN is not None:
    bot = telebot.TeleBot(TOKEN)
if isinstance(TOKEN, str):
    bot = telebot.TeleBot(TOKEN)
else:
    raise ValueError("Токен не найден")


@bot.message_handler(commands=["start"])
def handle_start_command(message):
    # Добавляем две кнопки
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    query_button = types.KeyboardButton("Запрос")
    keyboard.add(query_button)

    welcome_message = "Привет! Нажмите кнопку «Запрос» для получения информации о днях рождениях на сегодня."
    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    query_text = message.text.strip()

    if query_text == "Запрос":
        # Узнаем текущую дату и месяц
        current_date = datetime.now().strftime("%d.%m")

        # Обращаемся к базе данных и создаем курсор
        project_directory = os.getcwd()
        database_name = "People.sqlite3"
        database_path = os.path.join(project_directory, database_name)

        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Чтение данных
        select_query = "SELECT * FROM People"
        cursor.execute(select_query)

        records = cursor.fetchall()

        count_people = 0
        birthday_names = []

        # Бот проверяет, есть ли день рождения
        for record in records:
            birthday = record[1][:5]
            if birthday == current_date:
                count_people += 1
                birthday_names.append(record[0])

        if count_people > 0:
            # Формируем сообщение с именами, каждое с новой строки и с нумерацией
            birthday_message = "\n".join(
                f"{index + 1}. {name}" for index, name in enumerate(birthday_names)
            )
            bot.send_message(
                message.chat.id,
                f"Сегодня дней рождений {count_people}:\n{birthday_message}",
            )
        else:
            bot.send_message(message.chat.id, "Сегодня дней рождений нет :(")

        # Закрытие базы
        cursor.close()
        connection.close()


bot.polling(none_stop=True)
