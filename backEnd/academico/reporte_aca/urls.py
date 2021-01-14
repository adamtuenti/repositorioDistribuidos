from django.urls import path
from django.shortcuts import *
from django.views.generic import TemplateView
from academico.reporte_aca.Acta_entrega_certificados import Acta_entrega_certificados
from academico.reporte_aca.detalle_evaulacion_evento import Detalle_evaulacion_evento
from academico.reporte_aca.Acta_nota_evento import Acta_nota_evento
from academico.reporte_aca.Acta_entrega_certificado import Acta_entrega_certificado
from academico.reporte_aca.Acta_emision_certificado_evento import Acta_emision_certificado_evento
from academico.reporte_aca.excel import export_users_xls



urlpatterns = [
    path('entrega_certificado/',Acta_entrega_certificados.as_view(),name='entrega_certificado'),
    path('detalle_evaulacion_evento/',Detalle_evaulacion_evento.as_view(),name='detalle_evaulacion_evento'),
    path('acta_nota_evento/',Acta_nota_evento.as_view(),name='acta_nota_evento'),
    path('acta_entrega_certificado/',Acta_entrega_certificado.as_view(),name='Acta_entrega_certificado'),
    path('acta_emision_certificado_evento/',Acta_emision_certificado_evento.as_view(),name='Acta_emision_certificado_evento'),
    path('excel/',export_users_xls,name='excel'),
]
