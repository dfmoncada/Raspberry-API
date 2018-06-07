from django.db import models
from datetime import datetime, date
import json
import pytz

# Create your models here.


class SensorType(models.Model):
	name = models.CharField(max_length=50)
	unit = models.CharField(max_length=50)
	measure = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class SensorManager(models.Manager):
	def get_all_json(self, filter_date):
		sensors_all = self.all()
		

		json_all = []
		for item in sensors_all:
			json_all.append(item.get_json_with_relations(filter_date))
		return json_all

class Sensor(models.Model):
	objects = SensorManager()
	sensorType = models.ForeignKey(SensorType, on_delete=models.CASCADE)
	given_name = models.CharField(max_length=50)
	id_number = models.CharField(max_length=50)

	def get_json_with_relations(self, filter_date):

		return {
			"sensor_type_name":self.sensorType.name,
			"sensor_type_unit":self.sensorType.unit,
			"sensor_type_measure":self.sensorType.measure,
			"given_name":self.given_name,
			"id_number":self.id_number,
			'entries':self.get_entries_from_sensor_json(filter_date)
		}

	def get_entries_from_sensor_json(self,filter_date):
		entries_objects = Entry.objects.filter(sensor=self.id)

		today_date = datetime.now()
		timezone = pytz.timezone("GMT")
		today_date = timezone.localize(today_date)
		
		if (not filter_date==None and filter_date < today_date):
			entries_objects = entries_objects.filter(created_at__range=(filter_date,today_date))

		entries_json = []
		for i in entries_objects:
			entries_json.append(i.get_json())
		return entries_json

	def __str__(self):
		return self.given_name

class Entry(models.Model):
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
	value = models.FloatField()
	created_at = models.DateTimeField()

	def get_json(self):
		return {
			'created_at':self.created_at.__str__(),
			'value':self.value
		}
