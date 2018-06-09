import Adafruit_DHT


class DHT11:
    # [options] json with 'pin'= pin_number, type= any of '11','22','2302' ,
    def __init__(self, options):
        self.pin = options['pin']
        self.type = options['type']

    def read(self):
        sensor_args = {'11': Adafruit_DHT.DHT11,
                       '22': Adafruit_DHT.DHT22,
                       '2302': Adafruit_DHT.AM2302}
        sensor = sensor_args[self.type]
        humidity, temperature = Adafruit_DHT.read_retry(sensor, self.pin)
        return temperature

    def save(self, ):
        results = self.read()
        self.results = results



