from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.decorators import *
from rest_framework.renderers import *
from django.http import JsonResponse
from .models import *
from academico.participante.serializers import *

from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.views.generic import View
import xlwt
import itertools
#-------import para reportes----
from django.conf import settings
from academico.evento.models import *
from academico.diseño_evento.models import *
from django.db.models import Q
from io import BytesIO
from django.shortcuts import render, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, yellow, black
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime,date
from openpyxl import Workbook
from openpyxl.styles import Alignment,Border,Font,PatternFill,Side,Color
from academico.docente.models import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template import Context
from academico.reporte_aca.utils import link_callback
#----------------------------------
# Create your views here.

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def asistencia_by_evento_and_fecha(request):
    evento_id = request.GET.get('evento_id', None)
    fecha = request.GET.get('fecha', None)

    try:
        fecha_object = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        asistencia = Asistencia.objects.get(
            evento_id=evento_id,
            fecha=fecha_object
        )
        serializer = AsistenciaSerializer(asistencia)
        return Response(serializer.data)
    except ValueError:
        return JsonResponse({
            'detail': 'Either evento or fecha is null'
        }, status=400)
    except TypeError:
        return JsonResponse({
            'detail': 'Fecha parameter was missing'
        }, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({
            'detail': '. Not found'
        }, status=404)

#---------Seccion de reportes-------------------------

def contacto_participante(request):
    template_path = 'reportes/contacto_participante.html'
    #design = DesignEvento.objects.filter()
    #context = {'design':design}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render()
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def registro_asistencia_evento(request):
    template_path = 'reportes/registro_asistencia_evento.html'
    #design = DesignEvento.objects.filter()
    #context = {'design':design}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render()
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def reporte_asistencia(request):
    template_path = 'reportes/reporte_asistencia.html'
    #design = DesignEvento.objects.filter()
    #context = {'design':design}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render()
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def perfil_participante(request):
    template_path = 'reportes/perfil_participante.html'
    #design = DesignEvento.objects.filter()
    #context = {'design':design}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render()
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def acta_nota_evento(request):
    template_path = 'reportes/acta_nota_evento.html'
    #design = DesignEvento.objects.filter()
    #context = {'design':design}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render()
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def historico_participante(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Historial part.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    col_width = 150 * 35
    ws = wb.add_sheet('Users',cell_overwrite_ok=True)
    try:
        for i in itertools.count():
            ws.col(i).width = col_width
    except ValueError:
        pass

    ws.col(0).width = 150 * 20 
    ws.col(9).width = 150 * 23 
    ws.col(10).width = 150 * 23
    ws.col(11).width = 150 * 23   
    ws.col(7).width = 150 * 80
    ws.col(12).width = 150 * 23

    font_style = xlwt.easyxf('align: wrap on')

    mystyle = xlwt.easyxf('pattern: pattern solid, fore_colour green;'
                              'font: colour white, bold True; align: wrap on')

    ws.write_merge(0, 0, 0, 1, 'Fecha de impresion: {}'.format(date.today()))

    row_num = 2
    
    columns = [
                'Secuencia','Curso','Tipo Capacitacion','Evento programa','Promoción',
                'Fecha inicio','Fecha fin','Horario','Estado','Costo','Total horas',
                'Instructor','Área','Tipo certificado','Asistencia','Nota','Certificado recibido',
                'Modalidad','Codigo diseño','Versión','Tipo inscripción','Empresa','Aula',
                'Asesor responsable','vendedor','Coordinador responsable',
                'Fecha creacion evento','Fecha registro','Fecha Registro'
                ]


    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],mystyle)

    if request.method == 'POST':
        participante = Participante.objects.get(id=request.POST.get('participante'))
        ws.write_merge(0, 0, 2, 4, 'Nombre del participante: {} {}'.format( participante.nombres,participante.apellidos ))
        ws.write_merge(0, 0, 5, 6, 'Identificación: {}'.format(participante.identificacion))
        rows = Evento.objects.filter(eventosParticipante__id_participante=request.POST.get('participante')).select_related('diseno')
        for row in rows:
            design = row.get_design()
            aulas = row.get_aula()
            row_num += 1
            ws.write(row_num,0, row.codigo_evento,font_style)
            ws.write(row_num,1, design.cod_programa, font_style)
            ws.write(row_num,2, row.tipo_evento, font_style)
            ws.write(row_num,3, row.nombre, font_style)
            ws.write(row_num,4, row.promocion, font_style)
            ws.write(row_num,5, str(row.fecha_inicio), font_style)
            ws.write(row_num,6, str(row.fecha_fin), font_style)
            ws.write(row_num,7, str(str(row.horarios())), font_style)
            ws.write(row_num,8, row.estado, font_style)
            ws.write(row_num,9, str(row.centro_costos), font_style)
            ws.write(row_num,10, str(design.horas_totales), font_style)
            ws.write(row_num,11, 'Nombres: {} Apellidos: {}'.format(row.docente.nombres,row.docente.apellidos), font_style)
            ws.write(row_num,12, design.area.area, font_style)
            ws.write(row_num,13, design.tipo_certificado, font_style)
            ws.write(row_num,14, 'Falta este campo', font_style)
            ws.write(row_num,15, 'Falta este campo', font_style)
            ws.write(row_num,16, 'Falta este campo', font_style)
            ws.write(row_num,17, row.modalidad, font_style)
            ws.write(row_num,18, design.codigo, font_style)
            ws.write(row_num,19, design.version, font_style)
            ws.write(row_num,20, 'Falta este campo', font_style)
            if row.tipo_evento == 'corporativo':
                 empresa = PresupuestoEvento.obejcts.get(evento=row.codigo_evento)
                 ws.write(row_num,21,empresa.razon_nombres, font_style)
            else:
                ws.write(row_num,21,'Ninguno', font_style)

            ws.write(row_num,22,aulas.aula.nombre,font_style)
            ws.write(row_num,23,row.asesor_comercial_responsable,font_style)
            ws.write(row_num,24,'Falta este campo',font_style)
            ws.write(row_num,25,str(design.fecha),font_style) 
            ws.write(row_num,25,'Falta fecha registro',font_style) 
    wb.save(response)
    return response

def asistencia(request):   
    evento = Evento.objects.filter(Q(estado='Ejecutado'))
    return render(request,'asistencia.html',{'evento':evento})

           
def part_reprobados(request):
    template_path = 'reportes/reprobados_por_evento.html'
    #design = DesignEvento.objects.filter()
    context = {'design':'#'}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def cierre_eventos(request):
    context={}
    if request.POST:
        evento = Evento.objects.get(codigo_evento=request.POST['codigo_evento'])
        evento.estado = request.POST['estado']
        for opcion in request.POST.getlist('a'):
            if opcion=="asistencias":
                evento.cierre_asistencias = True
            if opcion=="calificaciones":
                evento.cierre_calificaciones = True
            if opcion=="informes":
                evento.habilitar_informes = True
            if opcion=="certificados":
                evento.generar_certificados = True
            if opcion=="notificaciones":
                evento.notificaciones = True
        evento.save()
        return render(request,'cierre_eventos.html',context)
    return render(request,'cierre_eventos.html',context)

def registrar_notas1(request):
    context={}
    return render(request,'registrar_notas1.html',context)

def registrar_notas_mejoramiento(request):
    context={}
    return render(request,'registrar_notas_mej.html',context)

def corregir_notas(request):
    context={}
    return render(request,'corregir_notas.html',context)

def aprobar_notas(request):
    context={}
    return render(request,'aprobar_notas.html',context)