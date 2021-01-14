from django.shortcuts import render
from ventas.propuesta_corp.models import *
from ventas.seguimientos.models import *
from academico.evento.models import *
from financiero.presupuestos.models import *
from financiero.procesos_especiales.models import *
from financiero.orden_facturacion.models import OrdenFacturacion,OrdenFacturacionParticipante
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
    proximos_seguimientos, cantidad_seguimientos = get_seguimientos_date(request.user)
    cant_mensual_natural,cant_mensual_empresa,cant_mensual_interesados = get_seguimientos_mensual_quantity()
    cant_prop_enviada,cant_prop_aceptada = cantidad_propuestas()
    return render(request, "index_ventas.html",{"propuestas":propuestas,  
                                                "eventosProximos":evento_presupuesto,
                                                "proximos_seguimientos":proximos_seguimientos,
                                                "seguimientos_hoy":cantidad_seguimientos,
                                                "seguimientos_mensual_natural":cant_mensual_natural,
                                                "seguimientos_mensual_empresa":cant_mensual_empresa,
                                                "seguimientos_mensual_interesados":cant_mensual_interesados,
                                                "propuestas_mensual_enviadas":cant_prop_enviada,
                                                "propuestas_mensual_aceptadas":cant_prop_aceptada,
                                                "eventos":get_eventos()
                                                })


def cantidad_participantes(request):
    codigoE=request.GET.get('cod_evento')
    participantes=ParticipanteIntermedio.objects.filter(cod_evento=codigoE)
    nump=participantes.count()
    return JsonResponse({'participantes': nump,'codigo':codigoE,})




def get_seguimientos_date(user):
    return  (
                Seguimiento_PersonaNatural.objects.filter(estado_seguimiento="PCTC").filter(asesor=user).filter(fecha_seguimiento__gte=datetime.date.today()).order_by('fecha_seguimiento')[:10],
                Seguimiento_PersonaNatural.objects.filter(estado_seguimiento="PCTC").filter(fecha_seguimiento=datetime.date.today()).filter(asesor=user).count()
            )


def get_seguimientos_mensual_quantity():
    fecha = datetime.date.today()
    return  (
                Seguimiento_PersonaNatural.objects.filter(estado_seguimiento="PCTC",fecha_seguimiento__year=fecha.year,fecha_seguimiento__month=fecha.month).count(),
                SeguimientoEmpresa.objects.filter(estado=1,fecha_seguimiento__year=fecha.year,fecha_seguimiento__month=fecha.month).count(),
                Seguimiento_Interesados.objects.filter(estado_seguimiento="PCTC",fecha_seguimiento__year=fecha.year,fecha_seguimiento__month=fecha.month).count()
            )


def cantidad_propuestas():
    fecha = datetime.date.today()
    return (
                PropuestaCorporativo.objects.filter(fecha_envio__year= fecha.year,fecha_envio__month = fecha.month).count(),
                PropuestaCorporativo.objects.filter(estado ="ACP" ,fecha_respuesta__year = fecha.year,fecha_respuesta__month = fecha.month).count()
           )
def get_eventos():
    eventos = dict()
    fecha = datetime.date.today()

    #Eventos con y sin presupuesto
    eventos_sin_presupuesto = Evento.objects.filter(presupuestoevento__isnull = True) 
    eventos_con_presupuesto = Evento.objects.filter(presupuestoevento__isnull = False)

    # Publico del evento
    eventos_abiertos = eventos_con_presupuesto.filter(publico = "Abierto")
    eventos_corporativos = eventos_con_presupuesto.filter(publico = "Corporativo") 
    eventos_abiertos_sp = eventos_sin_presupuesto.filter(publico = "Abierto")
    eventos_corporativos_sp = eventos_sin_presupuesto.filter(publico = "Corporativo")

    #Eventos abiertos
    eventos_activos_abiertos= eventos_abiertos.filter(estado = "Activo")
    eventos_programados_abiertos = eventos_abiertos.filter(Q(estado = "Programado")|Q(estado = "Reprogramado"))
    eventos_finalizados_abiertos = eventos_abiertos.filter(estado = "Ejecutado")

    #Eventos corporativos
    eventos_activos_corporativos= eventos_corporativos.filter(estado = "Activo")
    eventos_programados_corporativos = eventos_corporativos.filter(Q(estado = "Programado")|Q(estado = "Reprogramado"))
    eventos_finalizados_corporativos = eventos_corporativos.filter(estado = "Ejecutado")

    #Cantidad de Eventos abiertos
    cantidad_activos_abiertos = eventos_activos_abiertos.count()
    cantidad_programados_abiertos = eventos_programados_abiertos.filter(fecha_inicio__day__gte = fecha.day,fecha_inicio__month = fecha.month , fecha_inicio__year = fecha.year).count()
    cantidad_programados_abiertos_sp = eventos_abiertos_sp.filter(Q(estado = "Programado")|Q(estado = "Reprogramado"), fecha_inicio__day__gte = fecha.day,fecha_inicio__month = fecha.month , fecha_inicio__year = fecha.year ).count()
    total_programados_abiertos = cantidad_programados_abiertos_sp + cantidad_programados_abiertos
    cantidad_finalizados_abiertos = eventos_finalizados_abiertos.filter(fecha_fin__day__lte = fecha.day,fecha_fin__month = fecha.month, fecha_fin__year = fecha.year).count()

    #Cantidad de Eventos corporativos
    cantidad_activos_corporativos = eventos_activos_corporativos.count()
    cantidad_programados_corporativos = eventos_programados_corporativos.filter(fecha_inicio__day__gte = fecha.day,fecha_inicio__month = fecha.month , fecha_inicio__year = fecha.year).count()
    cantidad_programados_corporativos_sp = eventos_corporativos_sp.filter(Q(estado = "Programado")|Q(estado = "Reprogramado"), fecha_inicio__day__gte = fecha.day,fecha_inicio__month = fecha.month , fecha_inicio__year = fecha.year ).count()
    total_programados_corporativos = cantidad_programados_corporativos + cantidad_programados_corporativos_sp
    cantidad_finalizados_corporativos =eventos_finalizados_corporativos.filter(fecha_fin__day__lte = fecha.day,fecha_fin__month = fecha.month, fecha_fin__year = fecha.year).count()

    #Participantes en formacion
    cantidad_participantes_formacion = ParticipanteIntermedio.objects.filter(evento__estado = "Activo").count()
    #Clientes in House
    cantidad_clientes = ParticipanteIntermedio.objects.filter(evento__estado = "Activo", evento__publico = "Corporativo" , orden__tipo_cliente = "Jurídica").order_by("orden__ruc_ci").distinct("orden__ruc_ci").count()



    eventos["evento_abierto_activo"] = cantidad_activos_abiertos
    eventos["evento_abierto_planificado"] = total_programados_abiertos
    eventos["evento_abierto_ejecutado"] = cantidad_finalizados_abiertos
    eventos["evento_corporativo_activo"] = cantidad_activos_corporativos
    eventos["evento_corporativo_planificado"] = total_programados_corporativos
    eventos["evento_corporativo_ejecutado"] = cantidad_finalizados_corporativos
    eventos["evento_sin_presupuesto"] = cantidad_programados_abiertos_sp + cantidad_programados_corporativos_sp
    eventos["participantes_en_formacion"] = cantidad_participantes_formacion
    eventos["cliente_in_house"] = cantidad_clientes

    return eventos
    