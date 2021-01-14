from rest_framework import viewsets, filters
from .models import *
from .forms import *
from .serializers import *
from django.db.models import Q
from django.views.generic import ListView,TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render,reverse,get_object_or_404,get_list_or_404, redirect
from django.urls import reverse_lazy
from filters.mixins import FiltersMixin
from bootstrap_modal_forms.generic import BSModalCreateView,BSModalUpdateView,BSModalDeleteView
from django.views.generic import View
#-------import para reportes----
from django.conf import settings
from io import BytesIO
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
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
from rolepermissions.mixins import HasPermissionsMixin
from django.contrib.auth.mixins import LoginRequiredMixin
#----------------------------------
# API
class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer

class TipoEventoViewSet(viewsets.ModelViewSet):
    queryset = TipoEvento.objects.all()
    serializer_class = TipoEventoSerializer

class DesignEventoViewSet(FiltersMixin,viewsets.ModelViewSet):
    queryset = DesignEvento.objects.prefetch_related().all()
    serializer_class = DesignEventoSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'codigo',)
    ordering = ('id',)
    filter_mappings = {
        'id':'id',
        'cod':'codigo',
    }

class ObjetivoEspecificoViewSet(FiltersMixin,viewsets.ModelViewSet):
    queryset = ObjetivoEpecifico.objects.all()
    serializer_class = ObjetivoEspecificoSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'descripcion',)
    ordering = ('id',)
    filter_mappings = {
        'id':'id',
        'desc':'descripcion',
    }

class UnidadViewSet(FiltersMixin,viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'nombre_unidad',)
    ordering = ('id',)
    filter_mappings = {
        'id':'id',
        'nom':'nombre_unidad',
    }

class SubUnidadViewSet(viewsets.ModelViewSet):
    queryset = SubUnidad.objects.all()
    serializer_class = SubUnidadSerializer

class RecursoViewSet(viewsets.ModelViewSet):
    queryset = Recurso.objects.all()
    serializer_class =RecursoSerializer

class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    serializer_class = LecturaSerializer

class ReferenciaViewSet(viewsets.ModelViewSet):
    queryset = Referencia.objects.all()
    serializer_class = ReferenciaSerializer

#Design
class ListarDesign(LoginRequiredMixin, HasPermissionsMixin, ListView):
    # required_permission = 'consultar_academico'
    model=DesignEvento
    template_name="design/listaDiseño.html"

    def get_context_data(self,**kwargs):
        contexto = {}
        contexto['designs'] = DesignEvento.objects.filter()
        contexto['areas'] = Area.objects.all()
        return contexto


class ListarAprobarDesign(ListView):
    model=DesignEvento
    context_object_name =  'designs'
    template_name="design/listaAprobarDiseño.html"


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class CrearDesign(TemplateView):
    template_name='design/crearDiseño.html'
    
    def get_success_url(self):
        return reverse_lazy('listarDesign')

class EditDesign(TemplateView):
    template_name = 'design/editarDiseño.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diseno_id = self.kwargs['diseno_pk']
        diseno = DesignEvento.objects.get(id=diseno_id)
        context['diseno_id'] = diseno_id
        context['newDesign'] = diseno
        
        return context

class ViewDesign(LoginRequiredMixin, TemplateView):

    template_name = 'design/verDiseño.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diseno_id = self.kwargs['diseno_pk']
        diseno = DesignEvento.objects.get(id=diseno_id)
        context['diseno'] = diseno
        recursos = Recurso.objects.filter(design=diseno_id)
        context['recursos'] = recursos
        lecturas = Lectura.objects.filter(design=diseno_id)
        context['lecturas'] = lecturas
        referencias = Referencia.objects.filter(design=diseno_id)
        context['referencias'] = referencias
        if diseno.es_padre:
            hijos = DisenoPadreHijo.objects.filter(padre=diseno_id)
            context['hijos'] = hijos
            if hijos:
                for hijo in hijos:
                    unidades = Unidad.objects.filter(design=hijo.hijo.id)
                    context['unidades'] = unidades
                    subunidades = SubUnidad.objects.filter(design=hijo.hijo.id)
                    context['subunidades'] = subunidades
        else:
            especificos = ObjetivoEpecifico.objects.filter(design=diseno_id)
            context['especificos'] = especificos
            unidades = Unidad.objects.filter(design=diseno_id)
            context['unidades'] = unidades
            subunidades = SubUnidad.objects.filter(design=diseno_id)
            context['subunidades'] = subunidades

        return context

