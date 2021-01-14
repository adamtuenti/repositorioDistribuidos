from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from .models import *
from administrativo.productos.models import *
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core.files import File
from django.db import transaction
from administrativo.productos.models import *
from . import forms
#Forms
from .forms import *


from dal import autocomplete

#Itertools
from itertools import chain

from django.core.paginator import Paginator



# Create your views here.

def index_suministros(request):
	suministros_list = Suministro.objects.all().order_by("pk")
	filter = SuministroFilter(request.GET, queryset=suministros_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	suministros = paginator.get_page(page)
	return render(request, 'index_suministros.html', {'suministros': suministros, "filter":filter})


class suministros_view(CreateView):
    model= Suministro
    form_class= SuministroForm
    template_name='form_suministros.html'
    success_url=reverse_lazy('index_suministros')
    
    def get_context_data(self, **kwargs):
        data = super(suministros_view, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = SuministroProductoFormset(self.request.POST, self.request.FILES)
        else:
            data['formset'] = SuministroProductoFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        productos = context['formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            try:
                pre = str(int(self.model.objects.latest('pk').pk+1))
                sec = '0'*(4-len(pre))+pre
            except self.model.DoesNotExist:
                sec = '0001'
            form.instance.cod_suministro = sec
            self.object = form.save()
            if productos.is_valid():
                productos.instance = self.object
                productos.save()
                nel=[]
                for obj in productos.deleted_forms:
                        nel.append(obj.instance.producto)
                for p in productos :
                    if p.instance.producto!=None and p.instance.producto not in nel:
                        prod=Producto.objects.get(pk=p.instance.producto.id)
                        prod.stock_actual=prod.stock_actual+p.instance.cantidad
                        prod.save()
        return super(suministros_view, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index_suministros')

	# def post(self, request, *args, **kwargs):
	# 	self.object =self.get_object
	# 	form=self.form_class(request.POST)
	# 	if form.is_valid():
	# 		try:
	# 			fechaS=form.cleaned_data.get("fecha_seguimiento")
	# 			pre = str(int(self.model.objects.latest('pk').pk+1))
	# 			sec = '0'*(4-len(pre))+pre
	# 		except self.model.DoesNotExist:
	# 			sec = '0001'
	# 		form.instance.cod_suministro = sec
	# 		Suministro=form.save()
	# 		return redirect('index_suministros')
	# 	else:
	# 		return self.render_to_response(self.get_context_data(Suministro=Suministro))

class suministrosUpdateView(UpdateView):
    model= Suministro
    form_class= SuministroForm
    template_name='edicion_form_suministros.html'
    success_url=reverse_lazy('index_suministros')
    
    def get_context_data(self, **kwargs):
        data = super(suministrosUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = SuministroProductoFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['formset'] = SuministroProductoFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        productos = context['formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if productos.is_valid():
                productos.instance = self.object
                nel=[]
                for obj in productos.deleted_forms:
                        nel.append(obj.instance.producto)
                for p in productos :
                    if p.instance.producto!=None:
                        if p.instance.producto not in nel:
                            try:
                                ps=ProductoSuministro.objects.get(suministro__cod_suministro=form.instance.cod_suministro,producto=p.instance.producto)
                                prod=Producto.objects.get(pk=p.instance.producto.id)
                                prod.stock_actual=prod.stock_actual+p.instance.cantidad-ps.cantidad
                                prod.save()
                            except ProductoSuministro.DoesNotExist:
                                prod=Producto.objects.get(pk=p.instance.producto.id)
                                prod.stock_actual=prod.stock_actual+p.instance.cantidad
                                prod.save()
                        else :
                            try:
                                ps=ProductoSuministro.objects.get(suministro__cod_suministro=form.instance.cod_suministro,producto=p.instance.producto)
                                prod=Producto.objects.get(pk=p.instance.producto.id)
                                prod.stock_actual=prod.stock_actual-ps.cantidad
                                prod.save()
                            except ProductoSuministro.DoesNotExist:
                                print("no existe")
                productos.save()
        return super(suministrosUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index_suministros')

def load_personas(request):
    proveedor = request.GET.get("proveedor")
    identificacion=[]
    razon_nombre=[]
    proveedores=Proveedor.objects.all()
    print(proveedores)
    identificacion=render_to_string("dropdown_proveedor_rucOF.html",{"proveedores":proveedores})
    razon_nombre=render_to_string("dropdown_proveedor_razonOF.html",{"proveedores":proveedores})
    return JsonResponse({'ruc_ci': identificacion, 'razon_nombre': razon_nombre})

def load_productos(request):
    producto=[]
    productos=Producto.objects.filter(estado="Activo")
    print(productos)
    producto=render_to_string("dropdown_productos.html",{"productos":productos})
    return JsonResponse({'producto': producto,})

def load_producto_detalles(request):
    id = request.GET.get("id")
    idF = request.GET.get("idF")
    producto=Producto.objects.get(pk=id)
    return JsonResponse({'unidad': producto.unidad_medida,'iva':producto.iva,"estado":producto.estado,"controlable":producto.controlable,"stock":producto.stock_actual,"punto_reorden":producto.punto_reorden,"idF":idF})
	