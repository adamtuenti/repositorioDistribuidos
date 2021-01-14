from django.shortcuts import render, redirect, get_object_or_404
from financiero.plan_anual_compras.models import PlanAnualCompras, Partida, Producto
from financiero.orden_pago.models import Egresos
from .forms import PlanAnualComprasForm, PartidaForm, PlanAnualComprasUpdateForm
from .filters import PlanAnualComprasFilter
from datetime import date
from django.http import HttpResponseRedirect,JsonResponse
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from dal import autocomplete
from django.template.loader import render_to_string
# Create your views here.

def index(request):
    if (request.GET.get('estado', None) != None and 'Anulada' in request.GET['estado']):
        pac_lista = PlanAnualCompras.objects.all().order_by("-id")
    else:
        pac_lista = PlanAnualCompras.objects.all().exclude(estado='Anulada').order_by("-id")
    pac_filter = PlanAnualComprasFilter(request.GET, queryset=pac_lista)
    return render(request, "plan_anual_compras/pac_list.html", {"pac_lista":pac_lista, "filter":pac_filter})


class PACCreate(CreateView):
    model = PlanAnualCompras
    template_name = 'plan_anual_compras/pac_nuevo.html'
    form_class = PlanAnualComprasForm
    partida_form_class=PartidaForm
    success_url = '/financiero/plan_anual_compras/editar'
    def get_context_data(self,**kwargs):
        context=super(PACCreate,self).get_context_data(**kwargs)
        formset=self.partida_form_class()
        if('formset' not in context):
            context['formset']=formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form_Partida =self.partida_form_class(request.POST)
        if form.is_valid() and form_Partida.is_valid():
            pac=form.save(commit=False)
            partida=form_Partida.save(commit=False)
            if(pac.nombre==''):
                pac.nombre = 'Plan Anual de Compras - '+str(pac.año)
            pac.save()

            partida.pac = pac
            partida.save()
            return HttpResponseRedirect(self.get_success_url()+'/'+str(pac.pk))
        else:
            return self.render_to_response(self.get_context_data(form=form,formset=form_Partida))


