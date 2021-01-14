from django.shortcuts import render
from .models import Mantenimiento
from administrativo.ingreso_bienes.models import *
from django.urls import reverse_lazy
from . import forms
from .forms import *
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.shortcuts import render,redirect, get_object_or_404

from django.core.paginator import Paginator

# Create your views here.

def index_mantenimientos(request):
	mantenimientos_list = Mantenimiento.objects.all().order_by("pk")
	filter = MantenimientoFilter(request.GET, queryset=mantenimientos_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	mantenimientos = paginator.get_page(page)
	return render(request, 'index_mantenimientos.html', {'mantenimientos': mantenimientos, "filter":filter})

class mantenimientos_view(CreateView):
	model= Mantenimiento
	form_class= MantenimientoForm
	template_name='form_mantenimientos.html'
	success_url=reverse_lazy('index_mantenimientos')
    
	def post(self, request, *args, **kwargs):
		self.object =self.get_object
		form=self.form_class(request.POST, request.FILES)
		if form.is_valid():
			try:
				pre = str(int(self.model.objects.latest('pk').pk+1))
				sec = '0'*(4-len(pre))+pre
			except self.model.DoesNotExist:
				sec = '0001'
			form.instance.cod_mantenimiento = sec
			# +'-'+str(date.today().year)
			mantenimiento=form.save()
			return redirect('index_mantenimientos')
		else:
			return self.render_to_response(self.get_context_data(form=form))

class editar_mantenimiento(UpdateView):
	model = Mantenimiento
	form_class = MantenimientoUpdateForm
	template_name = 'editar_mantenimiento.html'
	success_url = reverse_lazy('index_mantenimiento')

	def get_context_data(self,**kwargs):
		pk=self.kwargs.get('pk',0)
		context = super().get_context_data(**kwargs)
		return context
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		pk=self.kwargs.get('pk',0)
		orden= self.model.objects.get(pk=pk)
		form=self.form_class(request.POST, request.FILES, instance=self.object)
		
		if form.is_valid():
			form.save()
			print(form)
			return redirect(self.get_success_url())
		else:
			print(form)
			print("no")
			return self.render_to_response(self.get_context_data(form=form))

def load_bien_detalles(request):
    id = request.GET.get("id")
    idF = request.GET.get("idF")
    bien=Bien.objects.get(pk=id)
    return JsonResponse({'frecuencia_Mantenimiento': bien.frecuencia_Mantenimiento,'preventivo':bien.preventivo,"correctivo":bien.correctivo,"idF":idF})