from django.shortcuts import render
from ventas.propuesta_corp.models import *
from ventas.seguimientos.models import *
from academico.evento.models import *
from financiero.presupuestos.models import *
from financiero.procesos_especiales.models import *
from financiero.orden_facturacion.models import OrdenFacturacion,OrdenFacturacionParticipante
from financiero.procesos_especiales.models import ProcesoEspecial
from financiero.orden_pago.models import OrdenPago
from financiero.orden_ingreso.models import OrdenIngreso
from ventas.views import get_eventos
from django.http import JsonResponse
import datetime
import operator
from django.db.models import Q
import locale
from functools import reduce

def index(request):
    dt = datetime.datetime.today()
    # locale.setlocale(locale.LC_ALL, 'es')
    propuestas=PropuestaCorporativo.objects.filter(estado="ACP",fecha_respuesta__month=dt.month,fecha_respuesta__year=dt.year)
    eventosEstados=["Programado","Reprogramado"]
    evento_presupuesto=PresupuestoEvento.objects.filter(evento__fecha_inicio__month=dt.month,evento__fecha_inicio__year=dt.year,evento__estado__in=eventosEstados).select_related('evento').order_by('evento__fecha_inicio')
    cant_prop_enviada,cant_prop_aceptada = cantidad_propuestas()
    return render(request, "index_financiero.html",{"propuestas":propuestas,
                                                "eventosProximos":evento_presupuesto,
                                                "propuestas_mensual_enviadas":cant_prop_enviada,
                                                "propuestas_mensual_aceptadas":cant_prop_aceptada,
                                                "eventos":get_eventos(),
                                                "alertas":alertas(),
                                                "evento_por_iniciar":get_eventos_iniciar(dt,eventosEstados),
                                                })

def alertas():
    alertas=dict()
    fecha = datetime.date.today()
    alertas['pres_enviado']=PresupuestoEvento.objects.filter(estado="Solicitud Enviada",fecha__year=fecha.year,fecha__month=fecha.month).count()
    alertas['pres_sin_evento']=PresupuestoEvento.objects.filter(evento__isnull=True,fecha__year=fecha.year,fecha__month=fecha.month).count()
    alertas['orden_fact']=OrdenFacturacion.objects.filter(estado="SLCE",fecha__year=fecha.year,fecha__month=fecha.month).count()
    alertas['proceso_especial']=ProcesoEspecial.objects.filter(estado="SOLI").count()
    alertas['pago_enviado']=OrdenPago.objects.filter(estado="Enviado",fecha__year=fecha.year,fecha__month=fecha.month).count()
    alertas['cobros']=OrdenIngreso.objects.filter(estado="ACTV",fecha__year=fecha.year,fecha__month=fecha.month).count()
    alertas['seguimientos_mensual_natural']=Seguimiento_PersonaNatural.objects.filter(Q(exito = "4") | Q(exito = "5"),Q(estado_participante="INSC")|Q(estado_participante="PGTO"),estado_seguimiento="CTDO",fecha_seguimiento__year=fecha.year,fecha_seguimiento__month=fecha.month).count()
    alertas['seguimientos_mensual_empresa']=SeguimientoEmpresa.objects.filter(Q(exito = 4) | Q(exito = 5),estado=3,fecha_seguimiento__year=fecha.year,fecha_seguimiento__month=fecha.month).count()
    return  alertas

def cantidad_participantes(request):
    codigoE=request.GET.get('cod_evento')
    participantes=ParticipanteIntermedio.objects.filter(cod_evento=codigoE)
    nump=participantes.count()
    return JsonResponse({'participantes': nump,'codigo':codigoE,})


def get_eventos_iniciar(time,estados):
    eventos=dict()
    #tmp=Evento.objects.filter(presupuestoevento__evento__isnull=False).distinct().filter(estado__in=estados)
    #eventos['cantidad_hoy']= tmp.filter(fecha_inicio=time).count()
    #eventos['hoy']=tmp.filter(fecha_inicio__gte=time).order_by('evento__fecha_inicio')[:10]
    tmp=PresupuestoEvento.objects.filter(evento__estado__in=estados)
    eventos['cantidad_hoy']= tmp.filter(evento__fecha_inicio=time).count()
    eventos['hoy']=tmp.filter(evento__fecha_inicio__gte=time).order_by('evento__fecha_inicio')[:10]
    return eventos


def cantidad_propuestas():
    fecha = datetime.date.today()
    return (
                PropuestaCorporativo.objects.filter(fecha_envio__year= fecha.year,fecha_envio__month = fecha.month).count(),
                PropuestaCorporativo.objects.filter(estado ="ACP" ,fecha_respuesta__year = fecha.year,fecha_respuesta__month = fecha.month).count()
           )

