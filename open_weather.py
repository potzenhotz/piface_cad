#!/usr/bin/env python3

import json
from urllib.request import urlopen
import api_key

#-----------------------------------------------------------------------
#Parameters
#-----------------------------------------------------------------------
num_of_pins=8
lat=53.86
lon=10.68

class weather:

	def __init__(self, lat, lon):
		self.weather_url = self.set_weather_url(api_key.open_weather_app_key, lat, lon)
		self.weather_obj = self.get_weather(self.weather_url)

	def set_weather_url(self, open_weater_app_key, lat, lon):
		raw_url = "https://api.openweathermap.org/data/2.5/weather?"
		and_url = "&"
		lat_url = "lat={0}".format(lat)
		lon_url = "lon={0}".format(lon)
		lang_url = "lang=de"
		units_url = "units=metric"
		id_url = "appid={0}".format(open_weater_app_key)
		weather_url = raw_url + lat_url + and_url + lon_url + and_url + lang_url + and_url + units_url + and_url + id_url
		return weather_url
	
	def get_weather(self, weather_url):
		jsonFile = urlopen(weather_url)
		jsonFileContent = jsonFile.read().decode('utf-8')
		weather_obj = json.loads(jsonFileContent)
		return weather_obj


if __name__=="__main__":
	weather = weather(lat, lon)
