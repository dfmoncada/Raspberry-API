from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$',views.index, name='index')
    url(r'^$', views.index, name='index'),
    url(r'^activate_thread/$', views.activate_thread, name='activate')
    # url(r'^activate_thread/(?P<id>\d+)$', views.activate_thread, name='activate')
]