# @login_required
def clonarDesign(request, diseno_id):
    diseno = DesignEvento.objects.get(id=diseno_id)
    ultimo_codigo = DesignEvento.objects.order_by('-id')[0].codigo[-3:]
    codigo_nuevo = str(int(ultimo_codigo)+1)
    if len(codigo_nuevo)==1 :
        codigo_nuevo = "00"+codigo_nuevo
    elif len(codigo_nuevo)==2:
        codigo_nuevo = "0"+codigo_nuevo
    codigo = diseno.codigo[:-3]+str(codigo_nuevo)

    diseno_nuevo = DesignEvento.objects.create(codigo=codigo,nombre=diseno.nombre,version=1,area=diseno.area,especialidad=diseno.especialidad,tipo_evento=diseno.tipo_evento,
        modalidad=diseno.modalidad,tipo_certificado=diseno.tipo_certificado,estado="En proceso",requisitos_facilitador=diseno.requisitos_facilitador,cod_programa=diseno.cod_programa,motivo_rechazo=diseno.motivo_rechazo,
        horas_presenciales=diseno.horas_presenciales,horas_autonomas=diseno.horas_autonomas,horas_totales=diseno.horas_totales,justificacion=diseno.justificacion,
        objetivo=diseno.objetivo,dirigido_participante=diseno.dirigido_participante,indispensable_participante=diseno.indispensable_participante,
        recomendables_participante=diseno.recomendables_participante,metodologia1=diseno.metodologia1,metodologia2=diseno.metodologia2,metodologia3=diseno.metodologia3,
        metodologia4=diseno.metodologia4,metodologia5=diseno.metodologia5,metodologia6=diseno.metodologia6,metodologia7=diseno.metodologia7,metodologia8=diseno.metodologia8)
    
    recursos = Recurso.objects.filter(design=diseno_id)
    for recurso in recursos:
        Recurso.objects.create(tipo=recurso.tipo,descripcion=recurso.descripcion,design=diseno_nuevo)
    
    lecturas = Lectura.objects.filter(design=diseno_id)
    for lectura in lecturas:
        Lectura.objects.create(tipo=lectura.tipo,titulo=lectura.titulo,autor=lectura.autor,sitio_web=lectura.sitio_web,enlace=lectura.enlace,publicacion=lectura.publicacion,editorial=lectura.editorial,pais=lectura.pais,fecha=lectura.fecha,descripcion=lectura.descripcion,design=diseno_nuevo)
    
    referencias = Referencia.objects.filter(design=diseno_id)
    for ref in referencias:
        Referencia.objects.create(tipo=ref.tipo,titulo=ref.titulo,autor=ref.autor,sitio_web=ref.sitio_web,enlace=ref.enlace,publicacion=ref.publicacion,editorial=ref.editorial,pais=ref.pais,fecha=ref.fecha,descripcion=ref.descripcion,design=diseno_nuevo)
    
    if diseno.es_padre:
        hijos = DisenoPadreHijo.objects.filter(padre=diseno_id)
        if hijos:
            for hijo in hijos:
                DisenoPadreHijo.objects.create(padre=diseno_nuevo, hijo=hijo.hijo)
    else:
        diseno_nuevo.es_padre=False
        diseno_nuevo.save()

        especificos = ObjetivoEpecifico.objects.filter(design=diseno_id)
        for esp in especificos:
            ObjetivoEpecifico.objects.create(descripcion=esp.descripcion,design=diseno_nuevo)
        
        unidades = Unidad.objects.filter(design=diseno_id)
        for uni in unidades:
            Unidad.objects.create(numero=uni.numero,nombre_unidad=uni.nombre_unidad,horas_presenciales_unidad=uni.horas_presenciales_unidad,
            horas_autonomas_unidad=uni.horas_autonomas_unidad,horas_totales=uni.horas_totales,objetivo=uni.objetivo,design=diseno_nuevo)
        
        subunidades = SubUnidad.objects.filter(design=diseno_id)
        for sub in subunidades:    
            SubUnidad.objects.create(numero_sub=sub.numero_sub,nombre_sub=sub.nombre_sub,horas_presenciales_sub=sub.horas_presenciales_sub,
            horas_autonomas_sub=sub.horas_autonomas_sub,horas_totales_sub=sub.horas_totales_sub,unidad=sub.unidad,design=diseno_nuevo)

    return redirect('listarDesign')

#Lista General Area/Especialidad

def ListarAreaEspecialidad(request):
    area=Area.objects.all()
    especialidad=Especialidad.objects.all()
    contexto={'areas':area,'especialidades':especialidad}
    return render(request,'area/listarGeneralArea.html',contexto)

