#!/usr/bin/env python3

import json
import api_key
import requests

# -----------------------------------------------------------------------
#Parameters
#-----------------------------------------------------------------------
num_of_pins=8
lat=53.86
lon=10.68

class weather:
	def __init__(self, lat, lon):
		self.__weather_url = self.set_weather_url(api_key.open_weather_api_key, lat, lon)
		self.__weather_dict = self.get_weather()

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
	
	def get_weather(self):
		#resp = requests.get(self.__weather_url, headers={'Cache-Control': 'no-cache'})
		resp = requests.get(self.__weather_url)
		weather_dict = resp.json()
		return weather_dict
	
	def update_weather(self):
		self.__weather_dict = self.get_weather()
	
	def get_condition(self):
		"""weather contains dicts inside a list"""
		return self.__weather_dict["weather"][0]["main"]

	def get_temp(self):
		return self.__weather_dict["main"]["temp"]

	def get_temp_min(self):
		return self.__weather_dict["main"]["temp_min"]

	def get_temp_max(self):
		return self.__weather_dict["main"]["temp_max"]

	def get_humidity(self):
		return self.__weather_dict["main"]["humidity"]

	def get_pressure(self):
		return self.__weather_dict["main"]["pressure"]

	def get_wind_speed(self):
		return self.__weather_dict["wind"]["speed"]

	def get_wind_dir(self):
		try:
			return self.__weather_dict["wind"]["deg"]
		except:
			return "NaN"

if __name__=="__main__":
	weather = weather(lat, lon)
	print(weather.get_condition())
	print(weather.get_temp())
	print(weather.get_temp_min())
	print(weather.get_temp_max())
	print(weather.get_humidity())
	print(weather.get_pressure())
	print(weather.get_wind_speed())
	print(weather.get_wind_dir())

