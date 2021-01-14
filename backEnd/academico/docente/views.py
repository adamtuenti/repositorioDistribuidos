from django.shortcuts import render
from django.views.generic import *
from django.shortcuts import *
from .models import *
from django.http import *
from functools import reduce
from operator import add
from django.conf import settings
from io import BytesIO
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,yellow,black
from reportlab.lib.styles import getSampleStyleSheet
from django.utils.dateparse import parse_date
from datetime import datetime,date
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, TA_CENTER
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch, mm, cm
from academico.evento.models import *
from reportlab.platypus import (
    Paragraph,
    Table,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
    Paragraph)

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from academico.reporte_aca.utils import link_callback


# Create your views here.
class DocenteFill(TemplateView):
    template_name='docente/fill.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente_id = self.kwargs['docente_pk']
        context['docente_id'] = docente_id
        return context

class DocenteCheck(TemplateView):
    template_name='docente/check.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        docente_id = self.kwargs['docente_pk']
        context['docente_id'] = docente_id
        return context

def docente_score(request,docente_pk):
    ms = {
        'actualizacionAcademica' : ActualizacionAcademica,
        'formacionDocente' : FormacionDocente,
        'experienciaDocente' : ExperienciaDocente,
        'perfil' : Perfil
    }
    score = {}
    for key, model in ms.items():
        try:
            queryset = get_list_or_404(model,docente_id = docente_pk)
            hours = list(map(lambda x: x.duracion_en_horas, queryset))
            total_hours = reduce(add, hours)            
            score[key] = total_hours
        except Http404:
            score[key] = 0
    return JsonResponse(score)

#-------Seccion de reportes------------------
# ---------Registro de asistencias del docente------------ 


def asistencia_docente(request):
    context = {}
    template_path = 'reportes/asistencia_docente.html'
    template = get_template(template_path)
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="Lista de docente.pdf"'
    html = template.render(context)
    fechaEvento = None
    try:
        if request.method == 'POST':
            cedula = request.POST.get('cedula')
            nombre = request.POST.get('nombres')
            nombreEvento= request.POST.get('evento')
            empresa = request.POST.get('empresa')
            fechaEvento= request.POST.get('fechaEvento')

            evento = Evento.objects.get(Q(codigo_evento=nombre)|Q(codigo_evento=cedula)|Q(codigo_evento=nombreEvento)|Q(codigo_evento=empresa)|Q(codigo_evento=fechaEvento))
            designEvento = DesignEvento.objects.get(Q(diseno__codigo_evento=nombreEvento)|Q(diseno__codigo_evento=empresa)|Q(diseno__codigo_evento=fechaEvento)|Q(diseno__codigo_evento=cedula)|Q(diseno__codigo_evento=nombre))
            aulas = Aula.objects.filter(Q(calendarioevento__evento=cedula)|Q(calendarioevento__evento=nombreEvento)|Q(calendarioevento__evento=empresa)|Q(calendarioevento__evento=fechaEvento))
            calendario = CalendarioEvento.objects.filter(Q(evento=nombreEvento)|Q(evento=empresa)|Q(evento=nombre)|Q(evento=cedula)|Q(evento=fechaEvento))
            context['fecha_impresion'] = date.today()
            context['aulas'] = aulas
            context['calendario'] = calendario
            context['evento'] = evento
            context['designEvento'] = designEvento
            html = template.render(context)
            response['Content-Disposition'] = 'attachment; filename="{} Sesiones del docente {} {}.pdf"'.format(evento.nombre,evento.docente.nombres,evento.docente.apellidos)
            pisaStatus = pisa.CreatePDF(
               html, dest=response, link_callback=link_callback)
            if pisaStatus.err:
               return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        context['prueba'] = 'Prueba'
        pisaStatus = pisa.CreatePDF(
           html, dest=response, link_callback=link_callback)
        if pisaStatus.err:
           return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    except Exception as e:
        raise e
        print(e)
        return redirect('participante_asistencia')
    
def docentePorCriterio(request):
    template_path = 'reportes/docente_criterio.html'
    design = DesignEvento.objects.filter()
    context = {'design':design}
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response