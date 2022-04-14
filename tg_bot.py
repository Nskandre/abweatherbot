import telebot
from telebot import types
from settings import OPEN_WEATHER_TOKEN, TG_TOKEN
import requests
import datetime
from utils import create_button

# token = '5276898707:AAGRP_TsLPKpk30AK5VoDHnMb-TesKehMZU'
bot = telebot.TeleBot(TG_TOKEN, parse_mode=None)

BTN_MSK = create_button('msk', 'Москва')
BTN_SPB = create_button('spb', 'Санкт-Петербург')
BTN_EKB = create_button('ekb', 'Екатеринбург')
# BTN_OTHER = create_button('other', 'Другой город')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Москва') # callback_data='Moscow')
    btn2 = types.KeyboardButton('Санкт-Петербург') #, 'Saint Petersburg')
    btn3 = types.KeyboardButton('Екатеринбург') #, 'Ekaterinburg')
    # btn4 = types.KeyboardButton('Другой город')  # , 'Other')
    markup.add(btn1, btn2, btn3) #, btn4)

    bot.reply_to(message, "Привет! Выбери город или напиши его название и получи сводку погоды!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text == BTN_MSK['text']:
        city = 'Moscow'
    elif message.text == BTN_SPB['text']:
        city = 'Saint Petersburg'
    elif message.text == BTN_EKB['text']:
        city = 'Ekaterinburg'
    else:
        city = message.text


    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_TOKEN}&units=metric'
        )
        data = r.json()

        user_city = data['name']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        wind = data['wind']['speed']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length = sunset - sunrise

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно, не пойму, что там за погода!'

        bot.send_message(message.chat.id, f'''{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} Погода в {user_city}: 
            {wd}
            Температура: {temp} °C
            Ощущается как: {feels_like} °C
            Скорость ветра {wind} м/c
            Влажность {humidity} %
            Давление {round(pressure / 1.33322387415)} мм.рт.ст
            Восход {sunrise} 
            Закат {sunset}
            Продолжительность дня {length}''')

    except:
        bot.send_message(message.chat.id, '\U00002620 Проверьте название города \U00002620')
