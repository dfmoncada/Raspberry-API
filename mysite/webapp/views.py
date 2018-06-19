import json
import threading

from django.http import HttpResponse, JsonResponse
from datetime import datetime

from .models import Sensor


# Create your views here.
def index(request):
    filter_date = str_to_datetime_default(request.GET.get('date'))
    sensors_json = Sensor.objects.get_all_json(filter_date)
    return HttpResponse(json.dumps(sensors_json), content_type='application/json')

# Thread is not starting on the background, so the page get's stuck after starting it.
def activate_thread(request, sleep = 60):
    return JsonResponse(Sensor.objects.activate_thread(sleep))

def deactivate_thread(request):
    return JsonResponse(Sensor.objects.deactivate_thread())

def activate_sensor(request, id):
    return JsonResponse({'response':'Sensors activated (not implemented)', 'sensor_id':id})

def live_read(request):
    sensors_live_json = Sensor.objects.get_all_live_json()
    return JsonResponse({'response':'Ok', 'data':sensors_live_json})

# HELPER FUNCTION, need to find a place for it, should be static
def str_to_datetime_default(query):
    if not query:
        return query
    query = datetime.strptime(query, "%Y-%m-%d_%H:%M:%S")
    return query
