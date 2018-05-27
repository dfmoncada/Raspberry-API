from datetime import datetime
import MySQLdb.connections
import time

cnx = MySQLdb.connect(user='root', password='root', database='pi_db', host='127.0.0.1', port=8889)
cursor = cnx.cursor()

sensors = [
	{'id':1,'id_key':'28-blablabla'},
	{'id':2,'id_key':'28-bla2bla2b'}
]



add_value = ("INSERT INTO webapp_entry "
               "(sensor_id, value, created_at) "
               "VALUES (%s, %s, %s)")

while True:
	for i in sensors:
		now = datetime.now()
		value = 24
		data_value = (i['id'], value, now)
		cursor.execute(add_value, data_value)

	# Insert new rows into entries for each sensor
	cnx.commit()
	time.sleep(5)



cursor.close()
cnx.close()