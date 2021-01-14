from django.urls import path
from django.views import generic

from . import views
from . import forms
from .models import *
from .views import *

urlpatterns = [
    path('', views.index_proveedores, name='index_proveedores'),
    path('nuevo/', proveedores_view.as_view(), name='proveedores_view'),
    path("ajax/load-ciudades/",views.load_ciudades, name="ajax_load_ciudades"),
    path("ajax/load-proveedor/",views.load_proveedor, name="ajax_load_proveedor"),
    path("ajax/load-all-proveedor/",views.load_all_proveedor, name="ajax_load_all_proveedor"),
    # path('editar/<pk>', views.proveedores_editar, name='proveedores_editar'),
    # path('editar/<pk>', views.editar_proveedor, name='editar_proveedor'),
    path('editar_proveedor/<pk>', editar_proveedor.as_view(), name='editar_proveedor'),
]