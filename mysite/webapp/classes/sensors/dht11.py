import Adafruit_DHT
from datetime import datetime

class DHT11:
    # [options] json with 'pin'= pin_number, type= any of '11','22','2302' ,
    add_value = ("INSERT INTO webapp_entry "
                "(sensor_id, type_id, value, created_at) "
                "VALUES (%s, %s, %s, %s)")
    value_names = ['temp', 'humid']
    def __init__(self, options):
        self.pin = options['pin']
        self.type = options['type']
        self.id = options['id']
        self.m_type = options['m_type']

    def read(self):
        sensor_args = {'11': Adafruit_DHT.DHT11,
                       '22': Adafruit_DHT.DHT22,
                       '2302': Adafruit_DHT.AM2302}
        sensor = sensor_args[self.type]
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
        return [temperature, humidity]

    def save(self, cursor):
        results = self.read()
        now = datetime.now()
        
        for i, result in (enumerate(results,start=0)):
            data_value = (self.id, self.m_type[DHT11.value_names[i]], results[i], now) 
            cursor.execute(self.add_value, data_value)
            print("data inserted=> sensor-id:" + str(self.id) + ', measure_type - ' + DHT11.value_names[i] + ', sensor type:' + self.type + ",  value:" + str(results[i]))
        
