from datetime import datetime

import pytz
from django.db import models


# Create your models here.

class MeasureType(models.Model):
    measurment = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    
    def __str__(self):
        return self.measurement
        

class SensorType(models.Model):
    name = models.CharField(max_length=50)
    measurements = models.ManyToManyField(MeasureType)

    def __str__(self):
        return self.name

    def get_json_entries(self, sensor):
        types_json = []
        types = self.measurements.all()
        for item in types:
            entries = []
            entries_objects = sensor.entry_set.filter(type__pk = item.id)
            for entry in entries_objects:
                entries.append(entry.get_json())
            types_json.append({"measure": item.measurment,
                            "unit": item.unit,
                            "entries": entries})
        return types_json 


class SensorManager(models.Manager):
    def get_all_json(self, filter_date):
        sensors_all = self.all()

        json_all = []
        for item in sensors_all:
            json_all.append(item.get_json_with_relations(filter_date))
        return json_all


class Sensor(models.Model):
    objects = SensorManager()
    sensor_type = models.ForeignKey(SensorType, on_delete=models.CASCADE)
    given_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    activated = models.BooleanField(default=False)

    def get_json_with_relations(self, filter_date):
        return {
            "sensor_type_name": self.sensor_type.name,
            "given_name": self.given_name,
            "location": self.location,
            "types": self.sensor_type.get_json_entries(self)
        }

    def get_entries_from_sensor_json(self, filter_date):
        entries_objects = Entry.objects.filter(sensor=self.id)

        today_date = datetime.now()
        # timezone = pytz.timezone("GMT")
        # today_date = timezone.localize(today_date)

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
