#!/usr/bin/env python3
import sys
if sys.version[0] != '3':
	print ('You must run piface-weather with python3')
	sys.exit(0)
import pifacecad
import open_weather as weather_api
import news_api
import time
import subprocess

#-----------------------------------------------------------------------
#Class
#-----------------------------------------------------------------------
class cad:
	def __init__(self):
		self.len_of_screen = 16
		self.txt_speed = 0.05
		self.txt_speed_start = 0.8
		self.num_of_pins=8
		self.set_cities()
		self.cad = pifacecad.PiFaceCAD()
		self.cad.lcd.backlight_on()
		self.cad.lcd.cursor_off()
		self.cad.lcd.blink_off()
		self.city = "Luebeck"
		self.weather = weather_api.weather(self.cities[self.city][0], self.cities[self.city][1])
		self.spiegel = news_api.spiegel_news()
		self.spiegel_headlines = self.spiegel.get_headlines()
		self.loop_index_weather = 0
		self.loop_index_news = 0
		self.loop_index_cities = 0
		self.turn_off_counter = 0
		self.cad.lcd.write("CAD Ready") 
	
	def set_cities(self):
		self.cities = {}
		self.cities["Luebeck"] = [53.86, 10,68]
		self.cities["Dortmund"] = [51.51, 7.46]
		self.cities["Essen"] = [51.45, 7.01]

	def initialize_weather(self):
		self.weather_list = self.weather.create_weather_list()

	def press_button_0(self, event):
		if self.loop_index_weather == len(self.weather_list):
			self.loop_index_weather = 0
		if self.loop_index_weather ==0:
			event.chip.lcd.write("Updating Data:\n{0}".format(self.city))
			self.weather_list = self.weather.update_weather()
			time.sleep(0.3)
			event.chip.lcd.clear()
		return event.chip.lcd.write(self.weather_list[self.loop_index_weather])

	def press_button_2(self, event):
		if self.loop_index_news == len(self.spiegel_headlines):
			self.loop_index_news = 0
		if self.loop_index_news ==0:
			event.chip.lcd.write("Updating Data:")
			time.sleep(0.5)
			event.chip.lcd.clear()
			self.spiegel.update_news()
		self.move_txt_on_screen(event, self.spiegel_headlines[self.loop_index_news])
	
	def press_button_4(self, event):
		event.chip.lcd.clear()
		if self.turn_off_counter == 0:
			event.chip.lcd.write("Turn off?\nPress again!")
			self.turn_off_counter += 1
		else:
			for i in range(3,0,-1):
				event.chip.lcd.write("Turning off in {}".format(i))
				time.sleep(1)
				event.chip.lcd.set_cursor(0,0)
			event.chip.lcd.clear()
			event.chip.lcd.write("Turning off...")
			time.sleep(1)
			event.chip.lcd.clear()
			self.turn_screen_off()
			self.turn_off_pi()

	def press_button_5(self, event):
		self.city = list(self.cities)[self.loop_index_cities]
		self.weather = weather_api.weather(self.cities[self.city][0], self.cities[self.city][1])
		self.loop_index_weather = 0
		return event.chip.lcd.write("City is set to:\n{}".format(self.city))

	def press_button_6(self, event):
		self.loop_index_cities = self.sub_one_of__counter(self.loop_index_cities, len(self.cities)-1)
		return event.chip.lcd.write(list(self.cities)[self.loop_index_cities])

	def press_button_7(self, event):
		self.loop_index_cities = self.add_one_to_counter(self.loop_index_cities, len(self.cities)-1)
		return event.chip.lcd.write(list(self.cities)[self.loop_index_cities])
	
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
			self.press_button_4(event)
		elif(event.pin_num == 5):
			self.press_button_5(event)
		elif(event.pin_num == 6):
			self.press_button_6(event)
		elif(event.pin_num == 7):
			self.press_button_7(event)
		else:
			self.cad.lcd.backlight_on()
			event.chip.lcd.write("Button: \n")
			event.chip.lcd.write(str(event.pin_num))
	
	def start_listener(self):
		listener = pifacecad.SwitchEventListener(chip=self.cad)
		for i in range(self.num_of_pins):
			listener.register(i, pifacecad.IODIR_FALLING_EDGE, self.handlePin)
		listener.activate()
	
	def turn_screen_off(self):
		self.cad.lcd.backlight_off()

	def move_txt_on_screen(self, event, text):
		loop_count = len(text) - self.len_of_screen + 1
		if loop_count <= 0:
			event.chip.lcd.write(text)
		else:
			for i in range(loop_count):
				event.chip.lcd.set_cursor(0,0)
				event.chip.lcd.write(text[i:self.len_of_screen+i])
				if i == 0:
					time.sleep(self.txt_speed+self.txt_speed_start)
				else:
					time.sleep(self.txt_speed)
	
	def add_one_to_counter(self, counter, max_counter):
		if counter == max_counter:
			return 0
		else:
			return counter + 1

	def sub_one_of__counter(self, counter, max_counter):
		if counter == 0:
			return max_counter
		else:
			return counter - 1

	def turn_off_pi(self):
		subprocess.call(["sudo", "shutdown", "-h", "0"])

if __name__ == "__main__":
	cad_instance = cad()
	cad_instance.start_listener()
	cad_instance.initialize_weather()
