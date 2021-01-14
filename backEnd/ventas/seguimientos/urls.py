from django.urls import path
from django_filters.views import FilterView
from . import views
from . import models
from .filters import SeguimientoEmpresaFilter


urlpatterns = [
    path("personas_naturales/", views.index_persona_natural, name="index_seguimientos_personas_naturales"),
    path("evento_naturales/", views.seguimientosNaturalEventos, name="seguimiento_evento_natural"),
    path("personas_naturales/editar/<pk>/", views.segumientoNaturalEdit.as_view(), name="seguimiento_natural_editar"),
    path('personas_naturales/eliminar/<pk>/', views.segumientoNaturalDelete.as_view(), name='seguimiento_natural_eliminar'),
    path('ajax/load-modal-eliminar',views.segumientoNatural_conf_elim,name='seguimiento_natural_confirmar_eliminar'),
    path('ajax/load-eventos',views.load_eventos_participantes,name='seguimiento_evento_natural_loadEventO'),
    path('ajax/load-eventos-other',views.load_eventos_participantes_other,name='seguimiento_evento_natural_loadEventD'),
    path("interesados/", views.index_interesados, name="index_seguimientos_interesados"),
    path("interesados/editar/<pk>/", views.seguimientoInteresadoEdit.as_view(), name='seguimiento_interesados_editar'),
    #path('empresa/', FilterView.as_view(filterset_class=SeguimientoEmpresaFilter,template_name='seguimientos/empresa/index_seguimiento_empresa.html'), name='seguimiento_empresa'),
    path('empresa/', views.index_empresa , name='seguimiento_empresa'),
    path("ajax/nuevo-seguimiento-empresa",views.nuevo_seguimieto_empresa,name='nuevo_seguimiento_empresa_gg'),
    path('ajax/seguimiento-empresa-nuevo', views.SeguimientoEmpresaNuevo, name='nuevo_seguimiento_empresa'),
    path('ajax/seguimiento-empresa-eliminar', views.eliminar_seguimieto_empresa, name='eliminar_seguimiento_empresa'),
    path('empresa/eliminar/<pk>', views.SeguimientoEmpresaEliminar.as_view(), name='eliminar_seguimiento_empresa_gg'),
    path('interesados/eliminar/<pk>/', views.segumientoInteresadoDelete.as_view(), name='seguimiento_interesados_eliminar'),
    path('ajax/load-modal-eliminar-interesados',views.segumientoInteresado_conf_elim,name='seguimiento_interesados_confirmar_eliminar'),
    path('empresa/editar/<pk>', views.SeguimientoEmpresaEditar.as_view(), name='editar_seguimiento_empresa'),
    path('ajax/load-n-participantes',views.load_n_participantes,name='ajax_load_n_participantes'),
    path('ajax/load-ofertas',views.load_oferta,name='ajax_load_ofertas'),
    path('ajax/load-eventos-tipo',views.load_evento_tipo,name='ajax_load_eventos_tipo'),
]
