import json

from django.http import HttpResponse
from datetime import datetime
from django.utils.dateparse import parse_datetime

from .models import Sensor


# Create your views here.
def index(request):
    filter_date = str_to_datetime_default(request.GET.get('date'))

    sensors_json = Sensor.objects.get_all_json(filter_date)
    return HttpResponse(json.dumps(sensors_json), content_type='application/json')


def activate_thread(request):
    sensor_id = request.GET.get('id')
    if sensor_id:
        if True:
            return HttpResponse(json.dump({'response': 'change', 'new_status': 'activated'}))
        return HttpResponse(json.dump({'response': 'change', 'new_status': 'deactivated'}))
    return HttpResponse(json.dump({'response': 'not found'}))


# HELPER FUNCTION, need to find a place for it, should be static
def str_to_datetime_default(query):
    if not query:
        return query
    query = datetime.strptime(query, "%Y-%m-%d_%H:%M:%S")
    return query