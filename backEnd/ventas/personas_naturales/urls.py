from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='natural_lista'),
    path('nuevo/', views.natural_nuevo, name='natural_nuevo'),
    path('nuevo_t/', views.natural_nuevo_t, name='natural_nuevo_t'),
    path('editar/<pk>/', views.NaturalUpdate.as_view(), name='natural_editar'),
    path('eliminar/', views.natural_delete, name='natural_eliminar'),
    path('eliminar/<pk>/', views.natural_delete, name='natural_eliminar'),
    path('seguimiento/nuevo/', views.seguimientoNaturalCreate, name='seguimiento_natural_create'),
    path('ajax/crear-seguimiento', views.crear_seguimiento_natural, name='ajax_seguimiento_create'),
    path('ajax/load-eventos', views.cargarEventosNatural, name='ajax_load_eventos_Natural'),
]