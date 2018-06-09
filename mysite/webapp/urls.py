from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$',views.index, name='index')
    url(r'^$', views.index, name='index'),
    url(r'^activate_thread/<id>', views.activate_thread, name='activate')
]
