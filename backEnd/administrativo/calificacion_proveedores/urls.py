from django.urls import path
from django_filters.views import FilterView
from django.views import generic

from . import views
from . import forms
from .models import *
from .views import *


urlpatterns = [
    path('', views.index_calificacion_proveedores, name='index_calificacion_proveedores'),
    path('nuevo/', calificacion_proveedores_view.as_view(), name='calificacion_proveedores_view'),
    # path("ajax/load-egresos/", views.load_egresos, name="ajax_load_egresos"),
    path('editar_calificacion_proveedor/<pk>', editar_calificacion_proveedor.as_view(), name='editar_calificacion_proveedor'),


]