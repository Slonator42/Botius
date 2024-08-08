Для того, чтобы работать с GitHub через VSC:
   1) Нужно установить git (https://git-scm.com/)
   2) Установить плагин (vscode:extension/GitHub.vscode-pull-request-github)
   3) Start a new Terminal and configure your ‘user.name’ and ‘user.email’ in git with the help of the following commands. git config user.email “you@example.com” git config user.name “Your Name”

After configuring your details, you can check by using the following command. git config –global –list
   4) Клонировать репозиторий с проектом
   5) При работе с проектом, синхронизировать его с Git
   https://www.geeksforgeeks.org/how-to-add-git-credentials-in-vscode/

  Чтобы подключиться к Excel таблице нужно:
   1) Подготовить таблицу, убрать ненужные данные
   2) Установить Sqlite3 
   3) Установить Openpyxl
   4) Сделать код на основе    https://www.pyblog.ru/post/exportxlssql/



   https://pythonru.com/biblioteki/poluchenie-dannyh-iz-tablicy-sqlite



   
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