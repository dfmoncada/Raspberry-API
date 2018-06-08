import json

from django.http import HttpResponse
from django.utils.dateparse import parse_datetime

from .models import Sensor


# Create your views here.
def index(request):
    filter_date = str_to_datetime_default(request.GET.get('date'))

    sensors_json = Sensor.objects.get_all_json(filter_date)
    return HttpResponse(json.dumps(sensors_json), content_type='application/json')


def str_to_datetime_default(query):
    if not query:
        return query
    query = list(query)
    query[-6] = '+'
    query = "".join(query)
    return parse_datetime(query)
