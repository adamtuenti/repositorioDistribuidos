from django.urls import path
from django.views import generic
from . import views
from .models import *
from .views import *

urlpatterns = [
    path('', views.analisis_cotizaciones, name='analisis_cotizaciones'),
    path('nuevo/', nuevo_analisis.as_view(), name='nuevo_analisis'),
]   