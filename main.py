from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
from token1 import Token
import weather

bot = Bot(token=Token)
dp = Dispatcher(bot)

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
    
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(f'Привет, чтобы узнать погоду нужно написать:\n' + \
                         '1. Город (официальное назавание),\n' + \
                         '2. Пробел,\n' + \
                         '3. Дата (Формат - день.месяц.год (цифрами)), максимум 5 дней назад и 7 дней вперёд от текущего дня.\n' + \
                         '(Можно без даты, тогда получишь текущую погоду)')
    
    await message.answer('Вот тебе пример: "Санкт-Петерубрг" покажет текущую погоду в Питере.\n' + \
                        'А вот "Санкт-Петерубрг 10.12.2022" покажет погоду 10 декабря 2022 года\n')

@dp.message_handler()
async def getWeatherBot(message: types.Message):
    if len(message.text.split(" ")) < 1:
        message.answer('Ты не указал город, мужик')
        return "Прикол"
    
    await message.answer('Смотрим погоду...')

    try:
        if len(message.text.split(" ")) > 1:
            response = weather.getWeather(message.text.split(" ")[0], message.text.split(" ")[1])
        else:
            response = weather.getWeather(message.text.split(" ")[0])
    
        await message.answer(response)
    except:
        await message.answer("В твоём запросе есть ошибка")

if __name__ == '__main__':
    executor.start_polling(dp)