import telebot
from telebot import types
from settings import OPEN_WEATHER_TOKEN
import requests
import datetime

token = '5276898707:AAGRP_TsLPKpk30AK5VoDHnMb-TesKehMZU'
bot = telebot.TeleBot(token, parse_mode=None)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Напиши мне название города и я пришлю тебе сводку погоды в нем! ")


@bot.message_handler(content_types=['text'])
def send_message(message):
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
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={OPEN_WEATHER_TOKEN}&units=metric'
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


bot.polling()