import telebot
from time import time
import random
import asyncio
from telebot import types
#from esphome2 import serv
import esphome2 as esp
#from esphome2 import sensor
#from imp import reload
import importlib as rel
import sqlite3


spis = ('не понимаю о чем речь','выражайтесь точнее','это не то что нужно','что еще скажете','тут я вам ничего не скажу','введите pip')
otvet = ('привет','пока','как дела','ты кто')
otvet2 = {"Приветствие":"Привет","Прощание":"До скорой встречи"}
cave = []
#sensor = 29
ds18 = 27.0
bot = telebot.TeleBot('6152936632:AAH6tzrKB22bJmpGJXMLoGJ3VuTYtN9psXk')
GROUP_ID = -834972694

#@bot.message_handler(content_types=['photo'])
@bot.message_handler(commands=['start'])
def get_photo(message):

    markup = types.InlineKeyboardMarkup()
    btn3 = types.InlineKeyboardButton('Получить значение с датчика', callback_data='temp')
    markup.row(btn3)
    btn1 = types.InlineKeyboardButton('Включить свет', callback_data='on')
    btn2 = types.InlineKeyboardButton('Выключить свет', callback_data='off')
    markup.row(btn1, btn2,)
    btn4 = types.InlineKeyboardButton('очистить сеанс', callback_data='delete')
    markup.row(btn4)
    bot.send_message(message.chat.id, 'Выбрать действие', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):

    if callback.data == 'on':
        asyncio.run(esp.serv(deb = True))
        bot.send_message(callback.message.chat.id, 'Выполнено')
    elif callback.data == 'off':
        asyncio.run(esp.serv(deb=False))
        bot.send_message(callback.message.chat.id, 'Выполнено')
    elif callback.data == 'temp':
        #asyncio.run(esphome2.serv())
        rel.reload(esp)
        bot.send_message(callback.message.chat.id, f'{esp.sensor}')
    elif callback.data =='delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)



@bot.message_handler(commands=['help'])
def maine(message):
    print(message)
    #asyncio.run(serv(deb = True))
    conn = sqlite3.connect('sostoyanie.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()
    #bot.send_message(message.chat.id, f'Привет {message.from_user.first_name},запускаю скрипт удаление вашего аккаунта...')
@bot.message_handler(commands=['stop'])
def maine2(message):
    print(message)
    #asyncio.run(serv(deb = False))



@bot.message_handler(func=lambda message: message.entities is not None)  # and message.chat.id == GROUP_ID)
def delete_links(message):
    print(message)
    for entity in message.entities:
        print('wot')
        if entity.type in ["url", "text_link"]:
            print('helo')
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f'{message.from_user.first_name} {message.from_user.last_name},ссылки не одобряю😡')


@bot.message_handler()
def info(message):
    g = message
    global spis
    global otvet
    #global deb
    cach = open ('cachfile.txt', 'a')
    cach.write(message.text + '\t')
    cach.write(message.from_user.first_name + '\n')


    cach.close()

    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}👋, введите "pip"')

    #elif message.text.lower() == "включи":
    #    deb = True
    #    asyncio.run(main())
    #elif message.text.lower() == 'выключи':
    #    deb = False
    #    asyncio.run(main())

    elif message.text.lower() == 'pip':
        print(message.from_user.id)
        bot.restrict_chat_member(message.chat.id,message.from_user.id, until_date=time() + 600)
        bot.send_message(message.chat.id, f'Пользователь, {message.from_user.first_name} заблокирован на 10 минут')
    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name} {random.choice(list(spis))}🤔')




if __name__ == "__main__":
    bot.infinity_polling()
#bot.polling(none_stop=True)