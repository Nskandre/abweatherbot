import requests
import datetime
from pprint import pprint
from settings import OPEN_WEATHER_TOKEN
# from tg_bot import CITY


def get_weather(city, OPEN_WEATHER_TOKEN):

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
        # pprint(data)

        user_city = data['name']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        # weather = data['weather']['description']
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

        print(f'''{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} Погода в {user_city}: 
        {wd}
        Температура: {temp} °C
        Ощущается как: {feels_like} °C
        Скорость ветра {wind} м/c
        Влажность {humidity} %
        Давление {round(pressure / 1.33322387415)} мм.рт.ст
        Восход {sunrise} 
        Закат {sunset}
        Продолжительность дня {length} 
        
        Отличного Вам дня!!!''')

    except Exception as ex:
        print(ex)
        print('Проверьте название города')


def main():
    city = input('Введите город (на латинице): ')
    get_weather(city, OPEN_WEATHER_TOKEN)

if __name__ == '__main__':
    main()

# main()