from django.urls import path
from django.views import generic

from . import views
from . import forms
from .models import *
from ventas.personas_juridicas.models import Juridica
urlpatterns = [
    path('', views.index_presupuestos, name='index_presupuestos'),
    path('nuevo/', views.PresupuestoEventoCreate.as_view(), name='nuevo_presupuestos'),
    path('editar/<pk>', views.PresupuestoEventoUpdate.as_view(), name='editar_presupuestos'),
    path('ajax/load-elminar-presupuesto',views.presupuesto_conf_elim,name='presupuesto_confirmar_eliminar'),
    path('eliminar/<pk>/', views.PresupuestoEventoDelete.as_view(), name='presupuesto_eliminar'),
    path('ajax/cargar-valor', views.cargar_info, name="ajax_cargar_valor"),
    path('aprobar/<pk>',views.PresupuestoEventoAprobar.as_view(), name="presupuesto_aprobar"),
    path('anular/<pk>',views.anular_presupuesto, name="presupuesto_anular"),
    path('ajax/load-eventos',views.load_eventos,name='ajax_load_eventos_presupuestos'),
    path('ajax/load-all-eventos',views.load_all_eventos,name='ajax_load_all_eventos_presupuestos'),
]
    

