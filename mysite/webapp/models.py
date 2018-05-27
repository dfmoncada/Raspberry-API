from django.db import models
import json

# Create your models here.


class SensorType(models.Model):
	name = models.CharField(max_length=50)
	unit = models.CharField(max_length=50)
	measure = models.CharField(max_length=50)

class Sensor(models.Model):
	sensorType = models.ForeignKey(SensorType, on_delete=models.CASCADE)
	given_name = models.CharField(max_length=50)
	id_number = models.CharField(max_length=50)

	def get_json_with_relations(self):
		return json.dumps({
			"sensor_type_name":self.sensorType.name,
			"sensor_type_unit":self.sensorType.unit,
			"sensor_type_measure":self.sensorType.measure,
			"given_name":self.given_name,
			"id_number":self.id_number,
			'entries':self.get_entries_from_sensor_json()
		})

	def get_entries_from_sensor_json(self):
		entries_objects = Entry.objects.filter(sensor=self.id)
		entries_json = []
		for i in entries_objects:
			entries_json.append(i.get_json())
		return entries_json

class Entry(models.Model):
	sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
	value = models.FloatField()
	created_at = models.DateTimeField()

	def get_json(self):
		return {
			'created_at':self.created_at.__str__(),
			'value':self.value
		}