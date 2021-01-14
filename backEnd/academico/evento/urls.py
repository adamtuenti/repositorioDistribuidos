from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from academico.evento.Api import *
from .views import *


router = routers.DefaultRouter()
router.register('tipoConvenioAliado', TipoConvenioAliadoViewSet)
router.register('aliado', AliadoViewSet)
router.register('docente', DocenteViewSet)
router.register('unidadAula', UnidadAulaViewSet)
router.register('tipoAula', TipoAulaViewSet)
router.register('estadoAula', EstadoAulaViewSet)
router.register('aula', AulaViewSet)
router.register('evento', EventoViewSet)
router.register('calendarioEvento', CalendarioEventoViewSet)
router.register('co', CoViewSet)
router.register('pubEvento', PubEventoViewSet)

urlpatterns = [  
    #Evento
    path('api/event/',include(router.urls)),
    path('eventoCrear/',CrearEvento.as_view(), name = 'crearEvento'),
    path('eventoListar/',ListarEvento.as_view(), name = 'listarEvento'),
    path('convalidarEvento/',convalidar_eventos, name = 'convalidarEvento'),
    path('eventoEditar/<int:pk>',EditarEvento.as_view(), name = 'editarEvento'),
    path('eventoEliminar/<int:pk>',EliminarEvento.as_view(), name = 'eliminarEvento'),
    path('eventoDetalle/<int:pk>',DetalleEvento.as_view(), name = 'detalleEvento'),
    #Aula
    path('aulaCrear/',CrearAula.as_view(), name = 'crearAula'),
    path('aulaListar/',ListarAula.as_view(), name = 'listarAula'),
    path('aulaEditar/<int:pk>',EditarAula.as_view(), name = 'editarAula'),
    path('aulaEliminar/<int:pk>',EliminarAula.as_view(), name = 'eliminarAula'),
    #Aula
    path('aliadoCrear/',CrearAliado.as_view(), name = 'crearAliado'),
    path('aliadoListar/',ListarAliado.as_view(), name = 'listarAliado'),
    path('aliadoEditar/<int:pk>',EditarAliado.as_view(), name = 'editarAliado'),
    path('aliadoEliminar/<int:pk>',EliminarAliado.as_view(), name = 'eliminarAliado'),
    #Dia
    path('diaCrear/',DiaCrear.as_view(), name = 'crearDia'),
    path('diaListar/',ListarDia.as_view(), name = 'listarDia'),
    path('diaEditar/<int:pk>',EditarDia.as_view(), name = 'editarDia'),
    path('diaEliminar/<int:pk>',EliminarDia.as_view(), name = 'eliminarDia'),
    #Pub
    path('pubCrear/',CrearPub.as_view(), name = 'crearPub'),
    path('pubListar/',ListarPub.as_view(), name = 'listarPub'),
    path('pubDetalle/<int:pk>',infoEvento.as_view(), name = 'detallePub'),


    path('getNameE/', loadEventoName),
    #--------Seccion de reportes------------
    path('reportes_generales/',reportes_generales,name='reportes_generales'),
    path('EventoCriterio/', EventoPorCriterio, name='EventoCriterio'),
    path('EventosPorGenero/',eventos_ejecutados,name='EventosPorGenero'),
    path('Registro_asistencia_evento/',Registro_asistencia_evento.as_view(),name='Registro_asistencia_evento'),
    path('detalle_participante/',detalle_part,name='detalle_participante'),

    #---------Apis----
    
    path('GuardarConvalidacion/',GuardarConvalidacion.as_view(),name='GuardarConvalidacion'),
    path('api_participantes/',part_api.as_view(),name='api_participantes'),
    path('api_participantesEventos/',part_eventos.as_view(),name='api_participantesEventos'),
    path('EventosDestino/',eventosDestino.as_view(),name='EventosDestino'),
    
]
