import json
import threading

from django.http import HttpResponse, JsonResponse
from datetime import datetime

from .models import Sensor
from .classes.elements_manager import ElementManager


# Create your views here.
def index(request):
    filter_date = str_to_datetime_default(request.GET.get('date'))

    sensors_json = Sensor.objects.get_all_json(filter_date)
    return HttpResponse(json.dumps(sensors_json), content_type='application/json')


def activate_thread(request):
    if True:
        threading.Thread(target=ElementManager.start_read_thread(), args=(), kwargs={})
        return JsonResponse({'response': 'change', 'new_status': 'activated'})
    return JsonResponse({'response': 'change', 'new_status': 'deactivated'})
    # return JsonResponse({'response': 'not found'})

def activate_sensor(request, id):
    return HttpResponse()


# HELPER FUNCTION, need to find a place for it, should be static
def str_to_datetime_default(query):
    if not query:
        return query
    query = datetime.strptime(query, "%Y-%m-%d_%H:%M:%S")
    return query