import telebot
from telebot import types

import re  # regexp

import api
import config

bot = telebot.TeleBot(config.bot_token)

conv_to = 'rub'
current = {}  # dict{user_id: conv_from}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton(text='Доллар USD')
    button2 = types.KeyboardButton(text='Евро EUR')
    button3 = types.KeyboardButton(text='Армянский драм AMD')
    button4 = types.KeyboardButton(text='Турецкая лира TRY')
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'Выбери валюту для конвертации в рубли', reply_markup=markup)


@bot.message_handler(content_types='text')
def receive_message(message):
    if message.text == 'Доллар USD':
        conv_from = 'usd'
    elif message.text == 'Евро EUR':
        conv_from = 'eur'
    elif message.text == 'Армянский драм AMD':
        conv_from = 'amd'
    elif message.text == 'Турецкая лира TRY':
        conv_from = 'try'
    else:
        if not message.from_user.id in current:
            bot.send_message(message.chat.id, 'Выбери валюту!')
            return
        else:
            conv_from = current[message.from_user.id]
            process_message(message, conv_from)
    current[message.from_user.id] = conv_from
    bot.send_message(message.chat.id, 'Введи сумму')


def process_message(message: telebot.types.Message, conv_from: str):
    """Process the text of the message and send a response to the chat."""
    text = re.findall('\d+|\.\d+|\,\d+', message.text)  # regexp - looking for numbers, dots and commas
    if len(text) < 1:  # list of relevant symbols
        bot.send_message(message.chat.id, 'Цифры где?')  # no numbers in the message
        return
    amount = ''.join(text)  # make a string from the list
    if str.count(amount, '.') + str.count(amount, ',') > 1:  # count the number of "."
        bot.send_message(message.chat.id, f'{amount}? Зачем столько точек')
        return
    if int(amount) <= 0:
        bot.send_message(message.chat.id, f'{amount}? Так нельзя')
        return
    result = api.get_result(conv_to, conv_from, amount)
    bot.send_message(message.chat.id, f'{result} рублей')


bot.polling(none_stop=True)
