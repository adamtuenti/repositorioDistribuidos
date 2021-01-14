from django.urls import path
from django.views import generic

from . import views
from . import forms
from .models import *
from .views import *

urlpatterns = [
    path('', views.index_suministros_egreso, name='index_suministros_egreso'),
    path('nuevo/', suministros_egreso_view.as_view(), name='suministros_egreso_view'),
    path('editar/<pk>/', suministrosEgresoUpdateView.as_view(), name='suministro_egreso_editar'),
    # path('editar_proveedor/<pk>', editar_proveedor.as_view(), name='editar_proveedor'),
]