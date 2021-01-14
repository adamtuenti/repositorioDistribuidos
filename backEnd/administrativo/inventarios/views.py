from django.shortcuts import render
from .models import Inventario, BienInventario
from django.template.loader import render_to_string
from administrativo.ingreso_bienes.models import *
from django.urls import reverse_lazy
from . import forms
from .forms import *
from django.db import transaction
from django.http import JsonResponse
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.shortcuts import render,redirect, get_object_or_404

from django.core.paginator import Paginator

# Create your views here.

def index_inventarios(request):	
	inventarios_list = Inventario.objects.all().order_by("pk")
	filter = InventarioFilter(request.GET, queryset=inventarios_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	inventarios = paginator.get_page(page)
	return render(request, 'index_inventarios.html', {'inventarios': inventarios, "filter":filter})

class inventarios_view(CreateView):
	model= Inventario
	form_class= InventarioForm
	template_name='nuevo_inventario.html'
	success_url=reverse_lazy('index_inventarios')

	def get_context_data(self, **kwargs):
		data = super(inventarios_view, self).get_context_data(**kwargs)
		if self.request.POST:
			data['formset'] = BienInventarioFormset(self.request.POST, self.request.FILES)
		else:
			data['formset'] = BienInventarioFormset()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		bienes = context['formset']
		with transaction.atomic():
			form.instance.created_by = self.request.user
			try:
				pre = str(int(self.model.objects.latest('pk').pk+1))
				sec = '0'*(4-len(pre))+pre
			except self.model.DoesNotExist:
				sec = '0001'
			form.instance.cod_inventario = sec
			self.object = form.save()
			if bienes.is_valid():
				bienes.instance = self.object
				bienes.save()
				# nel=[]
				# for obj in bienes.deleted_forms:
				# 		nel.append(obj.instance.bien)
				# for b in bienes :
				# 	if b.instance.bien!=None and b.instance.bien not in nel:
				# 		bien=Bien.objects.get(pk=b.instance.bien.id)
				# 		bien.save()
		return super(inventarios_view, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('index_inventarios')

def load_campos_bien_inventario(request):
	constataciones = render_to_string("dropdown_template.html", {"opciones":BienInventario.CONSTATACIONES_CHOICES})
	sedes = render_to_string("dropdown_template.html", {"opciones":BienInventario.SEDE_CHOICES})
	estados = render_to_string("dropdown_template.html", {"opciones":BienInventario.ESTADO_CHOICES})
	return JsonResponse({'constataciones': constataciones, 'sedes': sedes, 'estados': estados,})