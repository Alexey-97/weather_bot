from aiogram import Dispatcher, Bot, executor, types
import logging
import requests
from pprint import *
import datetime


open_weather_token = 'Токен сайта'

logging.basicConfig(level=logging.INFO)
bot = Bot(token="Токен бота")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def comand_start(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет назови город и я скажу какая там погода!")


@dp.message_handler()
async def get_weather(message: types.Message):
    """Функция обращается по API к openweathermap.org
    и выводит полученую погоду в телеграм боте """
    smile = {
        'clear': 'Ясно \U00002600',
        'clounds': 'Облачно \U00002601',  # словарь с смайлами для погоды
        'Rain': 'Дождь \U00002614',
        'thunderstorm': 'Гроза \U000026A1'
    }
    try:
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&limit=1&appid={open_weather_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        cur_weather = data['main']['temp']
        weather_descriptions = data['weather'][0]['main']
        if weather_descriptions in smile:
            wd = smile[weather_descriptions]
        else:
            wd = ""

        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(
            data['sys']['sunrise']
        )
        await message.reply(f'Погода в городе: {city}\nТемпература воздуха: {cur_weather} С° {wd} \nВлажность воздуха {humidity}  %\n'
                            f'Скоость ветра: {wind} м\c\nВремя рассвета: {sunrise_timestamp}\nХорошего дня!'
                            )
    except Exception:
        await message.reply("Город введён не коректно")


if __name__ == "__main__":
    executor.start_polling(dp)
