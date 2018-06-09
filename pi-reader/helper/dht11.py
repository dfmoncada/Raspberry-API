import Adafruit_DHT
from datetime import datetime

class DHT11:
    # [options] json with 'pin'= pin_number, type= any of '11','22','2302' ,
    add_value = ("INSERT INTO webapp_entry "
                "(sensor_id, value, created_at) "
                "VALUES (%s, %s, %s)")

    def __init__(self, options):
        self.pin = options['pin']
        self.type = options['type']
        self.temp_id = options['id']['temp']
        self.humid_id = options['id']['humid']

    def read(self):
        sensor_args = {'11': Adafruit_DHT.DHT11,
                       '22': Adafruit_DHT.DHT22,
                       '2302': Adafruit_DHT.AM2302}
        sensor = sensor_args[self.type]
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
        return {'temp':temperature, 'humid':humidity}

    def save(self, cursor):
        results = self.read()
        now = datetime.now()
        data_value_temp = (self.temp_id, results['temp'], now) 
        data_value_humid = (self.humid_id, results['humid'], now)
        cursor.execute(self.add_value, data_value_temp)
        cursor.execute(self.add_value, data_value_humid)
        print("data inserted=> sensor-id:'" + str(self.temp_id) + '-' + self.type + "', value:" + str(results['temp']))
        print("data inserted=> sensor-id:'" + str(self.humid_id) + '-' + self.type + "', value:" + str(results['humid']))
