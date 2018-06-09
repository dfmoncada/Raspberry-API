import time
from .sensors.ds18b20 import DS18B20
# from .sensors.dht11 import DHT11
import MySQLdb.connections
from webapp.models import Sensor
from .config import ConfigSetup

class ElementManager:


    def __init__(self):
        pass

    @staticmethod
    def start_read_thread(sleep=600):
        ElementManager.handle_connection()
        time.sleep(sleep)
        ElementManager.start_read_thread(sleep)

    @staticmethod
    def handle_connection():
        cnx = MySQLdb.connect(user='django', password='django-user-password', database='pidata', host='127.0.0.1',
                              port=3306)
        cursor = cnx.cursor()
        sensors = ConfigSetup.get_sensors() # to be changed for DB
        for sensor in sensors:
            sensor_class = globals()[sensor['type']]
            sensor_object = sensor_class(sensor['options'])
            sensor_object.save(cursor)

        # Insert new rows into entries for each sensor
        cnx.commit()
        print("loop commited.")

        cursor.close()
        cnx.close()

