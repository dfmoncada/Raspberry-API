from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core import serializers

from .models import Entry, SensorType, Sensor


# Create your views here.
def index(request):
	# data = [
	# 	{'id':1,'type_name':'ds18b20','unit':'degrees','measure':'temperature','given_name':'ferm temp 1', 'id_number':'28-123123',
	# 	'entries':[{'value':20,'created_at':'test date'},{'value':21,'created_at':'test date'},{'value':22,'created_at':'test date'}]}
	# ]
	sensors = Sensor.objects.all()
	# data = serializers.serialize('json', entry_list)
	data = []
	for i in sensors:
		data.append(i.get_json_with_relations())
	return HttpResponse(json.dumps(data),content_type='application/json')
	
