from django.urls import path
from django_filters.views import FilterView
from . import views
from .filters import PropuestaCorporativoFilter
import ventas.reporte_contacto.views

momazo=PropuestaCorporativoFilter.qs


urlpatterns = [
    path('nuevo', views.PropuestaCorporativoCreate.as_view(), name='propuesta_nuevo'),
    #path('', FilterView.as_view(filterset_class=PropuestaCorporativoFilter,template_name="propuesta_corp_list.html"), name='propuesta_corporativa'),
    path('', views.propuesta_list, name='propuesta_corporativa'), 
    path('editar/<pk>/', views.PropuestaCorporativoUpdate.as_view(), name='propuesta_editar'),    
    path('eliminar/<pk>/', views.PropuestaCorporativoDelete.as_view(), name='propuesta_eliminar'),
    
    
]
