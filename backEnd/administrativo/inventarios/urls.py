from django.urls import path
from django.views import generic
from . import views
from .models import *
from .views import *

urlpatterns = [
    path('', views.index_inventarios, name='index_inventarios'),
    path('nuevo/', inventarios_view.as_view(), name='inventarios_view'),
    path('ajax/load-selectores', views.load_campos_bien_inventario, name='load_selectores'),
]