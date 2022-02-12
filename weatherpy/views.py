import requests
import datetime
import time
import random

from django.shortcuts import render
from .forms import WeatherForm, UserMessage


def home(request):
    return render(request, 'weatherpy/home.html')


def weather(request):
    '''
    Fetchs weather data from openweathermap.

    There are two APIs for this, one that returns current weather and accepts
    location names as 'query' and another that only accepts lat/lon coordinates
    but returns more data ('onecallapi').

    One solution was, when needed, call the first API to get coordinates for a
    location and use it as arguments to call the 'onecallapi'.

    We also have two functions, json_extractor() which extracts current weather
    data and forecast_data() just for forecast weather.

    '''

    def forecast_data(json_index):
        '''
        Fetches the 7-day forecast data and converts it into usable data

        '''
        epoch = jsonier_onecallapi.get('daily')[json_index].get('dt')
        weekday = time.strftime('%A', time.localtime(epoch))
        day_temp = int(jsonier_onecallapi.get('daily')[
                       json_index].get('temp', {}).get('max'))
        day_weather_lower = jsonier_onecallapi.get('daily')[json_index].get(
            'weather')[0].get('main')
        day_weather = day_weather_lower.title()

        return weekday, day_temp, day_weather

    def json_extractor(json_obj, dict_key):
        '''
        Iterates over dict to get values
        '''

        value_list = []

        def json_iterator(json_obj, value_list, dict_key):

            if isinstance(json_obj, dict):
                for key, value in json_obj.items():
                    if isinstance(value, (dict, list)):
                        json_iterator(value, value_list, dict_key)
                    elif key == dict_key:
                        value_list.append(value)

            elif isinstance(json_obj, list):
                for item in json_obj:
                    json_iterator(item, value_list, dict_key)

            return value_list

        values = json_iterator(json_obj, value_list, dict_key)
        return values

    loc = request.POST.get('name')

    if loc == None:
        return render(request, 'weatherpy/weather_404.html')

    loc_upper = loc.title()

    # call for 'normal' API
    api = os.getenv('openweatherapi')
    address = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        loc + "&appid=" + api
    address_get = requests.get(address)
    jsonier = address_get.json()

    if jsonier.get('cod') == '404' or jsonier.get('cod') == '400':
        return render(request, 'weatherpy/weather_404.html')

    # call for 'onecallapi'
    lat = str(jsonier.get("coord", {}).get("lat"))
    lon = str(jsonier.get("coord", {}).get("lon"))
    onecallapi = "https://api.openweathermap.org/data/2.5/onecall?lat=" + \
        lat + "&lon=" + lon + "&exclude=&appid=81c4f61189c578db351b6f68d93ba526&units=metric"

    onecallapi_get = requests.get(onecallapi)
    jsonier_onecallapi = onecallapi_get.json()

    weather_list = (jsonier.get("weather"))[0]
    weather_get = weather_list.get('description')
    weather = weather_get.title()
    temp = int(jsonier.get("main", {}).get("temp"))
    temp_feel = int(
        (jsonier.get("main", {}).get("feels_like")))
    min_temp = int(jsonier.get("main", {}).get("temp_min"))
    max_temp = int(jsonier.get("main", {}).get("temp_max"))
    pressure = jsonier.get("main", {}).get("pressure")
    humidity = jsonier.get("main", {}).get("humidity")
    visibility = jsonier.get("visibility")
    wind_spd = jsonier.get("wind", {}).get("speed")
    wind_direction = jsonier.get("wind", {}).get("deg")
    gusts = jsonier.get("wind", {}).get("gust")
    clouds = jsonier.get("clouds", {}).get("all")
    country_code = jsonier.get("sys", {}).get("country")

    # sunrise
    epoch_sunrise = int(jsonier.get("sys", {}).get("sunrise"))
    sunrise_hour = time.strftime('%H', time.localtime(epoch_sunrise))
    sunrise_min = time.strftime('%M', time.localtime(epoch_sunrise))
    sunrise = sunrise_hour + ":" + sunrise_min

    # sunset
    epoch_sunset = int(jsonier.get("sys", {}).get("sunset"))
    sunset_hour = time.strftime('%H', time.localtime(epoch_sunset))
    sunset_min = time.strftime('%M', time.localtime(epoch_sunset))
    sunset = sunset_hour + ":" + sunset_min

    icon_number = jsonier.get("weather")[0].get('icon')
    degree = '°'

    daily_temp_data = jsonier_onecallapi.get("daily")[0]
    morning_temp = int(daily_temp_data.get('temp', {}).get('morn'))
    day_temp = int(daily_temp_data.get('temp', {}).get('day'))
    evening_temp = int(daily_temp_data.get('temp', {}).get('eve'))
    night_temp = int(daily_temp_data.get('temp', {}).get('night'))

    weekday1, day1_temp, day1_weather = forecast_data(0)
    weekday2, day2_temp, day2_weather = forecast_data(1)
    weekday3, day3_temp, day3_weather = forecast_data(2)
    weekday4, day4_temp, day4_weather = forecast_data(3)
    weekday5, day5_temp, day5_weather = forecast_data(4)
    weekday6, day6_temp, day6_weather = forecast_data(5)
    weekday7, day7_temp, day7_weather = forecast_data(6)

    context = {
        'day1_weather': day1_weather,
        'day2_weather': day2_weather,
        'day3_weather': day3_weather,
        'day4_weather': day4_weather,
        'day5_weather': day5_weather,
        'day6_weather': day6_weather,
        'day7_weather': day7_weather,
        'day1_temp': day1_temp,
        'day2_temp': day2_temp,
        'day3_temp': day3_temp,
        'day4_temp': day4_temp,
        'day5_temp': day5_temp,
        'day6_temp': day6_temp,
        'day7_temp': day7_temp,
        'weekday1': weekday1,
        'weekday2': weekday2,
        'weekday3': weekday3,
        'weekday4': weekday4,
        'weekday5': weekday5,
        'weekday6': weekday6,
        'weekday7': weekday7,
        'morning_temp': morning_temp,
        'day_temp': day_temp,
        'evening_temp': evening_temp,
        'night_temp': night_temp,
        'location': loc_upper,
        'weather': weather,
        'temp': temp,
        'temp_feel': temp_feel,
        'min_temp': min_temp,
        'max_temp': max_temp,
        'pressure': pressure,
        'humidity': humidity,
        'visibility': visibility,
        'wind_spd': wind_spd,
        'wind_direction': wind_direction,
        'gusts': gusts,
        'clouds': clouds,
        'country_code': country_code,
        'sunrise': sunrise,
        'sunset': sunset,
        'icon_number': icon_number,
        'degree': degree,
    }

    return render(request, 'weatherpy/weather.html', context)


