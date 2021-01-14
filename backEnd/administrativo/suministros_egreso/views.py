from .forms import Suministro_EgresoForm, FileForm, FileFormset, Suministro_EgresoFilter
from .models import Suministro_Egreso, Suministro_EgresoFile
from django.urls import reverse_lazy
from django.db import transaction
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from .models import *
from .models import Suministro_Egreso
from django.core.exceptions import ValidationError
from django.core.files import File
from . import forms
#Forms
from .forms import *


from dal import autocomplete

#Itertools
from itertools import chain

from django.core.paginator import Paginator

def index_suministros_egreso(request):
	suministros_egreso_list = Suministro_Egreso.objects.all().order_by("pk")
	filter = Suministro_EgresoFilter(request.GET, queryset=suministros_egreso_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	suministros_egreso = paginator.get_page(page)
	return render(request, 'index_suministros_egreso.html', {'suministros_egreso': suministros_egreso, "filter":filter})



class suministros_egreso_view(CreateView):
    model=Suministro_Egreso
    form_class=Suministro_EgresoForm
    form_class2=FileForm
    template_name='form_suministros_egreso.html'
    success_url=reverse_lazy('index_suministros_egreso')

    def get_context_data(self, **kwargs):
        data = super(suministros_egreso_view, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = FileFormset(self.request.POST,self.request.FILES)
            data['sumepro'] = SuministroEgresoProductoFormset(self.request.POST, self.request.FILES)
        else:
            data['formset'] =FileFormset()
            data['sumepro'] = SuministroEgresoProductoFormset()
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        productos = context['sumepro']
        titles= context['formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            try:
                pre = str(int(self.model.objects.latest('pk').pk+1))
                sec = '0'*(4-len(pre))+pre
            except self.model.DoesNotExist:
                sec = '0001'
            form.instance.cod_suministro_egreso = sec
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
            print(productos)
            print("si fue valido")
            productos.instance = self.object
            productos.save()
            nel=[]
            for obj in productos.deleted_forms:
                    nel.append(obj.instance.producto)
            for p in productos :
                if p.is_valid():
                    if p.instance.producto!=None and p.instance.producto not in nel:
                        prod=Producto.objects.get(pk=p.instance.producto.id)
                        prod.stock_actual=prod.stock_actual-p.instance.cantidad_despachada
                        prod.save()
        return super(suministros_egreso_view, self).form_valid(form)

    def get_success_url(self):
        return self.success_url


class suministrosEgresoUpdateView(UpdateView):
    model= Suministro_Egreso
    form_class= Suministro_EgresoForm
    template_name='edicion_form_suministros_egreso.html'
    success_url=reverse_lazy('index_suministros_egreso')
    
    def get_context_data(self, **kwargs):
        data = super(suministrosEgresoUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] =FileFormset(self.request.POST, self.request.FILES,instance=self.object)
            data['sumepro'] = SuministroEgresoProductoFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['formset'] =FileFormset(instance=self.object)
            data['sumepro'] = SuministroEgresoProductoFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        productos = context['sumepro']
        titles= context['formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
            if productos.is_valid():
                productos.instance = self.object
                nel=[]
                for obj in productos.deleted_forms:
                        nel.append(obj.instance.producto)
                for p in productos :
                    if p.instance.producto!=None:
                        if p.instance.producto not in nel:
                            try:
                                ps=ProductoSuministroEgreso.objects.get(suministro__cod_suministro_egreso=form.instance.cod_suministro_egreso,producto=p.instance.producto)
                                prod=Producto.objects.get(pk=p.instance.producto.id)
                                prod.stock_actual=prod.stock_actual-p.instance.cantidad_solicitada+ps.cantidad_solicitada
                                prod.save()
                            except ProductoSuministroEgreso.DoesNotExist:
                                prod=Producto.objects.get(pk=p.instance.producto.id)
                                prod.stock_actual=prod.stock_actual-p.instance.cantidad_solicitada
                                prod.save()
                        else :
                            try:
                                ps=ProductoSuministroEgreso.objects.get(suministro__cod_suministro_egreso=form.instance.cod_suministro_egreso,producto=p.instance.producto)
                                prod=Producto.objects.get(pk=p.instance.producto.id)
                                prod.stock_actual=prod.stock_actual+ps.cantidad_solicitada
                                prod.save()
                            except ProductoSuministroEgreso.DoesNotExist:
                                print("no existe")
                productos.save()
        return super(suministrosEgresoUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index_suministros_egreso')


def load_eventos(request):
    participantes= OrdenFacturacionParticipante.objects.all().distinct("cod_evento")
    listae=[]
    for p in participantes:
        listae.append(p.cod_evento)
    eventos=Evento.objects.filter(codigo_evento__in=listae)
    print(eventos)
    eventoslist=render_to_string("dropdown_evento.html",{"eventos":eventos})  
    return JsonResponse({'eventos': eventoslist})