class PACUpdate(UpdateView):
    model = PlanAnualCompras
    second_model = Partida
    template_name = 'plan_anual_compras/pac_editar.html'
    form_class = PlanAnualComprasForm
    update_form_class = PlanAnualComprasUpdateForm
    partida_form_class=PartidaForm
    success_url = reverse_lazy('pac_index')

    def get_context_data(self, **kwargs):
        context = super(PACUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        pac = self.model.objects.get(pk=pk)
        partidas = self.second_model.objects.filter(pac_id=pk)

        if 'form' in context:
            if pac.estado == "Grabado":
                context['form'] = self.form_class(instance=pac)
            else:
                context['form'] = self.update_form_class(instance=pac)
        context['partidas'] = partidas
        context['pac_id'] = pk
        return context



class PACDelete(DeleteView):
    model = PlanAnualCompras
    template_name = 'plan_anual_compras/pac_eliminar.html'
    success_url = reverse_lazy('pac_index')
    form_class = PlanAnualComprasForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = "Anulada"
        motivo = dict(request.POST).get("motivo_anular")[0]
        fanulado = dict(request.POST).get("fecha_anulado")[0]
        self.object.motivo_anular = motivo
        self.object.fecha_anulado = fanulado
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PACAprobar(UpdateView):
    model = PlanAnualCompras
    second_model=Partida
    form_class = PlanAnualComprasForm
    template_name = 'plan_anual_compras/pac_aprobar.html'
    success_url = reverse_lazy('pendiente_aprobacion')

    def get_context_data(self, **kwargs):
        context = super(PACAprobar,self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        pac = self.model.objects.get(pk=pk)
        if 'form' not in context:
            context['form'] = self.form_class(instance=pac)
        partidas = self.second_model.objects.filter(pac_id=pk)
        context['partidas'] = partidas
        context['pac_id'] = pk
        return context

def pac_conf_elim(request):
    pac_id = request.GET.get('pk')
    pac = PlanAnualCompras.objects.get(id=pac_id)
    form = PlanAnualComprasUpdateForm(instance=pac)
    return render(request, "plan_anual_compras/pac_eliminar.html", {"object": pac, "form": form})

def partida_update(request):
    p_id=request.GET.get('pk')
    pac_id = request.GET.get('fk')
    try:
        partida = Partida.objects.get(id=p_id)
        form = PartidaForm(instance=partida)
    except Partida.DoesNotExist:
        form = PartidaForm()
    return render(request, "plan_anual_compras/partida_editar.html", {"form": form,"pk":p_id,"fk":pac_id})

    
def partida_eliminar(request):
    p_id=request.GET.get('pk')
    pac_id = request.GET.get('fk')
    producto = Partida.objects.get(pk=p_id)
    return render(request, "plan_anual_compras/partida_eliminar.html", {"form": producto,"pk":p_id,"fk":pac_id})


def partida_aprobar_update(request):
    p_id=request.GET.get('pk')
    pac_id = request.GET.get('fk')
    try:
        partida = Partida.objects.get(id=p_id)
        form = PartidaForm(instance=partida)
    except Partida.DoesNotExist:
        form = PartidaForm()
    return render(request, "plan_anual_compras/partida_aprobar_editar.html", {"form": form,"pk":p_id,"fk":pac_id})

    
def partida_aprobar_eliminar(request):
    p_id=request.GET.get('pk')
    pac_id = request.GET.get('fk')
    producto = Partida.objects.get(pk=p_id)
    return render(request, "plan_anual_compras/partida_aprobar_eliminar.html", {"form": producto,"pk":p_id,"fk":pac_id})

class PartidaUpdate(UpdateView):
    model = Partida
    form_class = PartidaForm
    template_name = 'plan_anual_compras/partida_nuevo.html'
    success_url = '/financiero/plan_anual_compras/editar'

    def get_context_data(self, **kwargs):
        context = super(PartidaUpdate,self).get_context_data(**kwargs)
        fk=self.kwargs.get('fk',0)
        context['pac_id']=fk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pac_id = kwargs['fk']
        pk = kwargs['pk']
        try:
            partida = self.model.objects.get(id=pk)
            form = self.form_class(request.POST, instance=partida)
        except self.model.DoesNotExist:
            form = self.form_class(request.POST)
        if form.is_valid():
            p=form.save(commit=False)
            p.pac_id = pac_id
            p.save()
        return HttpResponseRedirect(self.get_success_url()+'/'+str(pac_id))


class PartidaDelete(DeleteView):
    model = Partida
    form_class = PartidaForm
    template_name = 'plan_anual_compras/partida_eliminar.html'
    success_url = '/financiero/plan_anual_compras/editar'

    def post(self, request, *args, **kwargs):
        pac_id = kwargs['fk']
        self.object=self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url()+'/'+str(pac_id))

class PartidaAprobarUpdate(UpdateView):
    model = Partida
    form_class = PartidaForm
    template_name = 'plan_anual_compras/partida_nuevo.html'
    success_url = '/financiero/plan_anual_compras/aprobar'

    def get_context_data(self, **kwargs):
        context = super(PartidaUpdate,self).get_context_data(**kwargs)
        fk=self.kwargs.get('fk',0)
        context['pac_id']=fk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pac_id = kwargs['fk']
        pk = kwargs['pk']
        try:
            partida = self.model.objects.get(id=pk)
            form = self.form_class(request.POST, instance=partida)
        except self.model.DoesNotExist:
            form = self.form_class(request.POST)
        if form.is_valid():
            p=form.save(commit=False)
            p.pac_id = pac_id
            p.save()
        return HttpResponseRedirect(self.get_success_url()+'/'+str(pac_id))


class PartidaAprobarDelete(DeleteView):
    model = Partida
    form_class = PartidaForm
    template_name = 'plan_anual_compras/partida_eliminar.html'
    success_url = '/financiero/plan_anual_compras/aprobar'

    def post(self, request, *args, **kwargs):
        pac_id = kwargs['fk']
        self.object=self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url()+'/'+str(pac_id))


def load_partida(request):
    #tipo = request.GET.get('tipo') DADO QUE NO IMPORTA CUAL CENTRO ES Y EN LA BASE SOLO SE CUENTA CON ESPOLTECH, SIEMPRE SE USARÁ EL 1.
    # DESCONMENTAR LA LINEA PREVIA SOLO SI YA SE CUENTA CON VALORES PARA OTRO CENTRO DE COSTO EN LA bASE Y COMENTAR LA LINEA INFERIOR
    tipo=1
    partidas = Egresos.objects.filter(centroc=tipo)
    codigo = render_to_string("plan_anual_compras/dropdown_codigo.html", {"partidas": partidas})
    partida = render_to_string("plan_anual_compras/dropdown_partida.html", {"partidas": partidas})
    return JsonResponse({'codigo': codigo, 'partida': partida})


def load_producto(request):
    productos = Producto.objects.all()
    productos_opts = render_to_string("plan_anual_compras/dropdown_producto.html", {"productos": productos})
    return JsonResponse({'producto': productos_opts})