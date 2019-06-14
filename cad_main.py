#!/usr/bin/env python3
import sys
if sys.version[0] != '3':
	print ('You must run piface-weather with python3')
	sys.exit(0)
import pifacecad
import open_weather as weather_api

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
		self.loop_index = 0

	def create_weather_list(self):
		self.weather_list = []
		self.weather_list.extend(["Temp: {}".format(self.weather.get_temp())])
		self.weather_list.extend(["Humidity: {}".format(self.weather.get_humidity())])

	
	def press_button_0(self, event):
		if self.loop_index == len(self.weather_list):
			self.loop_index = 0
		return event.chip.lcd.write(self.weather_list[self.loop_index])
	
	def handlePin(self, event):
		event.chip.lcd.clear()
		if(event.pin_num == 0):
			self.press_button_0(event)
			self.loop_index += 1
		else:
			event.chip.lcd.write("Button:")
			event.chip.lcd.write(str(event.pin_num))
	
	def start_listener(self):
		listener = pifacecad.SwitchEventListener(chip=self.cad)
		for i in range(num_of_pins):
			listener.register(i, pifacecad.IODIR_FALLING_EDGE, self.handlePin)
		listener.activate()


if __name__ == "__main__":
	#cad = init_cat()
	#start_listener()
	cad_instance = cad()
	cad_instance.start_listener()
	cad_instance.create_weather_list()
