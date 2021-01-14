from django.urls import path
from django.views import generic

from . import views
from .models import *

urlpatterns = [
    path('', views.index, name='procesos_especiales_index'),
    path('cambiarParticipante',views.cambiarParticipante,name='cambiarParticipante_modal'),    
    path('cambiarParticipanteCreate',views.cambiarParticipanteCreate,name='cambiarParticipanteCreate'),  
    path('ajax/load-eventosPE',views.load_eventos,name='ajax_load_eventosPE'), 
    path('ajax/load-eventosIndPE',views.load_eventosInd,name='ajax_load_eventosIndPE'),
    path('ajax/load-participantesPE',views.load_participantes_eventos,name='ajax_load_participantes_eventosPE'), 
    path('ajax/load-naturalesNoEventoPE',views.load_naturales_no_evento,name='ajax_load_naturales_no_eventoPE'),
    path('cambiarEvento',views.cambiarEventorender,name='cambiarEvento_modal'),
    path('cambiarEventoCreate',views.cambiarEventoCreate,name='cambiarEventoCreate'), 
    path('ajax/load-participantesTodosPE',views.load_participantes_todos,name='ajax_load_participantesTodosPE'),
    path('ajax/load-eventosPartPE',views.load_eventos_participantes,name='ajax_load_partEventoPE'), 
    path('ajax/load-eventosNoPartPE',views.load_eventosNo_participantes,name='ajax_load_nopartEventoPE'), 
    path('editar/<pk>/', views.ProcesoEspecialUpdate.as_view(), name='proceso_especial_editar'),  
    path('ajax/load-participantesEditPE',views.cambiarEvento,name='ajax_load_participantesEditPE'),
    path('ajax/load-participantesList',views.load_participantes_list,name='ajax_load_partListPE'),
    path('ajax/verificarAsistencia',views.verificarAsistencia,name='ajax_verificar_asistenciaPE'),
    path('ajax/verificarAsistenciaCambParticipante',views.verificarAsistenciaCambPart,name='ajax_verificar_asistenciaCP'),
    path('ajax/load-personas',views.agregarPersonaNaturalModal,name='ajax_load_personasPE'),
    path('ajax/load-personasList',views.agregarPersonaNatural,name='ajax_load_personasListPE'),
    path('ajax/alerta-CuponGratis',views.alertaPersonCuponGratis,name='ajax_alerta_cuponGratisPE'),
    path('crearCuponGratis',views.CuponGratis.as_view(),name='crear_cupon'),
    path('crearDevolucion',views.Devolucion.as_view(),name='crear_devolucion'),
    path('autorizarProcesoEspecial/<pk>/',views.ProcesoEspecialAutorizar.as_view(),name='autorizar_proceso_especial'),
    path('anular/<pk>',views.anular_proceso_especial, name="anualar_proceso_especial"),
    path('aprobar/<pk>',views.aprobar_proceso_especial, name="aprobar_proceso_especial"),
]
    

