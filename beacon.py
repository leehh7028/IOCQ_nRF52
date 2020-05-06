import sys
import pymysql
import serial

ser = serial.Serial(
	port='/dev/ttymxc1',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
	)

while True:

	word = ser.readline()	
	length =  len(word)
	if length == 81:
		print(word)
		split = word.split(":")
		MAC = split[0]
		MAJORMINOR = split[2]
		MAJORMINOR = MAJORMINOR[10:18]
		MAJOR = MAJORMINOR[0:4]
		MINOR = MAJORMINOR[4:8]
		RSSI = split[4]
		print("MAC : " + MAC)
		print("MAJOR MINOR : " + MAJORMINOR)
		print("MAJOR : " + MAJOR + "/ " + str(MAJOR)) )
		print("MINOR : " + MINOR)
		print("RSSI : " + RSSI)



