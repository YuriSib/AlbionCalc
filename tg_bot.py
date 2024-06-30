import telebot
from telebot import types, logger

from config import BOT_TOKEN
from main import main


bot = telebot.TeleBot(token=BOT_TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Обновить таблицу")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     text="Запуск парсинга", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Обновить таблицу"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Обновить таблицу")
        markup.add(btn1)
        bot.send_message(message.chat.id, text="Данные будут обновляться около минуты, подождите.")
        main()
        bot.send_message(message.chat.id, text="Данные в таблицу успешно обновлены!", reply_markup=markup)


bot.polling(none_stop=True)
