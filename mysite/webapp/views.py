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
    if not ElementManager.element_manager:
        ElementManager.element_manager = ElementManager()
        try:
            sleep = int(sleep)
        except:
            return JsonResponse({'response':'error', 'message':'input a correct integer value'})
        threading.Thread(target=ElementManager.element_manager.start_read_thread, args={sleep}, kwargs={}).start()
        return JsonResponse({'response':'change', 'new_status': 'activated'})
    return JsonResponse({'response': 'unchanged', 'status': 'activated'})
    # return JsonResponse({'response': 'not found'})

def deactivate_thread(request):
    changed = 'unchanged'
    if ElementManager.element_manager:
        changed = 'changed'
        ElementManager.element_manager.deactivate_thread()
    return JsonResponse({'response':changed,'status':'deactivated'})
        

def activate_sensor(request, id):
    return JsonResponse({'response':'Sensors activated (not implemented)', 'sensor_id':id})


# HELPER FUNCTION, need to find a place for it, should be static
def str_to_datetime_default(query):
    if not query:
        return query
    query = datetime.strptime(query, "%Y-%m-%d_%H:%M:%S")
    return query
