from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, HttpResponseForbidden
from django.forms.models import inlineformset_factory, modelformset_factory
from django.core import serializers
from financiero.presupuestos.models import PresupuestoEvento
from rest_framework import viewsets
from django.db.models import Q
from .serializers import *
import json
from .models import Evento, Aula, Aliado, CalendarioEvento, Docente, Co, PubEvento
from academico.evento.models import *
from academico.diseño_evento.models import *
from academico.docente.models import *
from academico.participante.models import *
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView, DetailView, View
from django.views.generic.edit import FormMixin
from .forms import EventoForm, AulaForm, AliadoForm, CalendarioForm, CalendarioFormSet, CoForm, CoFormSet, PubForm
#-------import para reportes----
from django.conf import settings
from io import BytesIO
from django.shortcuts import render, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,yellow,black
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime,date


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from academico.reporte_aca.utils import link_callback


#----------------------------------
# Create your views here.

#Api event
class TipoConvenioAliadoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoConvenioAliadoSerializer
    queryset = TipoConvenioAliado.objects.all()

class AliadoViewSet(viewsets.ModelViewSet):
    serializer_class = AliadoSerializer
    queryset = Aliado.objects.all()

class DocenteViewSet(viewsets.ModelViewSet):
    serializer_class = DocenteSerializer
    queryset = Docente.objects.all()

class UnidadAulaViewSet(viewsets.ModelViewSet):
    serializer_class = UnidadAulaSerializer
    queryset = UnidadAula.objects.all()

class TipoAulaViewSet(viewsets.ModelViewSet):
    serializer_class = TipoAulaSerializer
    queryset = TipoAula.objects.all()

class EstadoAulaViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoAulaSerializer
    queryset = EstadoAula.objects.all()    

class AulaViewSet(viewsets.ModelViewSet):
    serializer_class = AulaSerializer
    queryset = Aula.objects.all()

class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    queryset = Evento.objects.all()

class CalendarioEventoViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarioEventoSerializer
    queryset = CalendarioEvento.objects.all()

class CoViewSet(viewsets.ModelViewSet):
    serializer_class = CoSerializer
    queryset = Co.objects.all()

class PubEventoViewSet(viewsets.ModelViewSet):
    serializer_class = PubEventoSerializer
    queryset = PubEvento.objects.all()