def random_loc(request):

    def forecast_data(json_index):
        epoch = jsonier.get('daily')[json_index].get('dt')
        weekday = time.strftime('%A', time.localtime(epoch))

        day_temp = int(jsonier.get('daily')[
                       json_index].get('temp', {}).get('max'))

        day_weather_lower = jsonier.get('daily')[json_index].get(
            'weather')[0].get('main')
        day_weather = day_weather_lower.title()

        return weekday, day_temp, day_weather

    lat = str(random.randint(-70, 70))
    lon = str(random.randint(-180, 180))

    onecallapi = "https://api.openweathermap.org/data/2.5/onecall?lat=" + \
        lat + "&lon=" + lon + "&exclude=&appid=81c4f61189c578db351b6f68d93ba526&units=metric"

    onecallapi_get = requests.get(onecallapi)
    jsonier = onecallapi_get.json()

    # current weather
    daily_temp_data = jsonier.get("daily")[0]
    morning_temp = int(daily_temp_data.get('temp', {}).get('morn'))
    day_temp = int(daily_temp_data.get('temp', {}).get('day'))
    evening_temp = int(daily_temp_data.get('temp', {}).get('eve'))
    night_temp = int(daily_temp_data.get('temp', {}).get('night'))

    if jsonier.get('cod') == '404' or jsonier.get('cod') == '400':
        return render(request, 'weatherpy/weather_404.html')

    weather_list = jsonier.get("current", {}).get("weather")[0]
    weather_get = weather_list.get('description')
    weather = weather_get.title()

    temp = int(jsonier.get("current", {}).get("temp"))
    temp_feel = int(
        jsonier.get("current", {}).get("feels_like"))

    min_temp = int(jsonier.get("daily")[0].get("temp", {}).get('min'))
    max_temp = int(jsonier.get("daily")[0].get("temp", {}).get('max'))

    pressure = jsonier.get("current", {}).get("pressure")
    humidity = jsonier.get("current", {}).get("humidity")
    visibility = jsonier.get("current", {}).get("visibility")

    wind_spd = jsonier.get("current", {}).get("wind_speed")
    wind_spd_kmh = round((wind_spd * 1.862), 1)
    wind_direction = jsonier.get("current", {}).get("wind_deg")
    gusts = jsonier.get("current", {}).get("gust")
    clouds = jsonier.get("current", {}).get("clouds")
    country_code = jsonier.get("timezone")

    epoch_sunrise = int(jsonier.get("current", {}).get("sunrise"))
    sunrise = datetime.datetime.fromtimestamp(epoch_sunrise)
    epoch_sunset = int(jsonier.get("current", {}).get("sunset"))
    sunset = datetime.datetime.fromtimestamp(epoch_sunset)

    icon_number = weather_list.get("icon")
    degree = '°'

    daily_temp_data = jsonier.get("daily")[0]
    morning_temp = int(daily_temp_data.get('temp', {}).get('morn'))
    day_temp = int(daily_temp_data.get('temp', {}).get('day'))
    evening_temp = int(daily_temp_data.get('temp', {}).get('eve'))
    night_temp = int(daily_temp_data.get('temp', {}).get('night'))

    # forecast

    weekday1, day1_temp, day1_weather = forecast_data(0)
    weekday2, day2_temp, day2_weather = forecast_data(1)
    weekday3, day3_temp, day3_weather = forecast_data(2)
    weekday4, day4_temp, day4_weather = forecast_data(3)
    weekday5, day5_temp, day5_weather = forecast_data(4)
    weekday6, day6_temp, day6_weather = forecast_data(5)
    weekday7, day7_temp, day7_weather = forecast_data(6)

    context = {
        'day1_weather': day1_weather,
        'day2_weather': day2_weather,
        'day3_weather': day3_weather,
        'day4_weather': day4_weather,
        'day5_weather': day5_weather,
        'day6_weather': day6_weather,
        'day7_weather': day7_weather,
        'day1_temp': day1_temp,
        'day2_temp': day2_temp,
        'day3_temp': day3_temp,
        'day4_temp': day4_temp,
        'day5_temp': day5_temp,
        'day6_temp': day6_temp,
        'day7_temp': day7_temp,
        'weekday1': weekday1,
        'weekday2': weekday2,
        'weekday3': weekday3,
        'weekday4': weekday4,
        'weekday5': weekday5,
        'weekday6': weekday6,
        'weekday7': weekday7,
        'morning_temp': morning_temp,
        'day_temp': day_temp,
        'evening_temp': evening_temp,
        'night_temp': night_temp,
        'weather': weather,
        'temp': temp,
        'temp_feel': temp_feel,
        'min_temp': min_temp,
        'max_temp': max_temp,
        'pressure': pressure,
        'humidity': humidity,
        'visibility': visibility,
        'wind_spd': wind_spd,
        'wind_direction': wind_direction,
        'gusts': gusts,
        'clouds': clouds,
        'country_code': country_code,
        'sunrise': sunrise,
        'sunset': sunset,
        'icon_number': icon_number,
        'degree': degree,
        'lat': lat,
        'lon': lon,
    }

    return render(request, 'weatherpy/weatherrandom.html', context)


def about(request):
    return render(request, 'weatherpy/about.html')


def thanks(request):
    return render(request, 'weatherpy/thanks.html')


def contact(request):
    if request.method == 'POST':
        userdata = UserMessage(request.POST)
        if userdata.is_valid():
            post = userdata.save(commit=False)
            post.save()
            return render(request, 'weatherpy/thanks.html')

        else:
            msg = "Algum dos campos contem erros. Verifique se o e-mail está no formato xxxxx@zzzzz.yyy"
            contexto = {
                'contactform': userdata,
                'message': msg
            }

            return render(request, "weatherpy/contactform.html", contexto)

    else:
        contactform = UserMessage()

    return render(request, "weatherpy/contactform.html", {"contactform": contactform})
