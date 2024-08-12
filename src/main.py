import os
import random
import sqlite3
from datetime import datetime

import telebot
from telebot import types

TOKEN = os.getenv("TOKEN")
if TOKEN is not None:
    bot = telebot.TeleBot(TOKEN)
else:
    raise ValueError("Токен не найден")

# Список поздравлений
congratulations = [
    "Поздравляем с днем рождения! Желаем здоровья, удачи, любви, везения, мира, добра, улыбок, благополучия. Пусть все мечты исполняются. Пусть жизнь будет долгой и гладкой, полной ярких и запоминающихся событий!",
    "Хочу пожелать тебе не просто благополучия и хорошей жизни, а еще и удачного стечения обстоятельств. Чтобы достижениями своими ты мог гордиться. Живи ярко и улыбайся каждый день!",
    "С днем рождения! Желаю добра, света, мира, улыбок, отличного настроения. Пусть всё плохое обходит стороной, жизненные невзгоды преодолеваются с легкостью, а каждый день будет наполнен радостью и счастьем. И конечно, светлой веры, огромной надежды, бесконечной любви.",
    "В день рождения желаю легкости чувств, душевной бодрости, ясности мыслей и ярких позитивных ощущений. Пусть жизненная энергия поможет достичь самых невероятных замыслов.",
    "Поздравляю с днем рождения! Пусть счастье сопровождает вас на каждом пути, здоровье оберегает при любых обстоятельствах. Удача и везение станут вашим надежным спутником по жизни. Желаю вдохновения во всем, позитивного настроения и исполнения всех планов."
    "Желаю здоровья и хорошего настроения, всех благ и удовольствий жизни, благополучия и домашнего уюта, любви и человеческого счастья!"
    "Пусть в твой день рождения все будет необыкновенным и замечательным, словно в волшебных сказках, случаются чудеса, а счастье будет прекрасном, как радуга!"
    "Желаю самые приятные минуты жизни разделить с любимым человеком, радоваться мгновениям волшебного счастья, быть желанным и нужным в любой компании!"
    "Пусть свет счастливой звезды ведет тебя навстречу радостным и интересным событиям, радужным надеждам и мечтам, к успеху и процветанию!"
    "Желаем уютной атмосферы в доме, любви и теплоты в отношениях, уважения и доверия в коллективе, счастливых и радостных лет жизни!"
    "Пусть добрый художник раскрашивает твою жизнь лишь светлыми красками, а дни приносят впечатления, которые хочется вспоминать. С днем рождения!",
]


@bot.message_handler(commands=["start"])
def handle_start_command(message):
    # Добавляем кнопки "Запрос" и "Получить поздравление"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    query_button = types.KeyboardButton("Запрос")
    congratulation_button = types.KeyboardButton("Получить идею для поздравления")
    keyboard.add(query_button, congratulation_button)

    welcome_message = "Привет! Выберите действие:"
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

    elif query_text == "Получить идею для поздравления":
        # Выбираем случайное поздравление из списка
        random_congratulation = random.choice(congratulations)

        # Отправляем поздравление пользователю
        bot.send_message(message.chat.id, random_congratulation)

    # После обработки текста отправляем клавиатуру снова без дополнительного сообщения
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    query_button = types.KeyboardButton("Запрос")
    congratulation_button = types.KeyboardButton("Получить идею для поздравления")
    keyboard.add(query_button, congratulation_button)

    bot.send_message(
        message.chat.id, " ", reply_markup=keyboard
    )  # Пустое сообщение для отображения клавиатуры


bot.polling(none_stop=True)
