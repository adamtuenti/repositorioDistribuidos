from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProveedorForm, ProveedorUpdateForm
from .models import Proveedor
from .models import Ciudad
from .models import Sector
from .models import TipoEmpresa
from django.core.exceptions import ValidationError
from datetime import date
#Forms
from .forms import *


from dal import autocomplete

#Itertools
from itertools import chain

from django.core.paginator import Paginator



# Create your views here.

def index_proveedores(request):
	proveedores_list = Proveedor.objects.all().order_by("pk")
	filter = ProveedorFilter(request.GET, queryset=proveedores_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	proveedores = paginator.get_page(page)
	return render(request, 'index_proveedores.html', {'proveedores': proveedores, "filter":filter})

	
def load_ciudades(request):
	provincia_id = request.GET.get("provincia")
	ciudades = Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
	
	return render(request,"proveedores/dropdown_ciudades.html",{"ciudades":ciudades})




# def proveedores_view(request):

# 	if(request.method == "POST"):
# 		print(request.POST)
# 		form = ProveedorForm(request.POST)
# 		if(form.is_valid()):
# 			print("Acabo de entrar al post")
# 			form.save()
# 			return redirect('index_proveedores')
# 	else:
# 		form = ProveedorForm()
# 	return render(request,"forma_proveedores.html", {"form":form})



class proveedores_view(CreateView):
	model= Proveedor
	form_class= ProveedorForm
	template_name='forma_proveedores.html'
	success_url=reverse_lazy('index_proveedores')
	
	def post(self, request, *args, **kwargs):
		self.object =self.get_object
		form=self.form_class(request.POST)
		if form.is_valid():
			try:
				pre = str(int(self.model.objects.latest('pk').pk+1))
				sec = '0'*(4-len(pre))+pre
			except self.model.DoesNotExist:
				sec = '0001'
			form.instance.cod_proveedor = sec
			# +'-'+str(date.today().year)
			proveedor=form.save()
			return redirect('index_proveedores')
		else:
			return self.render_to_response(self.get_context_data(form=form))








class editar_proveedor(UpdateView):
	model = Proveedor
	form_class = ProveedorUpdateForm
	template_name = 'editar_forma_proveedores.html'
	success_url = reverse_lazy('index_proveedores')

	def get_context_data(self,**kwargs):
		pk=self.kwargs.get('pk',0)
		context = super().get_context_data(**kwargs)
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







# def proveedores_editar(request,pk):
# 	if(request.method == "POST"):
# 				if(form.is_valid()):
# 					pase = False
# 					if(pase):
# 						form.save()
# 						return HttpResponseRedirect(reverse_lazy("index_proveedores"))
# 				else:
# 					url = reverse_lazy('proveedores_editar', kwargs={'pk': pk})
# 					return HttpResponseRedirect(url)
			
# 	else:
# 		p = get_object_or_404(Proveedor, pk=pk)
# 		form = ProveedorForm(instance=p)
# 	return render(request,'editar_forma_proveedores.html')





def load_proveedor(request):
	tipo=request.GET.get('tipo')
	proveedores = Proveedor.objects.filter(tipo_proveedor__nombre=tipo)
	ruc_ci = render_to_string("dropdown_ci.html", {"proveedores":proveedores})
	razon_nombre = render_to_string("dropdown_nombres.html", {"proveedores":proveedores})
	return JsonResponse({"ruc_ci":ruc_ci,"razon_nombre":razon_nombre})


def load_all_proveedor(request):
	proveedores = Proveedor.objects.all()
	ruc_ci = render_to_string("dropdown_ci.html", {"proveedores":proveedores})
	razon_nombre = render_to_string("dropdown_nombres.html", {"proveedores":proveedores})
	return JsonResponse({"ruc_ci":ruc_ci,"razon_nombre":razon_nombre})

# def load_personas(request):
#     proveedor = request.GET.get("proveedor")
#     identificacion=[]
#     razon_nombre=[]
#     if persona=="Natural":
#         personas=Persona_Natural.objects.all()
#         print(personas)
#         print("natural")
#         identificacion=render_to_string("dropdown_natural_ciOF.html",{"personas":personas})
#         razon_nombre=render_to_string("dropdown_natural_nombresOF.html",{"personas":personas})
#     elif persona=="Jurídica":
#         personas=Juridica.objects.all()
#         print(personas)
#         print("juridica")
#         identificacion=render_to_string("dropdown_juridica_rucOF.html",{"personas":personas})
#         razon_nombre=render_to_string("dropdown_juridica_razonOF.html",{"personas":personas})
#     return JsonResponse({'ruc_ci': identificacion, 'razon_nombre': razon_nombre})




# def editar_proveedor(request,pk):
# 	proveedor_form = None
# 	error= None
# 	try:
# 		proveedor = Proveedor.objects.get(pk=pk)
# 		if request.method == "GET":
# 			proveedor_form = ProveedorForm(instance = proveedor)
# 		else:
# 			proveedor_form = ProveedorForm(request.POST, instance = proveedor)
# 			if proveedor_form.is_valid():
# 				proveedor_form.save()
# 			return redirect('index_proveedores')
# 	except ObjectDoesNotExist as e:
# 		error = e
# 	return render(request,'forma_proveedores.html',{'proveedor_form':proveedor_form, 'error':error})










# def editar_proveedor(request,pk):
# 	if(request.method == "POST"):
# 				if(form.is_valid()):
# 					pase = False
# 					if(pase):
# 						form.save()
# 						return HttpResponseRedirect(reverse_lazy("index_proveedores"))
# 				else:
# 					url = reverse_lazy('editar_proveedor', kwargs={'pk': pk})
# 					return HttpResponseRedirect(url)
			
# 	else:
# 		p = get_object_or_404(Proveedor, pk=pk)
# 		form = ProveedorForm(instance=p)
# 	return render(request,'forma_proveedores.html')