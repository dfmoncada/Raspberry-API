from datetime import datetime
import MySQLdb.connections
import time
from helper.ds18b20 import DS18B20
from helper.dht11 import DHT11
from config import Config_setup

cnx = MySQLdb.connect(user='django', password='django-user-password', database='pidata', host='127.0.0.1', port=3306)
cursor = cnx.cursor()



add_value = ("INSERT INTO webapp_entry "
             "(sensor_id, value, created_at) "
             "VALUES (%s, %s, %s)")

while True:
    for sensor in Config_setup.sensors:
        eval(sensor['type']).save(sensor['options'])

    # Insert new rows into entries for each sensor
    cnx.commit()
    print("loop commited.")
    time.sleep(600)

cursor.close()
cnx.close()
