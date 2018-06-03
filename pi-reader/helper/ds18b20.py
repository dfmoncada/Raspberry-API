import os, glob, time, sys, datetime

folder = '/sys/bus/w1/devices/'
file = '/w1_slave'
def read_temp_raw(name): #A function that grabs the raw temp data from the sensors
	f_1 = open(folder + name + file , 'r')
	lines_1 = f_1.readlines()
	f_1.close()
	return lines_1

def read_temp(name): #A function to check the connection was good and strip out the temperature
	lines = read_temp_raw(name)
	while lines[0][-4:-1] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw(name)
	equals_pos = lines[1].find('t=')+2
	temp = float(lines[1][equals_pos:])/1000
	return temp

