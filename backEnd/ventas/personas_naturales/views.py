from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from .forms import Natural_NuevoForm
from .models import Persona_Natural 
from . import forms
from .filters import NaturalBusquedaFilter
from django.core.paginator import Paginator
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

from ventas.seguimientos.forms import Seguimiento_NaturalForm
from ventas.seguimientos.models import *
from academico.evento.models import Evento
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from datetime import date
from seguridad.models import Usuario
# Create your views here.

def index(request):
    naturales_lista = Persona_Natural.objects.all()
    naturales_filter = NaturalBusquedaFilter(request.GET, queryset=naturales_lista)
    paginator = Paginator(naturales_filter.qs, 30) 
    page = request.GET.get('page')
    naturales = paginator.get_page(page)
    return render(request, 'personas_naturales/natural.html', {'naturales_filter': naturales_filter,"naturales":naturales})

def natural_nuevo_t(request):
	if(request.method == "POST"):
		form = forms.Natural_NuevoForm(request.POST)
		if(form.is_valid()):
			form.save()
			return redirect("natural_lista")
		return render(request,"personas_naturales/natural_nuevo.html", {"form":form})
	return redirect("natural_lista")

def natural_nuevo(request):
	if(request.method == "POST"):
		# form = forms.Natural_NuevoForm(request.POST)
		# if(form.is_valid()):
		# 	vacios = 0
		# 	for f in form.fields:
		# 		if(form[f].data==""):
		# 			vacios=vacios+1
		# 	return render(request, "personas_naturales/natural_confirmacion.html", {"form":form, "vacios":vacios})
		form = forms.Natural_NuevoForm(request.POST)
		if(form.is_valid()):
			form.save()
			return redirect("natural_lista")
		return render(request,"personas_naturales/natural_nuevo.html", {"form":form})
	else:
		form = forms.Natural_NuevoForm()
	return render(request,"personas_naturales/natural_nuevo.html", {"form":form})

class NaturalUpdate(UpdateView):
	model = Persona_Natural
	form_class = Natural_NuevoForm
	template_name = 'personas_naturales/natural_editar.html'
	success_url = reverse_lazy('natural_lista')

def natural_delete(request, pk=None):
	"""model = Persona_Natural
	template_name = 'personas_naturales/natural_eliminar.html'
	form_class = Natural_NuevoForm
	success_url = reverse_lazy('natural_lista')"""
	
	if(request.method == "POST"):
		p = get_object_or_404(Persona_Natural,pk=pk)
		p.delete()
		return redirect("natural_lista")
	else:
		pk = request.GET.get('cedula')
		cedula_char="0"+str(pk)
		p = get_object_or_404(Persona_Natural,pk=cedula_char)
		return render(request, 'personas_naturales/natural_eliminar.html', {'object': p})


def seguimientoNaturalCreate(request):
	natural_id=request.GET.get('pk')
	l=len(str(natural_id))
	if l!=10:
		cedula_char="0"+str(natural_id)
	else :
		cedula_char=natural_id
	seguimientos_form = Seguimiento_NaturalForm()
	natural=Persona_Natural.objects.get(cedula=cedula_char)
	return render(request,"personas_naturales/seguimiento_natural.html",{"natural":natural,"seguimientos_form":seguimientos_form})

def crear_seguimiento_natural(request):
	if request.method == 'POST':
		n_id=request.POST.get("pers_natural")
		natural=Persona_Natural.objects.get(cedula=n_id)
		asesor=None
		if request.user.is_authenticated:
			username = request.user.username
			User= Usuario.objects.get(username=username)
			asesor=User
		form = Seguimiento_NaturalForm(request.POST)
		if form.is_valid():
			try:
				pre=str(int(Seguimiento_PersonaNatural.objects.latest('pk').pk+1))
				sec='0'*(4-len(pre))+pre
			except Seguimiento_PersonaNatural.DoesNotExist:
				sec='0001' 
			form.instance.n_registro=sec
			estado=form.instance.estado_seguimiento
			
			form.instance.asesor=asesor
			form.save()
			if form.instance.proximo_seguimiento !=None:
				f=form.instance
				pre2=str(int(Seguimiento_PersonaNatural.objects.latest('pk').pk+1))
				sec2='0'*(4-len(pre2))+pre2
				newForm=Seguimiento_PersonaNatural(n_registro=sec2,fecha_registro=f.fecha_registro,fecha_seguimiento=f.proximo_seguimiento,estado_seguimiento="PCTC",canal_de_contacto=f.canal_de_contacto,exito=f.exito,cod_evento=f.cod_evento,nombre_evento=f.nombre_evento,tipo_inscripcion=f.tipo_inscripcion,observaciones=f.observaciones,pers_natural=f.pers_natural,estado_participante=f.estado_participante,asesor=asesor)
				newForm.save()
			return JsonResponse({'msj':"Se ha guardado el seguimiento con éxito"},status=200)
		else:
			return render_to_response("personas_naturales/seguimiento_natural.html", context={"seguimientos_form": form,'natural':natural}, status=500)


def cargarEventosNatural(request):
	codigo=[]
	nombre=[]
	eventos= Evento.objects.all().filter
	codigo=render_to_string("personas_naturales/dropdown_Ecodigo_natural.html",{"eventos":eventos})
	nombre=render_to_string("personas_naturales/dropdown_Enombre_natural.html",{"eventos":eventos})
	return JsonResponse({'cod': codigo, 'nom': nombre})