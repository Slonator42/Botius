import sqlite3
import os
import datetime

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

for row in records:
    have_a_birthday = 0
    #print("Имя:", row[0])
    #print("Дата:", row[1])
    birthday = row[1][:5]
    #print(birthday)
    if birthday == date:
        print(row[0])
        have_a_birthday = 1 
if have_a_birthday == 0:
    print('Сегодня дней рождений нет :(')

# закрытие базы
cursor.close()