import requests
from models import Weather,City


def getWeatherByCity(cityName,cityPk):
    url_params = {"appid": "1bc109621e2f9052ace74536aee024ef", "units": "metric", "lang": "fr"}
    query = "http://api.openweathermap.org/data/2.5/weather?q=" + cityName
    req = requests.get(query, params=url_params)
    data = req.json()
    weather = Weather.objects.create()
    weather.humidity = data["main"]["humidity"]
    weather.temp_min = data["main"]["temp_min"]
    weather.temp_max = data["main"]["temp_max"]
    weather.visibility = data["visibility"]
    weather.wind_speed = data["wind"]["speed"]
    weather.save()
    city = City.objects.get(pk=cityPk)
    city.weather = weather
    city.save()
