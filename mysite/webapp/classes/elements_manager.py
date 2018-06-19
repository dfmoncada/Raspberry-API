import time
import json
from .sensors.ds18b20 import DS18B20
from .sensors.dht11 import DHT11
import MySQLdb.connections
#from ..models import Sensor
from .config import ConfigSetup

class ElementManager:
    element_manager = None
    def __init__(self):
        ElementManager.element_manager = self
        self.active = True 

    def start_read_thread(self, sleep=600):
        if self.active:
            self.handle_connection()
            time.sleep(sleep)
            self.start_read_thread(sleep)

    def handle_connection(self):
        cnx = MySQLdb.connect(user='django', password='django-user-password', database='pidata', host='127.0.0.1',
                              port=3306)
        cursor = cnx.cursor()
        #sensors1 = ConfigSetup.get_sensors() # to be changed for DB
        sensors = Sensor.objects.all();
        for sensor in sensors:
            try:
                sensor_class = ElementManager.get_class_object(sensor)
                sensor_object.save(cursor)
            except Exception as e:
                print("error(sensor_id:"+str(sensor.id)+"):", e)
        # Insert new rows into entries for each sensor
        cnx.commit()
        print("loop commited.")

        cursor.close()
        cnx.close()

    def deactivate_thread(self):
        ElementManager.element_manager = None
        self.active = False

    @staticmethod
    def get_class_object(sensor):
        sensor_class = gloabls()[sensor.sensor_type.name]
        print('sensor:' + sensor.given_name, 'options:', json.loads(sensor.options))
        return sensor_class(json.loads(sensor.options))
