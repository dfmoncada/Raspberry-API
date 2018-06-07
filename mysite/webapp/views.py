from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core import serializers
from datetime import datetime
from django.utils.dateparse import parse_datetime
from .models import Entry, SensorType, Sensor, SensorManager

# Create your views here.
def index(request):
	# data = [
	# 	{'id':1,'type_name':'ds18b20','unit':'degrees','measure':'temperature','given_name':'ferm temp 1', 'id_number':'28-123123',
	# 	'entries':[{'value':20,'created_at':'test date'},{'value':21,'created_at':'test date'},{'value':22,'created_at':'test date'}]}
	# ]
	# sensors = Sensor.objects.all()
	# data = serializers.serialize('json', entry_list)
	
	# data = []
	# for i in sensors:
		# data.append(i.get_json_with_relations())
	filter_date = str_to_datetime_default(request.GET.get('date'))

	sensors_json = Sensor.objects.get_all_json(filter_date)
	return HttpResponse(json.dumps(sensors_json),content_type='application/json')
	
def filter(request):
	date_query = request.GET.get('date')
	from_datetime = str_to_datetime_default(date_query);

	return HttpResponse('<p>'+date.__str__()+'</p>')

# PRIVATE FUNCTIONS

def str_to_datetime_default(query):
	if not query:
		return query
	query = list(query)
	query[-6] = '+'
	query = "".join(query);
	return parse_datetime(query)