from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
#from django.core import serializers
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from django.views.generic import CreateView, UpdateView, DeleteView
from datetime import date
from django.template.loader import render_to_string
from .models import *
from .forms import PresupuestoEventoForm, PresupuestoEventoFormUpdate
from . import forms
from dal import autocomplete
from .filters import PresupuestoEventoFilter
from django.db.models import Max


def index_presupuestos(request):
    if (request.GET.get('estado', None) != None and 'Anulada' in request.GET['estado']):
        presupuestos_list = PresupuestoEvento.objects.all().order_by("-codigo","-version")
    else:
        presupuestos_list = PresupuestoEvento.objects.all().exclude(
            estado='Anulada').order_by("-codigo","-version")
    filter = PresupuestoEventoFilter(
        request.GET, queryset=presupuestos_list)
    return render(request, 'presupuestos/index.html', {"filter": filter})


class PresupuestoEventoCreate(CreateView):
    model = PresupuestoEvento
    form_class = PresupuestoEventoForm
    template_name = 'presupuestos/forma.html'
    success_url = reverse_lazy('index_presupuestos')

    def get_context_data(self, **kwargs):
        context = super(PresupuestoEventoCreate,
                        self).get_context_data(**kwargs)
        context['costo_horas'] = [0]
        context['impuesto_select'] = [0]
        context['impuesto_total'] = [0]
        context['honorario_instructores'] = [0]
        context['horas_instructores'] = [0]
        context['impuesto_porcentaje'] = [0]
        context['valor_total'] = [0]
        return context

    def form_valid(self, form):
        try:
            #pre_v=int(self.model.objects.get('pk').pk+1)
            p = self.model.objects.get(ultimo=True)
            p.ultimo=False
            p.save()
            pre_v =int(p.last_id)+1
            pre = str(pre_v)
            sec = '0'*(4-len(pre))+pre
        except self.model.DoesNotExist:
            sec = '0001'
            pre_v=1
        form.instance.codigo = sec+'-'+str(date.today().year)
        form.instance.last_id=pre_v
        return super().form_valid(form)


