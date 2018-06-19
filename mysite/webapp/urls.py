from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$',views.index, name='index')
    url(r'^$', views.index, name='index'),
    url(r'^activate_thread/(?P<sleep>\d+)$', views.activate_thread, name='activate_thread'),
    url(r'^activate_sensor/(?P<id>\d+)$', views.activate_sensor, name='activate_sensor'),
    url(r'^deactivate_thread/$', views.deactivate_thread, name='deactivate_thread'),
    url(r'^live_read/$', views.live_read, name='live_read'),
]
