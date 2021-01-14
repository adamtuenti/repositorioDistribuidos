from django.urls import path
from django.views import generic

from . import views
from . import forms
from .models import *
from .views import *

urlpatterns = [
    path('', views.index_mantenimientos, name='index_mantenimientos'),
    path('nuevo/', mantenimientos_view.as_view(), name='mantenimientos_view'),
    path('ajax/load-bienes-detalle', views.load_bien_detalles, name='load_bien_detalles'),
    path('editar/<pk>/', views.editar_mantenimiento.as_view(), name='editar_mantenimiento'),
]