import telebot
import xlrd
import xlwt
import os.path
from datetime import datetime
from xlutils.copy import copy
from auth import TOKEN

bot = telebot.TeleBot(TOKEN)
bot.delete_webhook()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    mes = """Здравствуйте, {0.first_name}
Это Ваш личный дневник питания. Напишите, что Вы съели и я сохраню это для Вас.
Что бы посмотреть ваш дневник, напишите 'посмотреть дневник'"""
    bot.send_message(message.chat.id, mes.format(message.from_user), parse_mode='html')


@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.chat.type == 'private':
        if message.text.lower() == "посмотреть дневник":
            if os.path.isfile(f'files/{message.chat.id}.xls'):
                f = open(f'files/{message.chat.id}.xls', 'rb')
                bot.send_document(message.chat.id, f)
            else:
                bot.send_message(message.chat.id, 'Вы еще ничего не ели!')
        else:
            create_file(message)
            my_book = xlrd.open_workbook(f'files/{message.chat.id}.xls', formatting_info=True)
            sheet = my_book.sheet_by_index(0)
            max_row = sheet.nrows
            max_col = 1
            today = datetime.today().date()
            try:
                date_in_table = sheet.cell_value(max_row - 2, 0)
                date_in_table = datetime(*xlrd.xldate.xldate_as_tuple(date_in_table, 0)).date()
                if today == date_in_table:
                    max_row = max_row - 2
                    max_col = sheet.row_len(max_row)
            except IndexError:
                pass
            style_date = xlwt.XFStyle()
            style_date.num_format_str = 'MM/DD/YYYY'
            style_time = xlwt.XFStyle()
            style_time.num_format_str = 'hh:mm'
            book = copy(my_book)
            sheet = book.get_sheet(0)
            sheet.write(max_row, 0, datetime.today().date(), style_date)
            sheet.write(max_row, max_col, datetime.today(), style_time)
            sheet.write(max_row + 1, max_col, message.text)
            book.save(f'files/{message.chat.id}.xls')
            bot.send_message(message.chat.id, 'Добавлено: ' + message.text)


def create_file(message):
    if not os.path.isfile(f'files/{message.chat.id}.xls'):
        rb = xlrd.open_workbook('files/diary.xls', on_demand=True, formatting_info=True)
        wb = copy(rb)
        wb.save(f'files/{message.chat.id}.xls')


bot.polling(none_stop=True)
