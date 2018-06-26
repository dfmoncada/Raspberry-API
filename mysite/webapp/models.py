from datetime import datetime
from .classes.sensors.ds18b20 import DS18B20
from .classes.sensors.dht11 import DHT11
import pytz, time, json, MySQLdb.connections, threading
from django.db import models
#from .classes.elements_manager import ElementManager

# Create your models here.

class MeasureType(models.Model):
    measurment = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    
    def json_info(self):
        return {"measure":self.measurment, "unit":self.unit}    

    def __str__(self):
        return self.unit
        

class SensorType(models.Model):
    name = models.CharField(max_length=50)
    measurements = models.ManyToManyField(MeasureType)

    def __str__(self):
        return self.name

    def get_json_entries(self, sensor, filter_date):
        types_json = []
        types = self.measurements.all()
        for item in types:
            entries = []
            entries_objects = sensor.entry_set.filter(type__pk = item.id).order_by("-created_at")
            for entry in entries_objects:
                entries.append(entry.get_json())
            type_temp = item.json_info()
            type_temp['entries'] = entries
            types_json.append(type_temp)
        return types_json 
    
    def get_json_live(self, sensor):
        types_json = []
        element_manager = ElementManager('')
        types = self.measurements.all()
        measure_values = element_manager.get_live(sensor) 
        for i, item in enumerate(types, start=0):
            type_temp = item.json_info()
            type_temp['entry'] = measure_values[i]
            types_json.append(type_temp)
        return types_json

class SensorManager(models.Manager):
    def activate_thread(self, sleep):
        if not ElementManager.element_manager:
            ElementManager.element_manager = ElementManager('sensor')
            try:
                sleep = int(sleep)
            except:
                return {'response':'error', 'message':'input a correct integer number'}
            threading.Thread(target=ElementManager.element_manager.start_read_thread, args={sleep}, kwargs={}).start()
            return {'response':'change', 'new_status': 'activated'}
        return {'response':'unchanged', 'status': 'activated'}

    def deactivate_thread(self):
        changed = 'unchanged'
        if ElementManager.element_manager:
            changed = 'changed'
            ElementManager.element_manager.deactivate_thread()
        return {'response':changed, 'status':'deactivated'}

    def activate_rule(rule):
        if not ElementManager.element_manager2:
            ElementManager.element_manager2 = ElementManager('rule')
            threading.Thread(target=ElementManager.element_manager2.start_rule, args={5}, kwargs={}).start()
            return {'response':'change', 'new_status': 'activated'}
        return {'response':'unchanged', 'status': 'activated'}
    
    def deactivate_rule(self):
        changed = 'unchanged'
        if ElementManager.element_manager2:
            changed = 'changed'
            ElementManager.element_manager2.deactivate_rule()
        return {'response':changed, 'status':'deactivated'}

    def get_all_json(self, filter_date):
        sensors_all = self.all()
        return SensorManager.list_to_json(sensors_all, filter_date)
 
    def get_all_live_json(self):
        sensors_all = self.all()
        return SensorManager.list_to_live_json(sensors_all)

    @staticmethod
    def list_to_json(sensors_all, filter_date):
        json_all = []
        for item in sensors_all:
            json_all.append(item.get_json_with_relations(filter_date))
        return json_all
    
    @staticmethod
    def list_to_live_json(sensors_all):
        json_all = []
        for item in sensors_all:
            json_all.append(item.get_live_json())
        return json_all

class Sensor(models.Model):
    objects = SensorManager()
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    given_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    activated = models.BooleanField(default=False)
    options = models.CharField(max_length=150)

    def get_json_with_relations(self, filter_date):
        json_object = self.json_info()
        json_object['types'] = self.sensor_type.get_json_entries(self, filter_date)
        return json_object

    def json_info(self):
        return {
            "sensor_id": self.id,
            "sensor_type_name": self.sensor_type.name,
            "given_name": self.given_name,
            "location": self.location,
        }

    def get_live_json(self):
        json_object = self.json_info()
        json_object['types'] = self.sensor_type.get_json_live(self)
        return json_object
         

    def get_entries_from_sensor_json(self, filter_date):
        entries_objects = Entry.objects.filter(sensor=self.id)
        today_date = datetime.now()
        if filter_date is not None and filter_date < today_date:
            entries_objects = entries_objects.filter(created_at__range=(filter_date, today_date))

        entries_json = []
        for i in entries_objects:
            entries_json.append(i.get_json())
        return entries_json

    def __str__(self):
        return self.given_name


class Entry(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    type = models.ForeignKey(MeasureType, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    def get_json(self):
        return {
            'created_at': self.created_at.strftime("%Y-%m-%d_%H:%M:%S"),
            'value': self.value
        }
    def __str__(self):
        return self.sensor.given_name + ':'+str(self.value)+'('+self.created_at.strftime("%Y-%m-%d_%H:%M:%S")+")"

class ElementManager:
    element_manager = None
    element_manager2 = None
    def __init__(self, type_n):
        if type_n == 'sensor':
            ElementManager.element_manager = self
        elif type_n == 'rule':
            ElementManager.element_manager2 = self
        self.active = True

    def start_rule(self, sleep):
        if self.active:
            try:
                read = Sensor.objects.get_all_live_json()
                result = 0
                if read[0]['types'][0]['entry'] > 26:
                    result = 1
                f=open("/sys/class/gpio/gpio18/value", "w+")
                f.write(str(result))
                f.close()
            except Exception as e:
                print(e)
            time.sleep(sleep)
            self.start_rule(sleep)
    
    def deactivate_rule(self):
        ElementManager.element_manager2 = None
        self.active = False

    def start_read_thread(self, sleep):
        if self.active:
            self.handle_connection()
            time.sleep(sleep)
            self.start_read_thread(sleep)

    def handle_connection(self):
        cnx = MySQLdb.connect(user='django', password='django-user-password', database='pidata', host='127.0.0.1', port=3306)
        cursor = cnx.cursor()
        sensors = Sensor.objects.all();
        for sensor in sensors:
            try:
                sensor_object = ElementManager.get_class_object(sensor)
                sensor_object.save(cursor)
                cnx.commit()
            except Exception as e:
                print("error(sensor_id:" + str(sensor.id)+ "):", e)
        print("loop commited.")
        cursor.close()
        cnx.close()

    def deactivate_thread(self):
        ElementManager.element_manager = None
        self.active = False

    def get_live(self, sensor):
        sensor_class = ElementManager.get_class_object(sensor)
        return sensor_class.read() 

    @staticmethod
    def get_class_object(sensor):
        sensor_class = globals()[sensor.sensor_type.name]
        print('sensor:' + sensor.given_name, 'options:', json.loads(sensor.options))
        return sensor_class(json.loads(sensor.options))