#Eventos
class CrearEvento(CreateView):
    model = Evento
    template_name = 'eventos/crearEvento.html'
    form_class = EventoForm
    success_url = reverse_lazy('listarEvento')
    
    def get_context_data(self, **kwargs):
        context = super(CrearEvento, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = CalendarioFormSet(queryset=CalendarioEvento.objects.none(), prefix='calendario')
        if 'form3' not in context:
            context['form3'] = CoFormSet(queryset=Co.objects.none(), prefix='cofaci')
        context['docente'] = Docente.objects.all()
        context['diseno'] = DesignEvento.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        #print('<--Datos del formulario crear evento-->')
        #print(form.data['diseno'])
        #print(form.data['codigo_evento'])
        #print(form.data['nombre'])
        #print(form.data['tipo_evento'])
        #print(form.data['codigo_evento_padre'])
        #print(form.data['nombre_evento_Padre'])
        #print(form.data['modalidad'])
        #print(form.data['centro_costos'])
        #print(form.data['alcance'])
        #print(form.data['promocion'])
        #print(form.data['duracion'])
        #print(form.data['aliado'])
        #print(form.data['docente'])
        #print(form.data['lugar'])
        #print(form.data['asesor_comercial_responsable'])
        #print(form.data['hora_break'])
        #print(form.data['servicios_incluidos'])
        #print(form.data['hora_almuerzo'])
        #print(form.data['opciones_de_calendario'])
        #print(form.data['fecha_inicio'])
        #print(form.data['fecha_fin'])
        #print(form.data['estado'])
        #print(form.data['web'])
        #print('<----------------------------------->')


        form2 = CalendarioFormSet(request.POST, prefix='calendario')
        form3 = CoFormSet(request.POST, prefix='cofaci')
        print(form2.errors)
        
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            
            eve = form.save(commit=False)
            eve.save()
            instancesdia = form2.save(commit=False)
            for instanced in instancesdia:
                instanced.evento = eve
                instanced.save()
            instancesco = form3.save(commit=False)
            for instance in instancesco:
                instance.evento = eve
                instance.save()
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            print('Error del formulario crear evento')
            print(form2.errors)
            print(form.errors)
            print(form3.errors)
            return self.render_to_response(self.get_context_data(form='form',form2='form2',form3='form3'))


class ListarEvento(ListView):
    model=Evento
    template_name='eventos/listarEvento.html'
    queryset = Evento.objects.all()

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['object_list'] = self.get_queryset()
        contexto['design'] = DesignEvento.objects.filter(estado='activo')
        contexto['areas'] = Area.objects.all()
        contexto['aulas'] = Aula.objects.all()
        return contexto


class EditarEvento(UpdateView):
    model = Evento
    template_name='eventos/crearEvento.html'
    form_class=EventoForm
    success_url = reverse_lazy('listarEvento')

    def get_context_data(self, **kwargs):
        context = super(EditarEvento, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        evento = self.model.objects.get(codigo_evento=pk)
        calendarios_days = CalendarioEvento.objects.filter(id=evento.codigo_evento)
        co = Co.objects.filter(id=evento.codigo_evento)
        if 'form' not in context:
            context['form'] = self.form_class()
        """if 'form2' not in context:
            context['form2'] = CalendarioFormSet(queryset=CalendarioEvento.objects.filter(evento_id=evento.codigo_evento))
        if 'form3' not in context:
            context['form3'] = CoFormSet(queryset=Co.objects.filter(evento_id=evento.codigo_evento))
        context['id'] = pk"""
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_evento = kwargs['pk']
        evento = self.model.objects.get(codigo_evento=id_evento)
        calendarios_days = CalendarioEvento.objects.filter(evento_id=evento.codigo_evento)
        co = Co.objects.filter(id=evento.codigo_evento)
        form = self.form_class(request.POST, instance=evento)
        print(form.is_valid())
        """form2 = CalendarioFormSet(request.POST, queryset=CalendarioEvento.objects.filter(evento_id=evento.codigo_evento))
        print(form2.errors)
        form3 = CoFormSet(request.POST, queryset=Co.objects.filter(evento_id=evento.codigo_evento))
        #print(form3.errors)"""

        if form.is_valid(): #and form2.is_valid() and form3.is_valid():
            #evento_modificado = form.save(commit=False)
            form.save()
            """instances = form2.save(commit=False)
            instances2 = form3.save(commit=False)
            print(evento.codigo_evento)
            for ce in instances:
                ce.evento = evento
                ce.save()

            for c in instances2:
                c.evento = evento
                c.save()"""
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            """if not form3.is_valid():
                print('form 3 no valida')
            if not form2.is_valid():
                print('form 2 no valida')"""
            if not form.is_valid():
                print('form 1 no son valida')
            return HttpResponseRedirect(self.get_success_url())

class EliminarEvento(DeleteView):
    model=Evento
    template_name="eventos/eliminarEvento.html"
    success_url=reverse_lazy('listarEvento')

#Aliados
class CrearAliado(CreateView):
    model=Aliado
    template_name="aliados/crearAliado.html"
    #success_message= 'El aliado ha sido creado con exito'
    form_class=AliadoForm
    success_url=reverse_lazy('listarAliado')

class ListarAliado(ListView):
    model=Aliado
    template_name="aliados/listarAliado.html"

class EditarAliado(UpdateView):
    model=Aliado
    template_name="aliados/crearAliado.html"
    form_class=AliadoForm
    success_url=reverse_lazy('listarAliado')

class EliminarAliado(DeleteView):
    model=Aliado
    template_name="aliados/eliminarAliado.html"
    success_url=reverse_lazy('listarAliado')

#Aulas
class CrearAula(CreateView):
    model = Aula
    template_name = 'aulas/crearAula.html'
    #success_message= 'El aula ha sido creada con exito'
    form_class = AulaForm
    success_url=reverse_lazy('listarAula')

class ListarAula(ListView):
    model=Aula
    template_name="aulas/listarAula.html"

class EditarAula(UpdateView):
    model=Aula
    template_name="aulas/crearAula.html"
    form_class=AulaForm
    success_url=reverse_lazy('listarAula')

class EliminarAula(DeleteView):
    model=Aula
    template_name="aulas/eliminarAula.html"
    success_url=reverse_lazy('listarAula')

class DiaCrear(CreateView):
    model = CalendarioEvento
    template_name = 'dias/crearDia.html'
    form_class = CalendarioForm
    success_url = reverse_lazy('listarDia')

class EditarDia(UpdateView):
    model = CalendarioEvento
    template_name = 'dias/crearDia.html'
    form_class = CalendarioForm
    success_url=reverse_lazy('listarDia')

class ListarDia(ListView):
    model = CalendarioEvento
    template_name = 'dias/listarDia.html'

class EliminarDia(DeleteView):
    model = CalendarioEvento
    template_name="dias/eliminarDia.html"
    success_url=reverse_lazy('listarDia')

class CrearPub(CreateView):
    model = PubEvento
    template_name='pub/crearPub.html'
    form_class = PubForm
    success_url=reverse_lazy('listarPub')

class ListarPub(ListView):
    model = PubEvento
    template_name = 'pub/listarPub.html'

class DetalleEvento(FormMixin, DetailView):
    model = Evento
    form_class = PubForm
    template_name='pub/crearPub.html'

    def get_context_data(self, **kwargs):
        context = super(DetalleEvento, self).get_context_data(**kwargs)
        #self.object.web = 'Publicado'
        #self.object.save(update_fields=['web'])
        return context

    def get_success_url(self):
        return reverse('listarEvento')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

class infoEvento(DetailView):
    model = PubEvento
    template_name='pub/infoPub.html'

def convalidar_eventos(request):
    return render(request,'eventos/convalidar_evento.html')

#consultas
def loadEventoName(request):
    event = Evento.objects.all()
    json_event = serializers.serialize('json', event)
    return HttpResponse(json_event, content_type='application/json')




#--------------Seccion de reportes----------------
import xlwt
import itertools

def EventoPorCriterio(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Reporte evento.xls"'
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
                'Codigo evento','Curso','Tipo Capacitacion','Evento programa',
                'Promoción','Fecha inicio','Fecha fin','Horario','Estado',
                'Participantes registrados','Costo','Horas','Instructor',
                'Área','Tipo de certificado','Modalidad','Empresa','Aula',
                'Asesor responsable','Coordinador responsable','Fecha creación evento'
                ]


    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],mystyle)

    if request.method == 'POST':
        if not  request.POST.get('areas') and not request.POST.get('fechaInicio') and not request.POST.get('fechaFin') and not request.POST.get('coordinador')  and not request.POST.get('estado') and not request.POST.get('periodo') and not request.POST.get('asesor') and not request.POST.get('publico'):
            rows = Evento.objects.all()
            for row in rows:
                cant_participantes = Participante.objects.filter(evento__codigo_evento=row.codigo_evento).count()
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
                ws.write(row_num,9, str(cant_participantes), font_style)
                ws.write(row_num,10, row.centro_costos, font_style)
                ws.write(row_num,11, str(design.horas_totales), font_style)
                ws.write(row_num,12, 'Nombres: {} Apellidos: {}'.format(row.docente.nombres,row.docente.apellidos), font_style)
                ws.write(row_num,13, design.area.area, font_style)
                ws.write(row_num,14, design.tipo_certificado, font_style)
                ws.write(row_num,15, row.modalidad, font_style)
                if row.tipo_evento == 'corporativo':
                     ws.write(row_num,16,'Falta nombre empresa', font_style)
                else:
                    ws.write(row_num,16,'Ninguno', font_style)

                ws.write(row_num,17,aulas.aula.nombre,font_style)
                ws.write(row_num,18,row.asesor_comercial_responsable,font_style)
                ws.write(row_num,19,'Preguntar sobre este campo',font_style)
                ws.write(row_num,20,str(design.fecha),font_style)

        else:
            rows = Evento.objects.filter(Q(asesor_comercial_responsable=request.POST.get('asesor'))|Q(diseno__area=request.POST.get('areas')) |Q(codigo_evento=request.POST.get('fechaInicio')) |Q(codigo_evento=request.POST.get('fechaFin')) | Q(codigo_evento= request.POST.get('coordinador')) | Q(codigo_evento= request.POST.get('periodo')) | Q(estado = request.POST.get('estado')) | Q(tipo_evento = request.POST.get('tipo'))  | Q(publico = request.POST.get('publico')) | Q(calendario_evento__aula__codigo_aula=request.POST.get('aulas'))).distinct('codigo_evento')
            for row in rows:
                cant_participantes = Participante.objects.filter(evento__codigo_evento=row.codigo_evento).count()
                design = row.get_design()
                aulas = row.get_aula()
                row_num += 1
                ws.write(row_num,0,row.codigo_evento,font_style)
                ws.write(row_num,1, design.cod_programa, font_style)
                ws.write(row_num,2, row.tipo_evento, font_style)
                ws.write(row_num,3, row.nombre, font_style)
                ws.write(row_num,4, row.promocion, font_style)
                ws.write(row_num,5, str(row.fecha_inicio), font_style)
                ws.write(row_num,6, str(row.fecha_fin), font_style)
                ws.write(row_num,7, str(str(row.horarios())), font_style)
                ws.write(row_num,8, row.estado, font_style)
                ws.write(row_num,9, str(cant_participantes), font_style)
                ws.write(row_num,10, row.centro_costos, font_style)
                ws.write(row_num,11, str(design.horas_totales), font_style)
                ws.write(row_num,12, 'Nombres: {} Apellidos: {}'.format(row.docente.nombres,row.docente.apellidos), font_style)
                ws.write(row_num,13, design.area.area, font_style)
                ws.write(row_num,14, design.tipo_certificado, font_style)
                ws.write(row_num,15, row.modalidad, font_style)
                
                if row.tipo_evento == 'corporativo':
                     ws.write(row_num,16,row.get_empresa(), font_style)
                else:
                    ws.write(row_num,16,'Ninguno', font_style)

                ws.write(row_num,17,aulas.aula.nombre,font_style)
                ws.write(row_num,18,row.asesor_comercial_responsable,font_style)
                ws.write(row_num,19,'Preguntar sobre este campo',font_style)
                ws.write(row_num,20,str(design.fecha),font_style)


    wb.save(response)
    return response


