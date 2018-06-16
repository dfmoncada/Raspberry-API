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

# Thread is not starting on the background, so the page get's stuck after starting it.
def activate_thread(request, sleep = 60):
    print(ElementManager.thread, ElementManager.active ,'hola')
    if not ElementManager.thread:
        ElementManager.thread = threading.Thread(target=ElementManager.start_read_thread, args={sleep}, kwargs={})
        ElementManager.active = True
        ElementManager.thread.start()
        return JsonResponse({'response':'change', 'new_status': 'activated'})
    return JsonResponse({'response': 'unchanged', 'status': 'activated'})
    # return JsonResponse({'response': 'not found'})

def deactivate_thread(request):
    changed = 'unchanged'
    if ElementManager.active:
        changed = 'changed'
    ElementManager.active = False
    return JsonResponse({'response':changed,'status':'deactivated'})
        

def activate_sensor(request, id):
    return JsonResponse({'response':'Sensors activated (not implemented)'})


# HELPER FUNCTION, need to find a place for it, should be static
def str_to_datetime_default(query):
    if not query:
        return query
    query = datetime.strptime(query, "%Y-%m-%d_%H:%M:%S")
    return query
