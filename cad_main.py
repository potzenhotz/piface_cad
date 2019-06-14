#!/usr/bin/env python3
import sys
if sys.version[0] != '3':
	print ('You must run piface-weather with python3')
	sys.exit(0)
import pifacecad
import open_weather as weather

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
	start_listener()
