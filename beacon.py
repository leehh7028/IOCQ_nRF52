import sys
import pymysql
import serial
import pymysql
from time import sleep
import os
import openpyxl



ser = serial.Serial(
	port='/dev/ttymxc1',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
	)

class DB_sending:
    def __init__(self):
        self.url = "210.115.227.108"
        self.id = 'cic'
        self.password = '20180903in'
        self.dbName = 'kindergartenbus'

    def creat_connet(self):
        self.db = pymysql.connect(host=self.url, port=3306, user=self.id, passwd=self.password, db=self.dbName, charset='utf8')
        self.cursor = self.db.cursor()

    def calcualte_distance_rssi(self, txPower, rssi):
        txPower_num =  int(txPower)
        rssi_num = int(rssi)
        if rssi_num is 0 :
            return -1
        if txPower_num == 0:
            return -1
        ratio = rssi_num * 1.0 / txPower_num
        if ratio < 1.0 :
            return str(ratio**10)
        else:
            distance = (0.89976) * (ratio**7.7095) + 0.111
            return str(distance)

    def insert_unique_data(self, mac, uuid, major, minor):
        sql = "insert into device_unique_info_tb (macAddress, UUID, major, minor) " \
                "select '"+ mac+"' ,'"+uuid+"' ,'"+major+"' ,'"+minor+"' from dual where not exists" \
                "( select * from device_unique_info_tb where macAddress = '"+mac+"' and UUID = '"+uuid+"')"
#       print(sql)
        self.cursor.execute(sql)
        self.db.commit()
#print(self.cursor.lastrowid)

    def insert_valiable_data(self, mac, rssi, txpower, accuracy):
        sql = "INSERT IGNORE INTO device_variable_info_tb (macAddress, rssi, txpower, accuracy, time) VALUES ('"+ mac +"', '"+ rssi +"', '"+ txpower +"', '"+ accuracy +"', CURRENT_TIMESTAMP);"
#       print(sql)
        self.cursor.execute(sql)
        self.db.commit()
#       print(self.cursor.lastrowid)

    def run_sensor_thread(self):
        os.system("sudo python3 /home/pi/sensorDataToDB.py")


dev_id = 0
conn = DB_sending()



while True:

	word = ser.readline()	
	length =  len(word)

	if length == 81:
		
		print(word)
		split = word.split(":")

		MAC = split[0]
		POWER = split[1]
		MAJORMINOR = split[2]
		RSSI = split[4]

		TX_POWER = POWER[4:5]
		MAJORMINOR = MAJORMINOR[10:18]
		MAJOR = MAJORMINOR[0:4]
		MINOR = MAJORMINOR[4:8]

		MAJOR_INT = int(MAJOR, 16)
		MINOR_INT = int(MINOR, 16)

		if MINOR_INT != 30530:
			continue

		conn.creat_connet()		
		conn.insert_unique_data(str(MAC), 'null', str(MAJOR_INT), str(MINOR_INT))
#		conn.insert_unique_data(str(MAC), i'null', str(MAJOR), str(MINOR))
#		conn.insert_valiable_data("MAC", str(RSSI), str(TX_POWER), str(conn.calcualte_distance_rssi(TX_POWER, RSSI)))
		conn.insert_valiable_data(MAC, RSSI, "-59", conn.calcualte_distance_rssi("-59", RSSI))

		
#		print("test : ",  MAJOR_INT)
#		print("MAC : " + MAC)
#		print("Tx Power : " + TX_POWER)
#		print("MAJOR : " + MAJOR)
#		print("MINOR : " + MINOR)
#		print("MAJOR_INT : %d ", MAJOR_INT)
#		print("MAJOR_INT : " + str(MAJOR_INT))
		print("MINOR_INT : " + str(MINOR_INT))
#		print("RSSI : " + RSSI)

























