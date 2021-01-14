from django.urls import path
from django.views import generic
from . import views
from .models import *
from .views import *

urlpatterns = [
    path('', views.ordenes_compra, name='ordenes_compra'),
    path('nueva/', views.nueva_orden, name='nueva_orden'),
]