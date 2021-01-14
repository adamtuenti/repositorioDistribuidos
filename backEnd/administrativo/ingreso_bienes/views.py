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
from . import forms
from .forms import *
from dal import autocomplete
from itertools import chain
from django.core.paginator import Paginator

# Create your views here.

class registro_bien(CreateView):
	model = Ingreso_Bien
	form_class = RegistroForm
	template_name ='registro_bien.html'
	success_url = reverse_lazy('consulta_bien')

'''def registro_bien(request):
	registro_list=Bien.objects.all().order_by("pk")
	filter = BienFilter(request.GET, queryset=registro_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	registros = paginator.get_page(page)
	return render(request, 'registro_bien.html', {'registros': registros, "filter":filter})'''


def consulta_bien(request):
	bien_list = Bien.objects.all().order_by("pk")
	filter = BienFilter(request.GET, queryset=bien_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	consultas = paginator.get_page(page)
	return render(request, 'consulta_bien.html', {'consultas': consultas, "filter":filter})

	
class nuevo_bien(CreateView):
	model= Bien
	form_class= BienForm
	template_name='nuevo_bien.html'
	success_url=reverse_lazy('consulta_bien')
	
	def post(self, request, *args, **kwargs):
		self.object =self.get_object
		form=self.form_class(request.POST)
		if form.is_valid():
			try:
				pre = str(int(self.model.objects.latest('pk').pk+1))
				sec = '0'*(4-len(pre))+pre
			except self.model.DoesNotExist:
				sec = '0001'
			form.instance.cod_activo = sec
			# +'-'+str(date.today().year)
			activo=form.save()
			return redirect('consulta_bien')
		else:
			return self.render_to_response(self.get_context_data(form=form))

def load_bien(request):
	tipo=request.GET.get('tipo_Bien')
	bienes = Bien.objects.filter(tipo_bien=tipo)
	cod_bien = render_to_string("dropdown_cod_bien.html", {"bienes":bienes})
	cod_Inventariound = render_to_string("dropdown_cod_inv.html", {"bienes":bienes})
	nombre = render_to_string("dropdown_nombres_bienes.html", {"bienes":bienes})
	return JsonResponse({"cod_bien":cod_bien,"cod_Inventariound":cod_Inventariound,"nombre":nombre,})

def load_bien_detalles(request):
	id_bien=request.GET.get('id_bien')
	bien = Bien.objects.get(pk=id_bien)
	return JsonResponse({"tipo_mantenimiento":bien.tipo_mantenimiento,"freq_mantenimiento":bien.frecuencia_mantenimiento,
	"caracteristicas":bien.caracteristicas,"marca":bien.marca,"modelo":bien.modelo,"n_serie":bien.n_serie})

def load_ingreso_bienes(request):
	num_factura = request.GET.get('num_factura')
	ingreso_bienes = Ingreso_Bien.objects.get(num_factura=num_factura)
	return JsonResponse({"cod_orden":ingreso_bienes.cod_orden,"fecha_facturacion":ingreso_bienes.fecha_factura,"centro_costos":ingreso_bienes.centro_costos.nombre,"id_ingreso":ingreso_bienes.pk,})

def load_ingreso_bienes_id(request):
	id_ingreso = request.GET.get('id_ingreso')
	ingreso_bienes = Ingreso_Bien.objects.get(pk=id_ingreso)
	return JsonResponse({"cod_orden":ingreso_bienes.cod_orden,"fecha_facturacion":ingreso_bienes.fecha_factura,"centro_costos":ingreso_bienes.centro_costos.nombre,"num_factura":ingreso_bienes.num_factura,"ruc_ci":ingreso_bienes.proveedor.ruc,})