class Registro_asistencia_evento(View):
    def cabecera(self,pdf):
        #Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT+'/image_event/espol.png'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 740, 190, 90,preserveAspectRatio=True)
        #Se dibuja una linea horizontal
        pdf.line(260,740,35,740)
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Times-Roman", 10)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(315, 790, b" REGISTRO DE ASISTENCIA POR EVENTO")
        pdf.drawString(426, 774, u"CÓDIGO EVENTO ")
        pdf.drawString(466, 761, u"########")
        pdf.drawString(35, 720, u"Programa:") ; pdf.drawString(260, 720, u"Duración:")
        pdf.drawString(35, 705, u"Promoción:") ; pdf.drawString(260, 705, u"Fecha Inicio:")
        pdf.drawString(35, 690, u"Curso:") ; pdf.drawString(260, 690, u"Fecha Final:")
        pdf.drawString(35, 675, u"Instructor:") ; pdf.drawString(260, 675, u"Tipo de Capacitación:")
        pdf.drawString(460,665,"CONTROL DE ASISTENCIA")


    def pie_pagina(self,pdf):
        pdf.setFillColor(HexColor(308011))
        pdf.drawString(10, 60, u" /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
        pdf.setFillColor(HexColor(000000))
        page_num = pdf.getPageNumber()
        text = "Pag %s" % page_num
        pdf.drawString(500, 30, text)
        pdf.drawString(35,50 ,u'CEC ESPOL, Campus Gustavo Galindo Velasco | Teléf:042269763 | 0960507588 ')
        now = datetime.now()
        pdf.drawString(35,35, u"Fecha impresión:"+str(now.day)+'/'+str(now.month)+'/'+str(now.year))
        pdf.drawString(260, 35,u'Usuario')

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_LEFT
        styleBH = styles["Normal"]
        styleBH.alignment = TA_CENTER
        hnum = Paragraph('''<b>N.-</b>''', styleBH)
        hcedula = Paragraph('''<b>Cedula</b>''', styleBH)
        hnombre = Paragraph('''<b>Nombre</b>''', styleBH)
        hfirma = Paragraph('''<b>Firma</b>''', styleBH)
        hentrada = Paragraph('''<b>H.Entrada</b>''', styleBH)
        hsalida = Paragraph('''<b>H.Salida</b>''', styleBH)
        #hcargo = Paragraph('''<b>Cargo</b>''', styleBH)
        #harea = Paragraph('''<b>Área</b>''', styleBH)
        #-----conteniedo en la tabla-------

        con= Paragraph('0940659261',styleBH)
        con1= Paragraph('Steven Burgos',styleBH)
        
        encabezados = (hnum,hcedula,hnombre,hfirma,hentrada,hsalida,"","","","","","","","","","")#hprofesion,hcargo,harea)
        encabezados2=("","","","","")
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [('0',con,con1),('1')]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados2,encabezados] + detalles, colWidths=[1 * cm,2.5*cm, 2.5 * cm, 4 * cm, 2.5 * cm,2.5*cm,0.5*cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(2,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 1), (-1, -1), 0.5, colors.black), 
                ('GRID', (6, 0), (-1, -1), 0.5, colors.black),
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (6, 0), (-1, 0), 40),

            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 850, 650)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 20,y-50)
    def get(self, request, ):

            
            #Indicamos el tipo de contenido a devolver, en este caso un pdf
            response = HttpResponse(content_type='application/pdf')
            #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
            buffer = BytesIO()
            #Canvas nos permite hacer el reporte con coordenadas X y Y
            pdf = canvas.Canvas(buffer)
            #Llamo al método donde están definidos los datos que aparecen en el reporte.
            y = 590 
            self.cabecera(pdf)
            self.pie_pagina(pdf)
            self.tabla(pdf,y)
            #Con show page hacemos un corte de página para pasar a la siguiente
            pdf.showPage()
            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response


