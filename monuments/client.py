import requests
from monuments.models import *
from monuments.serializers import WeatherSerializer


def getWeatherByCity(cityName, cityPk):
    url_params = {"appid": "1bc109621e2f9052ace74536aee024ef", "units": "metric", "lang": "fr"}
    query = "http://api.openweathermap.org/data/2.5/weather?q=" + cityName
    req = requests.get(query, params=url_params)
    data = req.json()
    city = City.objects.get(pk=cityPk)
    weather = Weather.objects.create()
    weather.humidity = data["main"]["humidity"]
    weather.temp_min = data["main"]["temp_min"]
    weather.temp_max = data["main"]["temp_max"]
    weather.visibility = data["visibility"]
    weather.wind_speed = data["wind"]["speed"]
    weather.main = data["weather"][0]["main"]
    weather.description = data["weather"][0]["description"]
    weather.city = city
    weather.save()