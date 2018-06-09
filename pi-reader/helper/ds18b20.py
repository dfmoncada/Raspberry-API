import os, glob, time, sys, datetime


class DS18B20:
    folder = '/sys/bus/w1/devices/'
    file = '/w1_slave'
    add_value = ("INSERT INTO webapp_entry "
                 "(sensor_id, value, created_at) "
                 "VALUES (%s, %s, %s)")

    def __init__(self, options):
        self.name = options['name']
        self.id = options['id']

    def read_temp_raw(self, name):  # A function that grabs the raw temp data from the sensors
        f_1 = open(DS18B20.folder + name + file, 'r')
        lines_1 = f_1.readlines()
        f_1.close()
        return lines_1

    def read(self):  # A function to check the connection was good and strip out the temperature
        lines = DS18B20.read_temp_raw(self.name)
        while lines[0][-4:-1] != 'YES':
            time.sleep(0.2)
            lines = DS18B20.read_temp_raw(self.name)
        equals_pos = lines[1].find('t=') + 2
        temp = float(lines[1][equals_pos:]) / 1000
        return temp

    def save(self, cursor):
        value = self.read()
        now = datetime.now()
        data_value = (self.id, value, now)
        cursor.execute(self.add_value, data_value)
        print("data inserted=> sensor-id:'" + sensor['id_key'] + "', value:" + str(value))
