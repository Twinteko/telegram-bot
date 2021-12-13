import requests, json
import datetime
from geopy import geocoders

API_KEY = "9ee48e4ff1867cd5496c2366f13fa950"

def getUtcUnixDate(dateString: str):
    dateArray = dateString.split(".")
    date = datetime.datetime(2021, int(dateArray[1]), int(dateArray[0]), tzinfo=datetime.timezone.utc)

    return f"{round(datetime.datetime.timestamp(date))}"


def getGeolocation(city: str):
    geolocator = geocoders.Nominatim(user_agent="telegram_bot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    
    return str(round(float(latitude), 2)), str(round(float(longitude), 2))


def kelvinToCelsius(temp):
    return round(temp-273.15, 3)


def getWeather(city: str, date: str =None):
    latitudeAndLongtitude = getGeolocation(city)

    if(date is not None):
        BASE_URL = "https://api.openweathermap.org/data/2.5/onecall/timemachine?"
        URL =   BASE_URL + "lat=" + latitudeAndLongtitude[0] + \
                "&lon=" + latitudeAndLongtitude[1] + \
                "&dt=" + getUtcUnixDate(date) + \
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

            print(f"{city:-^30}")
            print(f"Температура: {temperature}")
            print(f"Влажность: {humidity}%")
            print(f"Давление: {pressure}s")
            print(f"Описание: {report[0]['description'].title()}")

        else:
            print("Где-то ошибка")

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

            print(f"{city:-^30}")
            print(f"Температура: {temperature}")
            print(f"Влажность: {humidity}%")
            print(f"Давление: {pressure}")
            print(f"Описание: {report[0]['description'].title()}")

        else:
            print("Где-то ошибка")
    

getWeather("Санкт-Петербург", "10.12")
getWeather("Санкт-Петербург")