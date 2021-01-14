from django.urls import path
from django.views import generic

from . import views
from . import forms
from .models import *
from .views import *

urlpatterns = [
    path('', views.index_suministros, name='index_suministros'),
    path('nuevo/', suministros_view.as_view(), name='suministros_view'),
    path('ajax/load-productos', views.load_productos, name='load_productosS'),
    path('ajax/load-producto-detalle', views.load_producto_detalles, name='load_producto_datalleS'),
    path('editar_suministro/<pk>/', views.suministrosUpdateView.as_view(), name='suministro_editar'),  
    # path('editar_proveedor/<pk>', editar_proveedor.as_view(), name='editar_proveedor'),
]