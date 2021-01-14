from django.urls import path, include
from django.shortcuts import *
from academico.participante.views import *
from django.views.generic import TemplateView
from .views import *
from academico.participante.Api import *

urlpatterns = [
    path('asistencia/', asistencia, name="participante_asistencia"),
    path('login_participante/',login_participante.as_view(),name='login_participante'),
    path('existe_participante/',existe_participante.as_view(),name='existe_participante'),
    path('notificaciones_participante/',notificaciones_participante.as_view(),name='notificaciones_participante'),
    path('actualizar_notificacion/',actualizar_notificacion.as_view(),name='actualizar_notificacion'),
    path('cursos_participante/',cursos_participante.as_view(),name='cursos_participante'),
    path('detalles_curso/',detalles_curso.as_view(),name='detalles_curso'),
    path('asistencia/by_evento_and_fecha', asistencia_by_evento_and_fecha, name="asistencia_by_evento_and_fecha"),
    #---------Reporte----------
    path('ParticipantesReprobados/', part_reprobados,name='Part_Reprobados'),
    path('historico_participante/', historico_participante, name='historico_participante'),
    #--------
    path('contacto_participante',contacto_participante,name='contacto_participante'),
    path('registro_asistencia_evento/',registro_asistencia_evento,name='registro_asistencia_evento'),
    path('reporte_asistencia',reporte_asistencia,name='reporte_asistencia'),
    path('perfil_participante',perfil_participante,name='perfil_participante'),
    #-----
    path('acta_nota_evento',acta_nota_evento,name='acta_nota_evento'),
    path('cierre_eventos',cierre_eventos,name='cierre_eventos'),
    path('registrar_notas_1raevaluacion',registrar_notas1,name='registrar_notas1'),  
    path('registrar_notas_mejoramiento',registrar_notas_mejoramiento,name='registrar_notas_mejoramiento'),    
    path('rectificar_notas',corregir_notas,name='corregir_notas'),
    path('aprobar_notas',aprobar_notas,name='aprobar_notas'),
]
