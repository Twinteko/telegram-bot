from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)
from telegram import Update
import logging
from token1 import Token
import weather

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
    
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Привет, {update.effective_user.first_name}, чтобы узнать погоду нужно написать ' + \
                                '"/pogoda" и через пробел:\n1. Город (официальное назавание),\n' + \
                                '2. Пробел,\n3. Дата (Формат - день.месяц (цифрами)), максимум 5 дней назад.\n(Можно без даты, тогда получишь текущую погоду)')
    
    update.message.reply_text('Вот тебе пример: "/pogoda Санкт-Петерубрг" покажет текущую погоду в Питере.\n' + \
                                'А вот "/pogoda Санкт-Петерубрг 12.12" покажет погоду 12 декабря\n(Команду лучше не копировать)')

def getWeatherBot(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 1:
        update.message.reply_text('Ты не указал город, мужик')
        return "Прикол"
    
    update.message.reply_text('Смотрим погоду...')

    if len(context.args) > 1:
        response = weather.getWeather(context.args[0], context.args[1])

    else:
        response = weather.getWeather(context.args[0])
    
    update.message.reply_text(response)
    


def main() -> None:
    updater = Updater(token = Token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    getWeather_handler = CommandHandler('pogoda', getWeatherBot)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(getWeather_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()