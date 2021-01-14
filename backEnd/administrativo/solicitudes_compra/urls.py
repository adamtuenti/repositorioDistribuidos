from django.urls import path
from django.views import generic
from . import views
from .models import *
from .views import *

urlpatterns = [
    path('', views.solicitudes_compra, name='solicitudes_compra'),
    path('nueva/', nueva_compra.as_view(), name='nueva_compra'),
    path('editar/<pk>/', views.solicitud_editar.as_view(), name='solicitud_editar'),
]