class PresupuestoEventoUpdate(UpdateView):
    model = PresupuestoEvento
    form_class = PresupuestoEventoForm
    second_form_class = PresupuestoEventoFormUpdate
    template_name = 'presupuestos/editar.html'
    success_url = reverse_lazy('index_presupuestos')

    def get_context_data(self, **kwargs):
        context = super(PresupuestoEventoUpdate,
                        self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        presupuesto = self.model.objects.get(pk=pk)
        if self.request.POST:
            if presupuesto.estado == "Grabado":
                context['form'] = self.form_class(self.request.POST,instance=presupuesto)
            else:
                context['form'] = self.second_form_class(self.request.POST,instance=presupuesto)
        else:
            if presupuesto.estado == "Grabado":
                context['form'] = self.form_class(instance=presupuesto)
            else:
                context['form'] = self.second_form_class(instance=presupuesto)
        context['costo_horas'] = [float(i) for i in str(
            presupuesto.costo_hora_instructores).split(',')[:-1]]
        context['impuesto_select'] = [int(i) for i in str(
            presupuesto.impuesto_select).split(',')[:-1]]
        context['impuesto_total'] = [float(i) for i in str(
            presupuesto.impuesto_total).split(',')[:-1]]
        context['honorario_instructores'] = [float(i) for i in str(
            presupuesto.honorario_instructores).split(',')[:-1]]
        context['horas_instructores'] = [int(i) for i in str(
            presupuesto.horas_instructores).split(',')[:-1]]
        context['valor_total'] = [float(i) for i in str(
            presupuesto.valor_total).split(',')[:-1]]
        context['impuesto_porcentaje'] = [int(i) for i in str(
            presupuesto.impuesto_porcentaje).split(',')[:-1]]
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        form=self.form_class(request.POST)
        pk=self.kwargs.get('pk',0)
        
        if form.is_valid():
            prop= self.model.objects.get(pk=pk)
            if prop.version!=form.instance.version:
                prop.active=False
                prop.ultimo=False
                prop.save()
                p=form.save(commit=False)
                p.active=True
                p.estado="Grabado"
                p.fecha_envio=None
                p.fecha_aprobada_sin=None
                p.fecha_aprobada_con=None
                p.save()
            else :
                formr = self.form_class(request.POST or None, instance=prop)
                formr.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class PresupuestoEventoDelete(DeleteView):
    model = PresupuestoEvento
    template_name = 'presupuestos/eliminar.html'
    success_url = reverse_lazy('index_presupuestos')
    form_class = PresupuestoEventoForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = "Anulada"
        motivo = dict(request.POST).get("motivo_anular")[0]
        fanulado = dict(request.POST).get("fecha_anulado")[0]
        self.object.motivo_anular = motivo
        self.object.fecha_anulado = fanulado
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def presupuesto_conf_elim(request):
    presupuesto_id = request.GET.get('pk')
    presupuesto = PresupuestoEvento.objects.get(id=presupuesto_id)
    form = PresupuestoEventoForm(instance=presupuesto)
    return render(request, "presupuestos/eliminar.html", {"presupuesto": presupuesto, "form": form})


class PresupuestoEventoAprobar(UpdateView):
    model = PresupuestoEvento
    form_class = PresupuestoEventoForm
    template_name = 'presupuestos/aprobar.html'
    success_url = reverse_lazy('pendiente_aprobacion')

    def get_context_data(self, **kwargs):
        context = super(PresupuestoEventoAprobar,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        presupuesto = self.model.objects.get(pk=pk)
        cod = presupuesto.codigo
        tmp = self.model.objects.filter(codigo = cod)
        max_version_enviada = tmp.filter(estado="Solicitud Enviada").aggregate(Max('version'))
        version_aprobada = tmp.filter(Q(estado="Autorizada sin evento")|Q(estado="Autorizada con evento")).order_by("-fecha_aprobada_sin").first()
        context['version_enviada'] = max_version_enviada
        context['version_aprobada'] = version_aprobada
        context['costo_horas'] = [float(i) for i in str(
            presupuesto.costo_hora_instructores).split(',')[:-1]]
        context['impuesto_select'] = [int(i) for i in str(
            presupuesto.impuesto_select).split(',')[:-1]]
        context['impuesto_total'] = [float(i) for i in str(
            presupuesto.impuesto_total).split(',')[:-1]]
        context['honorario_instructores'] = [float(i) for i in str(
            presupuesto.honorario_instructores).split(',')[:-1]]
        context['horas_instructores'] = [int(i) for i in str(
            presupuesto.horas_instructores).split(',')[:-1]]
        context['valor_total'] = [float(i) for i in str(
            presupuesto.valor_total).split(',')[:-1]]
        context['impuesto_porcentaje'] = [int(i) for i in str(
            presupuesto.impuesto_porcentaje).split(',')[:-1]]
        context['p_id'] = presupuesto.pk
        return context


def anular_presupuesto(request, pk):
    if(request.method == 'POST'):
        p = get_object_or_404(PresupuestoEvento, pk=pk)
        p.estado = "Anulada"
        motivo = dict(request.POST).get("motivo_anular")[0]
        p.motivo_anular = motivo
        p.save()
        return redirect('pendiente_aprobacion')


def cargar_info(request):
    modelo = request.GET.get('modelo')
    id = request.GET.get('id')
    if id == "100" or id=="":
        valor = 0
        return JsonResponse({'costo': valor})
    if modelo == "pasaje_instructor" or modelo == "pasaje_personal":
        valor = TarifarioServicioAereo.objects.get(pk=id).costo
    elif modelo == "hospedaje_alimentacion_instructor" or modelo == "hospedaje_alimentacion_personal":
        valor = TarifarioHospedajeAlimentacionDocente.objects.get(pk=id).costo
    elif modelo == "break_instructor" or modelo == 'break_evento':
        valor = TarifarioServicioAlimentacionBreak.objects.get(pk=id).costo
    elif modelo == "almuerzo_instructor" or modelo == "almuerzo_evento":
        valor = TarifarioServicioAlimentacionAlmuerzo.objects.get(pk=id).costo
    elif modelo == "instalaciones":
        valor = TarifarioInstalacion.objects.get(pk=id).costo
    elif modelo == "publicidad":
        valor = TarifarioPublicidad.objects.get(pk=id).costo
    elif modelo == "personal_evento":
        valor = TarifarioPlantillaDelPersonal.objects.get(pk=id).costo
    elif modelo == "prospecto_evento":
        valor = TarifarioProspecto.objects.get(pk=id).costo
    elif modelo in ['carpeta', 'certificados', 'maletin', 'block', 'pluma', 'lapiz', 'cd', 'aportacion_facultad', 'credencial_plastico', 'credencial_pvc', 'pendrive', 'otros_materiales', 'impuesto', 'ceremonia']:
        valor = TarifarioMaterial.objects.get(pk=id).costo_con_iva
    elif modelo == "centro_costo":
        objeto = Centro_Costos.objects.get(pk=id)
        valor = {'espol': objeto.espol, 'espoltech': objeto.espoltech,
                 'ministerio': objeto.ministerio, 'fundaespol': objeto.fundaespol}
    elif modelo == 'cafeteria_limpieza':
        valor = TarifarioOtroSuministro.objects.get(pk=id).costo
    else:
        valor = 0
    return JsonResponse({'costo': valor})



def load_eventos(request):
    #tipo_evento = request.GET.get('tipo')
    eventos = Evento.objects.filter(presupuestoevento__evento__isnull=True).distinct()#.filter(publico=tipo_evento).distinct()
    codigos = render_to_string("presupuestos/dropdown_evento_codigo.html", {"eventos": eventos})
    nombres = render_to_string("presupuestos/dropdown_evento_nombre.html", {"eventos": eventos})
    return JsonResponse({'codigo': codigos, 'nombre': nombres})

def load_all_eventos(request):
    #tipo_evento = request.GET.get('tipo')
    #eventos = Evento.objects.filter(publico=tipo_evento)
    eventos = Evento.objects.all()
    codigos = render_to_string("presupuestos/dropdown_evento_codigo.html", {"eventos": eventos})
    nombres = render_to_string("presupuestos/dropdown_evento_nombre.html", {"eventos": eventos})
    return JsonResponse({'codigo': codigos, 'nombre': nombres})