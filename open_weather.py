#!/usr/bin/env python3

import json
from urllib.request import urlopen
import api_key

# -----------------------------------------------------------------------
#Parameters
#-----------------------------------------------------------------------
num_of_pins=8
lat=53.86
lon=10.68

class weather:
	def __init__(self, lat, lon):
		self.weather_url = self.set_weather_url(api_key.open_weather_api_key, lat, lon)
		self.weather_dict = self.get_weather(self.weather_url)

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
		weather_dict = json.loads(jsonFileContent)
		return weather_dict
	
	def get_condition(self):
		"""weather contains dicts inside a list"""
		return self.weather_dict["weather"][0]["main"]

	def get_temp(self):
		return self.weather_dict["main"]["temp"]

	def get_temp_min(self):
		return self.weather_dict["main"]["temp_min"]

	def get_temp_max(self):
		return self.weather_dict["main"]["temp_max"]

	def get_humidity(self):
		return self.weather_dict["main"]["humidity"]

	def get_pressure(self):
		return self.weather_dict["main"]["pressure"]

	def get_wind_speed(self):
		return self.weather_dict["wind"]["speed"]

	def get_wind_dir(self):
		try:
			return self.weather_dict["wind"]["deg"]
		except:
			return "NaN"

if __name__=="__main__":
	weather = weather(lat, lon)
	#print(weather.weather_dict)
	print(weather.get_condition())
	print(weather.get_temp())
	print(weather.get_temp_min())
	print(weather.get_temp_max())
	print(weather.get_humidity())
	print(weather.get_pressure())
	print(weather.get_wind_speed())
	print(weather.get_wind_dir())