def  eventos_ejecutados(request):
    template_path = 'reportes/EventosTransparencia.html'
    response = HttpResponse(content_type='application/pdf')
    context = {}
    context['fecha_actual'] = date.today()
    if request.method == 'POST':
       context['evento'] = Evento.objects.filter().select_related('diseno')
       response['Content-Disposition'] = 'attachment; filename="reporte transparencia {}.pdf"'.format(str(date.today()))
    template = get_template(template_path)
    html = template.render(context)
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def detalle_part(request):
    template_path = 'reportes/EventosPorGenero.html'
    response = HttpResponse(content_type='application/pdf')
    total_hombres = 0
    total_mujeres = 0
    total_abierto = ""
    total_corporativo = ""
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    context = {}
    context['fecha_actual'] = date.today()
    if request.method == 'POST':
        response['Content-Disposition'] = 'attachment; filename="Reporte de eventos por género.pdf"'
        evento = Evento.objects.filter()
        cant_abiertos = Evento.objects.filter(publico='Abierto').count()
        cant_corporativos = Evento.objects.filter(publico='Corporativo').count()
        context['total_por_publico'] = "Abierto: {} Corporativo: {}".format(cant_abiertos,cant_corporativos)
        for row in evento:
            total_hombres += Participante.objects.filter(Q(evento=row.codigo_evento) & Q(genero='M')).count()
            total_mujeres += Participante.objects.filter(Q(evento=row.codigo_evento) & Q(genero='F')).count()
        context['total_hombres'] = total_hombres
        context['total_mujeres'] = total_mujeres
        context['evento'] = evento
    template = get_template(template_path)
    html = template.render(context)
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response





def reportes_generales(request):
    contexto = {}
    docentes = Docente.objects.filter()
    evento = Evento.objects.filter(Q(estado='No ejecutado') | Q(estado='convalidado'))
    participantes = Participante.objects.all().select_related()

    return render(request,'reportes/reportes_generales.html',{'evento':evento,'participantes':participantes})
