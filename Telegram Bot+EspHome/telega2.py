import telebot
from Secrets import bot_api, secret_comand
from time import time
import random
from telebot import types
import esphome2 as esp
import importlib as rel
import sqlite3
from device import Light, Wled

spis = ('Не понимаю о чем речь', 'Просьба выражатся точнее',
        'Это не то что нужно', 'Что еще скажете', 'еще немного',
        'Тут я вам ничего не скажу', 'Введите pip', 'почти угадал')

bot = telebot.TeleBot(bot_api)
GROUP_ID = -834972694


def buttons(message):
    markup = types.InlineKeyboardMarkup()
    btn3 = types.InlineKeyboardButton('Получить значение с датчика', callback_data='temp')
    markup.row(btn3)
    btn1 = types.InlineKeyboardButton('Включить свет', callback_data='on')
    btn2 = types.InlineKeyboardButton('Выключить свет', callback_data='off')
    markup.row(btn1, btn2)
    btn4 = types.InlineKeyboardButton('Включить Wled', callback_data='wled_on')
    btn5 = types.InlineKeyboardButton('Выкл Wled', callback_data='wled_off')
    markup.row(btn4, btn5)
    bot.send_message(message.chat.id, 'Выбрать действие', reply_markup=markup)


def buttons2(callback):
    markup = types.InlineKeyboardMarkup()
    btn6 = types.InlineKeyboardButton('20%', callback_data='20')
    btn7 = types.InlineKeyboardButton('70%', callback_data='70')
    btn8 = types.InlineKeyboardButton('100%', callback_data='100')
    markup.row(btn6, btn7, btn8)
    bot.send_message(callback.message.chat.id, 'Установи яркость(по умолчанию 50%)', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'on':
        buttons2(callback)
        Light(4244719125, True, 0.5)
        bot.send_message(callback.message.chat.id, 'Подсветка рабочей зоны ВКЛ')
    elif callback.data == 'off':
        Light(4244719125, False, 0.0)
        bot.send_message(callback.message.chat.id, 'Подсветка рабочей ВЫКЛ')
    elif callback.data == 'temp':
        rel.reload(esp)
        bot.send_message(callback.message.chat.id, f'{esp.sensor}')
    elif callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback.data == '20':
        bot.send_message(callback.message.chat.id, 'Установлено 20%')
        Light(4244719125, True, 0.2)
    elif callback.data == '70':
        bot.send_message(callback.message.chat.id, 'Установлено 50%')
        Light(4244719125, True, 0.5)
    elif callback.data == '100':
        bot.send_message(callback.message.chat.id, 'Установлено 90%')
        Light(4244719125, True, 0.9)
    elif callback.data == 'wled_on':
        Wled(True, 255)
        bot.send_message(callback.message.chat.id, 'Wled включился')
    elif callback.data == 'wled_off':
        Wled(False, 0)
        bot.send_message(callback.message.chat.id, 'Wled выкл')


@bot.message_handler(commands=['help'])
def maine(message):
    print(message)
    conn = sqlite3.connect('sostoyanie.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key,'
                'name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()


@bot.message_handler(func=lambda message: message.entities is not None)  # and message.chat.id == GROUP_ID)
def delete_links(message):
    print(message)
    for entity in message.entities:
        print('wot')
        if entity.type in ["url", "text_link"]:
            print('helo')
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f'{message.from_user.first_name}'
                                              f' {message.from_user.last_name},ссылки не одобряю😡')


@bot.message_handler()
def info(message):
    global spis
    cach = open('cachfile.txt', 'a')
    cach.write(message.text + '\t')
    cach.write(message.from_user.first_name + '\n')
    cach.close()

    if message.text.lower() == secret_comand:
        buttons(message)
    elif message.text.lower() == "привет":
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}👋, введите "pip"')
    elif message.text.lower() == 'pip':
        print(message.from_user.id)
        bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time() + 300)
        bot.send_message(message.chat.id, f'Пользователь, {message.from_user.first_name} заблокирован на 10 минут')
    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name} {random.choice(list(spis))}🤔')


if __name__ == "__main__":
    bot.polling(none_stop=True)
