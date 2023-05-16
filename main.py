import telebot
from telebot import types
import random
import xlrd

TOKEN = '5800444955:AAG5UNnWzS_DVUYKPgAdhkJXRIak83QjJCs'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # клавиатура
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("кнопка1")
    but2 = types.KeyboardButton("кнопка2")
    markup.add(but1, but2)

    bot.reply_to(message, "Здравствуй, {0.first_name}\nСмотрю, ты за Единую, Великую и Недилимую".format(message.from_user),
                 parse_mode='html',
                 reply_markup=markup)
    bot.send_message('hello')


if __name__ == '__main__':
    pass
