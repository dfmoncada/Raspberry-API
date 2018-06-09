from datetime import datetime
import MySQLdb.connections
import time
from helper.ds18b20 import DS18B20
from helper.dht11 import DHT11
from config import ConfigSetup

cnx = MySQLdb.connect(user='django', password='django-user-password', database='pidata', host='127.0.0.1', port=3306)
cursor = cnx.cursor()



add_value = ("INSERT INTO webapp_entry "
             "(sensor_id, value, created_at) "
             "VALUES (%s, %s, %s)")

sensors = ConfigSetup.get_sensors()

while True:
    for sensor in sensors:
       sensor_class = globals()[sensor['type']]
       sensor_object = sensor_class(sensor['options'])
       sensor_object.save(cursor)

    # Insert new rows into entries for each sensor
    cnx.commit()
    print("loop commited.")
    time.sleep(600)

cursor.close()
cnx.close()
