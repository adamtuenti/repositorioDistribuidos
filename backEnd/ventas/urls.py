from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index_ventas"),
    path("ajax/load-participantes-cantidad", views.cantidad_participantes, name="menu_eventos_proximos_partC"),
]
