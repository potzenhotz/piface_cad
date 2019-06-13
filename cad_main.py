#!/usr/bin/env python3
import sys
if sys.version[0] != '3':
	print ('You must run piface-weather with python3')
	sys.exit(0)
import pifacecad
import api_key
import json
from urllib.request import urlopen

#-----------------------------------------------------------------------
#Parameters
#-----------------------------------------------------------------------
num_of_pins=8
lat=53.86
lon=10.68

#-----------------------------------------------------------------------
#Functions
#-----------------------------------------------------------------------
def init_cat():
	cad = pifacecad.PiFaceCAD()
	cad.lcd.backlight_on()
	cad.lcd.cursor_off()
	cad.lcd.blink_off()
	return cad

def get_weather_url(open_weater_app_key, lat, lon):
	raw_url = "https://api.openweathermap.org/data/2.5/weather?"
	and_url = "&"
	lat_url = "lat={0}".format(lat)
	lon_url = "lon={0}".format(lon)
	lang_url = "lang=de"
	units_url = "units=metric"
	id_url = "appid={0}".format(open_weater_app_key)
	weather_url = raw_url + lat_url + and_url + lon_url + and_url + lang_url + and_url + units_url + and_url + id_url
	return weather_url

def get_weather(weather_url):
	jsonFile = urlopen(weather_url)
	jsonFileContent = jsonFile.read().decode('utf-8')
	weather_obj = json.loads(jsonFileContent)
	return weather_obj

def press_button_0(event):
	temp = weather_obj['main']['temp']
	return event.chip.lcd.write("Temp: {0}".format(temp))


def handlePin(event):
	event.chip.lcd.clear()
	if(event.pin_num == 0):
		press_button_0(event)
	else:
		event.chip.lcd.write("Button:")
		event.chip.lcd.write(str(event.pin_num))

def start_listener():
	listener = pifacecad.SwitchEventListener(chip=cad)
	for i in range(num_of_pins):
		listener.register(i, pifacecad.IODIR_FALLING_EDGE, handlePin)
	listener.activate()


if __name__ == "__main__":
	cad = init_cat()
	weather_url = get_weather_url(api_key.open_weater_app_key, lat, lon)
	weather_obj = get_weather(weather_url)
	start_listener()
