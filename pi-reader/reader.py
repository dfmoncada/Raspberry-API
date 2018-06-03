from datetime import datetime
import MySQLdb.connections
import time
from helper.ds18b20 import read_temp_raw, read_temp

cnx = MySQLdb.connect(user='django', password='django-user-password', database='pidata', host='127.0.0.1', port=3306)
cursor = cnx.cursor()

sensors = [
	{'id':1,'id_key':'28-051693633fff'},
]



add_value = ("INSERT INTO webapp_entry "
               "(sensor_id, value, created_at) "
               "VALUES (%s, %s, %s)")

while True:
	for i in sensors:
		now = datetime.now()
		value = read_temp(i['id_key'])
		data_value = (i['id'], value, now)
		cursor.execute(add_value, data_value)
		print("data inserted=> sensor-id:'" + i['id_key'] + "', value:" + str(value))

	# Insert new rows into entries for each sensor
	cnx.commit()
	print("loop commited.")
	time.sleep(60)




cursor.close()
cnx.close()