#Area
class CrearArea(BSModalCreateView):
    model=Area
    form_class=AreaForm
    template_name='area/crearArea.html'
    # success_message = 'El área se creo con exito'
    success_url = reverse_lazy('listarGeneral')

class UpdateArea(BSModalUpdateView):
    model=Area
    form_class=AreaForm
    template_name='area/crearArea.html'
    # success_message = 'El área se actualizó con exito'
    success_url = reverse_lazy('listarGeneral')

def borrar_area(request, id_area):
    delete_area = Area.objects.get(id=id_area)
    delete_area.delete()
    messages.success(request, 'El área ha sido eliminado')
    return redirect('listarGeneral')

#Especialidad
class CrearEspecialidad(BSModalCreateView):
    model=Especialidad
    form_class=EspecialidadForm
    template_name='especialidades/crearEspecialidad.html'
    # success_message = 'La especicalidad se creo con exito'
    success_url = reverse_lazy('listarGeneral')

class UpdateEspecialidad(BSModalUpdateView):
    model=Especialidad
    form_class=EspecialidadForm
    template_name='especialidades/crearEspecialidad.html'
    # success_message = 'La especicalidad se actualizó con exito'
    success_url = reverse_lazy('listarGeneral')

def borrar_especialidad(request, id_especialidad):
    delete_esp = Especialidad.objects.get(id=id_especialidad)
    delete_esp.delete()
    messages.success(request, 'La especialidad ha sido eliminada')
    return redirect('listarGeneral')
#--------Seccion de Reportes---------------------   



def eventos_ejecutados(request):
    template_path = 'reportes/eventos_ejecutados.html'
    context = {}
    total_aprobacion = 0
    total_participacion = 0
    total_horas = 0
    total_horas_presencial = 0
    total_horas_semi_presencial = 0
    total_horas_virtual = 0


    design = DesignEvento.objects.all().order_by('fecha')
    if request.method == 'POST':
        total_horas = request.POST.get('horas')
        if not total_horas:
            total_horas = 0

        context['fecha'] = date.today()
        if not request.POST.get('modalidades') and not request.POST.get('tipo') and not request.POST.get('horas') and not request.POST.get('estado') and not request.POST.get('tipoEvento') and not request.POST.get('areas'):  
            total_aprobacion = design.filter(tipo_certificado='Aprobación').count()
            total_participacion = design.filter(tipo_certificado='Participación').count()
            context['design'] = design
            #print('todos')
        else:
            design = design.filter(Q(tipo_certificado=request.POST.get('tipoCertificado'))|Q(tipo_evento=str(request.POST.get('tipo')))|Q(area__id=request.POST.get('areas')) | Q(horas_totales=int(total_horas)) | Q(estado=request.POST.get('estado'))| Q(modalidad=request.POST.get('modalidades'))).order_by('fecha')
            total_aprobacion = design.filter(tipo_certificado='Aprobación').count()
            total_participacion = design.filter(tipo_certificado='Participación').count()
            context['design'] =design
            
        for d in design:
            if d.modalidad == 'Presencial':
               total_horas_presencial = total_horas_presencial + d.horas_totales
            if d.modalidad == 'Semi-Presencial':
               total_horas_semi_presencial = total_horas_semi_presencial + d.horas_totales
            if d.modalidad == 'Virtual':
               total_horas_virtual = total_horas_virtual + d.horas_totales

    modalidad_por_hora = [
                          total_horas_presencial,
                          total_horas_semi_presencial,
                          total_horas_virtual
                         ]

    tipo_cursos = [
                   design.filter(tipo_evento='Diplomado').count(),
                   design.filter(tipo_evento='Programa').count(),
                   design.filter(tipo_evento='Curso').count(),
                   design.filter(tipo_evento='Taller').count(),
                   design.filter(tipo_evento='Conferencia').count(),
                   design.filter(tipo_evento='Seminario').count(),
                   design.filter(tipo_evento='Webinario').count(),
                   design.filter(tipo_evento='Charla').count(),
                   design.filter(tipo_evento='Modulo').count() 
                  ]

    tipo_certificado_total = [
                              total_aprobacion,
                              total_participacion
                             ]             

    context['cantidad_designs'] = design.count()
    context['modalidad_por_hora'] = modalidad_por_hora
    context['lista_tipo_evento'] = tipo_cursos 
    context['tipo_certificado_total'] = tipo_certificado_total

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Eventos ejecutados por diseño {}.pdf"'.format(date.today())
    template = get_template(template_path)
    html = template.render(context)
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


