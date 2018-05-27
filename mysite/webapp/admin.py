from django.contrib import admin
from webapp.models import Entry, Sensor, SensorType
# Register your models here.

admin.site.register(Entry)
admin.site.register(Sensor)
admin.site.register(SensorType)