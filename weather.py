import requests, json
import datetime
import time
from geopy import geocoders

API_KEY = "9ee48e4ff1867cd5496c2366f13fa950"

def getUtcUnixDate(dateString: str):
    dateArray = dateString.split(".")
    date = datetime.datetime(int(dateArray[2]), int(dateArray[1]), int(dateArray[0]), tzinfo=datetime.timezone.utc)

    return f"{round(datetime.datetime.timestamp(date))}"


def getGeolocation(city: str):
    geolocator = geocoders.Nominatim(user_agent="telegram_bot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    
    return str(round(float(latitude), 2)), str(round(float(longitude), 2))


def getCurrentUtcUnixDate():
    date = roundUtcUnixDateToDays(int(time.time()))
    return date

def roundUtcUnixDateToDays(date: int):
    date -= date % 60
    date -= date % (60 * 60)
    date -= date % (60 * 60 * 24)
    return date


def getWeather(city: str, date: str =None):
    latitudeAndLongtitude = getGeolocation(city)

    if (date is not None):
        userInputDate = datetime.timedelta(seconds=int(getUtcUnixDate(date)))
        currentDate = datetime.timedelta(seconds=getCurrentUtcUnixDate())
        oneDay = datetime.timedelta(days=1)

        if ((userInputDate <= currentDate) and (userInputDate >= currentDate - 5 * oneDay)):
            BASE_URL = "https://api.openweathermap.org/data/2.5/onecall/timemachine?"
            URL =   BASE_URL + "lat=" + latitudeAndLongtitude[0] + \
                    "&lon=" + latitudeAndLongtitude[1] + \
                    "&dt=" + int(getUtcUnixDate(date)) + \
                    "&appid=" + API_KEY + \
                    "&units=metric&lang=ru"
                    
            response = requests.get(URL)

            if response.status_code == 200:

                data = response.json()
                
                main = data['current']
                
                temperature = main['temp']
                
                humidity = main['humidity']
                
                pressure = main['pressure']

                report = main['weather']
                
                return f"{city:-^30}\n" + \
                        f"Температура: {temperature}\n" + \
                        f"Влажность: {humidity}%\n" + \
                        f"Давление: {pressure}\n" + \
                        f"Описание: {report[0]['description'].title()}"

            else:
                return "В твоём запросе есть ошибка"

        if ((userInputDate < currentDate - 5 * oneDay)):
            return "Смотреть погоду можно только на 5 дней назад от текущего."

        if ((userInputDate > currentDate) and (userInputDate <= currentDate + 7 * oneDay)):
            BASE_URL = "https://api.openweathermap.org/data/2.5/onecall?"
            URL =   BASE_URL + "lat=" + latitudeAndLongtitude[0] + \
                    "&lon=" + latitudeAndLongtitude[1] + \
                    "&appid=" + API_KEY + \
                    "&units=metric&lang=ru&exclude=current,minutely,hourly,alerts"
                    
            response = requests.get(URL)

            if response.status_code == 200:

                data = response.json()
                
                daily = data['daily']

                temperature = 0
                humidity = 0
                pressure = 0
                report = ""

                for day in daily:
                    if (roundUtcUnixDateToDays(day['dt']) == int(getUtcUnixDate(date))):
                        temperature = day['temp']['day']
                        humidity = day['humidity']
                        pressure = day['pressure']
                        report = day['weather']
                
                return f"{city:-^30}\n" + \
                        f"Температура: {temperature}\n" + \
                        f"Влажность: {humidity}%\n" + \
                        f"Давление: {pressure}\n" + \
                        f"Описание: {report[0]['description'].title()}"

            else:
                return "В твоём запросе есть ошибка."

        if ((userInputDate > currentDate + 7 * oneDay)):
            return "Смотреть погоду можно только на 7 дней вперёд от текущего."

    else:
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        URL =   BASE_URL + "q=" + city + \
                "&appid=" + API_KEY + \
                "&units=metric&lang=ru"

        response = requests.get(URL)

        if response.status_code == 200:
        
            data = response.json()
            
            main = data['main']
            
            temperature = main['temp']
            
            humidity = main['humidity']
            
            pressure = main['pressure']

            report = data['weather']


            return f"{city:-^30}\n" + \
                    f"Температура: {temperature}\n" + \
                    f"Влажность: {humidity}%\n" + \
                    f"Давление: {pressure}\n" + \
                    f"Описание: {report[0]['description'].title()}"

        else:
            return "В твоём запросе есть ошибка"