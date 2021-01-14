from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import TemplateView,ListView,UpdateView,CreateView,DeleteView
from .forms import ProductoForm, ProductoUpdateForm
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Producto
from django.core.exceptions import ValidationError
from datetime import date
#Forms
from .forms import *


from dal import autocomplete

#Itertools
from itertools import chain

from django.core.paginator import Paginator


def index_productos(request):
	productos_list = Producto.objects.all().order_by("pk")
	filter = ProductoFilter(request.GET, queryset=productos_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	productos = paginator.get_page(page)
	return render(request, 'producto_index.html', {'productos': productos, "filter":filter})
    

# def productos_view(request):
# 	if(request.method == "POST"):
# 		print(request.POST)
# 		form = ProductoForm(request.POST)
# 		if(form.is_valid()):
# 			print("Acabo de entrar al post")
# 			form.save()
# 			return redirect('index_productos')
# 	else:
# 		form = ProductoForm()
# 		print('entre a productos view')
# 	return render(request,"prod.html", {"form":form})



class productos_view(CreateView):
	model= Producto
	form_class= ProductoForm
	template_name='prod.html'
	success_url=reverse_lazy('index_productos')
	
	def post(self, request, *args, **kwargs):
		self.object =self.get_object
		form=self.form_class(request.POST)
		if form.is_valid():
			try:
				pre = str(int(self.model.objects.latest('pk').pk+1))
				sec = '0'*(4-len(pre))+pre
			except self.model.DoesNotExist:
				sec = '0001'
			form.instance.cod_producto = sec
			# +'-'+str(date.today().year)
			producto=form.save()
			return redirect('index_productos')
		else:
			return self.render_to_response(self.get_context_data(form=form))


class editar_producto(UpdateView):
	model = Producto
	form_class = ProductoUpdateForm
	template_name = 'editar_prod.html'
	success_url = reverse_lazy('index_productos')

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
			print(form)
			return redirect(self.get_success_url())
		else:
			print(form)
			print("no")
			return self.render_to_response(self.get_context_data(form=form))
        


	# def post(self, request, *args, **kwargs):
	# 	print("lol")
	# 	self.object=self.get_object()
        
	# 	form=self.form_class(request.POST)
	# 	pk=self.kwargs.get('pk',0)
	# 	print(pk)
        
	# 	if form.is_valid():
	# 		prop= self.model.objects.get(pk=pk)
	# 		formr = self.form_class(request.POST or None, instance=prop)
	# 		formr.save()
	# 		return HttpResponseRedirect(self.get_success_url())
	# 	else:
	# 		return self.render_to_response(self.get_context_data(form=form))


		

# def editar_producto(request,pk):
# 	producto = Producto.objects.get(pk=pk)
# 	if request.method == "GET":
# 		producto_form = ProductoForm(instance = producto)
# 	else:
# 		producto_form = ProductoForm(request.POST, instance = producto)
# 		if producto_form.is_valid():
# 			producto_form.save()
# 		redirect('index_productos')
# 	return render(request,'prod.html',{'producto_form':producto_form})
