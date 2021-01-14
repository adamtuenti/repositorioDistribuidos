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



def analisis_cotizaciones(request):	
	analisis_list = AnalisisCotizaciones.objects.all().order_by("pk")
	filter = AnalisisFilter(request.GET, queryset=analisis_list )
	paginator = Paginator(filter.qs, 30) 
	page = request.GET.get('page')
	analisis = paginator.get_page(page)
	return render(request, 'analisis_cotizaciones.html', {'analisis': analisis, "filter":filter})


class nuevo_analisis(CreateView):
	model = AnalisisCotizaciones
	form_class = CotizacionesForm
	template_name = 'nuevo_analisis.html'
	success_url = reverse_lazy('analisis_cotizaciones')
	
	def get_success_url(self):
		return reverse_lazy('analisis_cotizaciones')
