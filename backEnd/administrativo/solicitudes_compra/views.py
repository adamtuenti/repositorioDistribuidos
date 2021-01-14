from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from .models import *
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core.files import File
from django.db import transaction
from . import forms
from .forms import *
from dal import autocomplete
from itertools import chain
from django.core.paginator import Paginator


def solicitudes_compra(request):	
	solicitudes_list = SolicitudCompra.objects.all().order_by("pk")
	filter = ComprasFilter(request.GET, queryset=solicitudes_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	solicitudes = paginator.get_page(page)
	return render(request, 'solicitudes_compra.html', {'solicitudes': solicitudes, "filter":filter})	



class nueva_compra(CreateView):
	model = SolicitudCompra
	form_class = ComprasForm
	template_name = 'nueva_compra.html'
	success_url = reverse_lazy('solicitudes_compra')

	def get_context_data(self, **kwargs):
		data = super(nueva_compra, self).get_context_data(**kwargs)
		if self.request.POST:
			data['formset'] = SolicitudProductoFormset(self.request.POST, self.request.FILES)
		else:
			data['formset'] = SolicitudProductoFormset()
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
			form.instance.cod_solicitud = sec
			self.object = form.save()
			if productos.is_valid():
				print("es valido")
				productos.instance = self.object
				productos.save()
				nel=[]
				for obj in productos.deleted_forms:
						nel.append(obj.instance.producto)
				for p in productos :
					print("producto")
					print (p)
					if p.instance.producto!=None and p.instance.producto not in nel:
						prod=Producto.objects.get(pk=p.instance.producto.id)
						#prod.stock_actual=prod.stock_actual+p.instance.cantidad
						#prod.save()
		
		return super(nueva_compra, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('solicitudes_compra')



class solicitud_editar(UpdateView):
	model = SolicitudCompra
	form_class = ComprasUpdateForm
	template_name = 'solicitud_editar.html'
	success_url = reverse_lazy('solicitudes_compra')

	def get_context_data(self, **kwargs):
		data = super(solicitud_editar, self).get_context_data(**kwargs)
		if self.request.POST:
			data['formset'] = SolicitudProductoFormset(self.request.POST, self.request.FILES, instance=self.object)
		else:
			data['formset'] = SolicitudProductoFormset(instance=self.object)
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
								ps=ProductoSolicitud.objects.get(solicitudcompra__cod_solicitud=form.instance.cod_solicitud,producto=p.instance.producto)
								prod=Producto.objects.get(pk=p.instance.producto.id)
								# prod.stock_actual=prod.stock_actual+p.instance.cantidad-ps.cantidad
								# prod.save()
							except ProductoSolicitud.DoesNotExist:
								prod=Producto.objects.get(pk=p.instance.producto.id)
								# prod.stock_actual=prod.stock_actual+p.instance.cantidad
								# prod.save()
						else :
							try:
								ps=ProductoSolicitud.objects.get(solicitudcompra__cod_solicitud=form.instance.cod_solicitud,producto=p.instance.producto)
								prod=Producto.objects.get(pk=p.instance.producto.id)
								# prod.stock_actual=prod.stock_actual-ps.cantidad
								# prod.save()
							except ProductoSolicitud.DoesNotExist:
								print("no existe")
				productos.save()
		return super(solicitud_editar, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('solicitudes_compra')