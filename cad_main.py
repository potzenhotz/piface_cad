#!/usr/bin/env python3
import sys
if sys.version[0] != '3':
	print ('You must run piface-weather with python3')
	sys.exit(0)
import pifacecad
import open_weather as weather_api
import news_api
import time


#if ascii error is raised:
#export PYTHONIOENCODING=utf-8
#-----------------------------------------------------------------------
#Parameters
#-----------------------------------------------------------------------
num_of_pins=8
lat=53.86
lon=10.68

#-----------------------------------------------------------------------
#Class
#-----------------------------------------------------------------------
class cad:
	def __init__(self):
		self.cad = pifacecad.PiFaceCAD()
		self.cad.lcd.backlight_on()
		self.cad.lcd.cursor_off()
		self.cad.lcd.blink_off()
		self.weather = weather_api.weather(lat, lon)
		self.spiegel_headlines = news_api.spiegel_news()
		self.loop_index_weather = 0
		self.loop_index_news = 0

	def create_weather_list(self):
		self.weather_list = []
		deg_symbol = u'\N{DEGREE SIGN}'
		condition = self.weather.get_condition()
		temp = self.weather.get_temp()
		humidity = self.weather.get_humidity()
		pressure = self.weather.get_pressure()
		temp_min = self.weather.get_temp_min()
		temp_max = self.weather.get_temp_max()
		wind_speed = self.weather.get_wind_speed()
		wind_dir = self.weather.get_wind_dir()
		self.weather_list.extend(["\n{0}".format(condition)])
		self.weather_list.extend(["{0}\nTemp: {1} C".format(condition, temp)])
		self.weather_list.extend(["Temp: {0} C\nPress: {1} hPa".format(temp, pressure)])
		self.weather_list.extend(["Press: {0} hPa\nHumidity: {1}%".format(pressure, humidity)])
		self.weather_list.extend(["Humidity: {0}%\nW-Speed: {1} m/s".format(humidity, wind_speed)])
		self.weather_list.extend(["W-Speed: {0} m/s\nW-Dir: {1}".format(wind_speed, wind_dir)])
		self.weather_list.extend(["W-Dir: {0}\nT_Min: {1} C".format(wind_dir, temp_min)])
		self.weather_list.extend(["T_Min: {0} C\nT_Max: {1} C".format(temp_min, temp_max)])
		self.weather_list.extend(["T_Max: {0} C\n{1}".format(temp_max, condition)])

	def press_button_0(self, event):
		if self.loop_index_weather == len(self.weather_list):
			self.loop_index_weather = 0
		if self.loop_index_weather ==0:
			event.chip.lcd.write("Updating Data:")
			self.weather.update_weather()
		return event.chip.lcd.write(self.weather_list[self.loop_index_weather])

	def press_button_2(self, event):
		if self.loop_index_news == len(self.spiegel_headlines):
			self.loop_index_news = 0
		if self.loop_index_news ==0:
			event.chip.lcd.write("Updating Data:")
			self.spiegel_headlines.update_news()
		return event.chip.lcd.write(self.spiegel_headlines[self.loop_index_news])
	
	def handlePin(self, event):
		event.chip.lcd.clear()
		if(event.pin_num == 0):
			self.cad.lcd.backlight_on()
			self.press_button_0(event)
			self.loop_index_weather += 1
		elif(event.pin_num == 2):
			self.cad.lcd.backlight_on()
			self.press_button_2(event)
			self.loop_index_news += 1
		elif(event.pin_num == 4):
			self.turn_off()
		else:
			self.cad.lcd.backlight_on()
			event.chip.lcd.write("Button: \n")
			event.chip.lcd.write(str(event.pin_num))
	
	def start_listener(self):
		listener = pifacecad.SwitchEventListener(chip=self.cad)
		for i in range(num_of_pins):
			listener.register(i, pifacecad.IODIR_FALLING_EDGE, self.handlePin)
		listener.activate()
	
	def turn_off(self):
		self.cad.lcd.backlight_off()

if __name__ == "__main__":
	cad_instance = cad()
	cad_instance.start_listener()
	cad_instance.create_weather_list()
