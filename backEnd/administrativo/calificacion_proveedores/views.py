from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from ventas.personas_naturales.models import Persona_Natural
from ventas.personas_juridicas.models import Juridica
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from .models import *
from .models import Proveedor
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core.files import File
from . import forms
#Forms
from .forms import *


from dal import autocomplete

#Itertools
from itertools import chain

from django.core.paginator import Paginator



# Create your views here.

def index_calificacion_proveedores(request):
	calificacion_proveedores_list = Calificacion_proveedor.objects.all().order_by("pk")
	filter = Calificacion_proveedorFilter(request.GET, queryset=calificacion_proveedores_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	calificacion_proveedores = paginator.get_page(page)
	return render(request, 'index_calificacion.html', {'calificacion_proveedores': calificacion_proveedores, "filter":filter})


class calificacion_proveedores_view(CreateView):
	model= Calificacion_proveedor
	form_class= Calificacion_proveedorForm
	template_name='form_calificacion.html'
	success_url=reverse_lazy('index_calificacion_proveedores')

	# def get_context_data(self, **kwargs):
	# 	context=super(calificacion_proveedores_view,self).get_context_data(**kwargs)
	# 	formset=self.formset_class()
	# 	if formset not in context:
	# 		context['formset']=formset
	# 	return context
	
	def post(self, request, *args, **kwargs):
		self.object =self.get_object
		form=self.form_class(request.POST)
		if form.is_valid():
			try:
				pre = str(int(Calificacion_proveedor.objects.latest('pk').pk)+1)
				sec = '0'*(4-len(pre))+pre
			except Calificacion_proveedor.DoesNotExist:
				sec = '0001'
			calificacion=form.save(commit=False)
			calificacion.cod_calificacion = sec
			calificacion.save()
			# form.instance.cod_calificacion = sec
			# +'-'+str(date.today().year)
			# calificacion_proveedor=form.save()
			return redirect('index_calificacion_proveedores')
		else:
			return self.render_to_response(self.get_context_data(form=form))



class editar_calificacion_proveedor(UpdateView):
	model = Calificacion_proveedor
	form_class = Calificacion_proveedorUpdateForm
	template_name = 'editar_forma_calificacion_proveedores.html'
	success_url = reverse_lazy('index_calificacion_proveedores')

	def get_context_data(self,**kwargs):
		pk=self.kwargs.get('pk',0)
		context = super(editar_calificacion_proveedor, self).get_context_data(**kwargs)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		pk=self.kwargs.get('pk',0)
		orden= self.model.objects.get(pk=pk)
		form=self.form_class(request.POST, instance=self.object)
		
		if form.is_valid():
			form.save()
			print("SI FUNCIONA")
			print(self.object)
			return redirect(self.get_success_url())
		else:
			print("NOOOOo")
			return self.render_to_response(self.get_context_data(form=form))




def load_personas(request):
    proveedor = request.GET.get("proveedor")
    identificacion=[]
    razon_nombre=[]
    proveedores=Proveedor.objects.all()
    print(proveedores)
    identificacion=render_to_string("dropdown_proveedor_rucOF.html",{"proveedores":proveedores})
    razon_nombre=render_to_string("dropdown_proveedor_razonOF.html",{"proveedores":proveedores})
    return JsonResponse({'ruc_ci': identificacion, 'razon_nombre': razon_nombre})




def load_eventos(request):
    participantes= OrdenFacturacionParticipante.objects.all().distinct("cod_evento")
    listae=[]
    for p in participantes:
        listae.append(p.cod_evento)
    eventos=Evento.objects.filter(codigo_evento__in=listae)
    print(eventos)
    eventoslist=render_to_string("dropdown_evento.html",{"eventos":eventos})  
    return JsonResponse({'eventos': eventoslist})