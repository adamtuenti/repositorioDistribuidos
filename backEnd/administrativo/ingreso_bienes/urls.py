from django.urls import path
from django.views import generic

from . import views
from .models import *
from .views import *

urlpatterns = [
    path('', views.consulta_bien, name='consulta_bien'),
    path('registro_bien/', registro_bien.as_view(), name='registro_bien'),
    path('nuevo/', nuevo_bien.as_view(), name='nuevo_bien'),
    path("ajax/load-bien/",views.load_bien, name="ajax_load_bien"),
    path("ajax/load-bien-detalles/",views.load_bien_detalles, name="ajax_load_bien_detalles"),
    path("ajax/load-ingreso-bienes/",views.load_ingreso_bienes, name="ajax_load_ingreso_bienes"),
    path("ajax/load-ingreso-bienes-id/",views.load_ingreso_bienes_id, name="ajax_load_ingreso_bienes_id"),
    
]