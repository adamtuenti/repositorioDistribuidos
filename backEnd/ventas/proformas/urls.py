from django.urls import path
from django_filters.views import FilterView
from .filters import ProformaFilter
from . import views
import ventas.reporte_contacto.views

urlpatterns = [
    path('nuevo', views.ProformaCreate.as_view(), name='proforma_nuevo'),
    path('' ,views.proforma_list, name='proforma_lista'),
    path('editar/<pk>/', views.ProformaUpdate.as_view(), name='proforma_editar'),    
    path('eliminar/<pk>/', views.ProformaDelete.as_view(), name='proforma_eliminar'),
]