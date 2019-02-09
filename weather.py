#!/usr/bin/python
import feedparser


#Set Variables to ensure we start fresh
min_temp = ''
max_temp = ''

#OpenweatherMap Settings
owm_api = 'e20a5ac3dc0f2a1c6f00a83ff9ce64e9' #http://openweathermap.org/appid#get
owm_cityid = '2172880' #Search for city and use number in result URL
owm_unit = 'metric' #metric or imperial

#Open Weather Map API URL
weatherURL = feedparser.parse ('http://api.openweathermap.org/data/2.5/weather?id=%s&appid=%s&mode=xml&units=%s' % (owm_cityid, owm_api, owm_unit))

#Get Yahoo Weather Code, min temp, max temp and weather text summary
min_temp = weatherURL.feed.temperature.get('min')
max_temp = weatherURL.feed.temperature.get('max')
print("get weather forecast ...")
forecast_text = weatherURL.feed.weather.get('value')
print(forecast_text)