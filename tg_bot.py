import telebot as telebot
from telebot import types
from settings import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # img = open('hello.png', 'rb')
    # bot.send_sticker(message.chat.id, img)

    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn1 = types.KeyboardButton(BTN_DOC['text'])
    # btn2 = types.KeyboardButton(BTN_REV['text'])
    # btn3 = types.KeyboardButton(BTN_NEW_ITEM['text'])
    # markup.add(btn1, btn2, btn3)

    bot.reply_to(message, 'Привет! Это твой личный помощник. Чего изволите?', reply_markup=markup)