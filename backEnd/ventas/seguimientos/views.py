from django.shortcuts import render, redirect,render_to_response
from django.forms.models import inlineformset_factory, modelformset_factory
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import SeguimientoEmpresa, Seguimiento_PersonaNatural, Seguimiento_Interesados
from ..personas_juridicas.models import Juridica
from .forms import *
from django.urls import reverse_lazy
from .models import Seguimiento_PersonaNatural, Seguimiento_Interesados
from .filters import *
from datetime import date
from ..proformas.models import Proforma
from ..propuesta_corp.models import PropuestaCorporativo
from django.http.response import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.http import JsonResponse
from django.template.loader import render_to_string

from financiero.procesos_especiales.models import ParticipanteIntermedio
from academico.evento.models import Evento
from ventas.interesados.models import CanalContacto
from seguridad.models import Usuario
# Create your views here.
def index_empresa(request):
    seguimiento_emp = SeguimientoEmpresa.objects.all().order_by('pk')
    emp_filter = SeguimientoEmpresaFilter(request.GET, queryset=seguimiento_emp)
    return render(request, "seguimientos/empresa/index_seguimiento_empresa.html", {"filter":emp_filter})

def nuevo_seguimieto_empresa(request):
    ruc=request.GET.get('pk')
    empresa=Juridica.objects.get(ruc=ruc)
    form=SeguimientoEmpresaForm()
    formset=SEFormset()
    return render(request,"seguimientos/empresa/nuevo_seguimiento_empresa.html",context={"empresa":empresa,"form":form,"formset":formset})

def SeguimientoEmpresaNuevo(request):
    if request.method == 'POST':
        j_id=request.POST.get("juridica")
        empresa=Juridica.objects.get(ruc=j_id)
        form=SeguimientoEmpresaForm(request.POST)
        formset=SEFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                pre = str(int(SeguimientoEmpresa.objects.latest('pk').pk)+1)
                sec = '0'*(4-len(pre))+pre
            except SeguimientoEmpresa.DoesNotExist:
                sec = '0001'
            seg=form.save(commit=False)
            seg.n_seguimiento = sec
            seg.added_by=request.user
            seg.save()
            seg_id=str(seg.id+1)
            for f in formset:
                if f.is_valid():
                    ff=f.save(commit=False)
                    if ff.nombre_evento and ff.codigo_evento:
                        ff.seguimiento_empresa=seg
                        ff.save()
            if seg.fecha_proximo:
                form2=SeguimientoEmpresaForm(request.POST)
                formset2=SEFormset(request.POST)
                if form2.is_valid() and formset2.is_valid():
                    sec = '0'*(4-len(seg_id))+seg_id
                    seg2 = form2.save(commit=False)
                    seg2.n_seguimiento=sec
                    seg2.estado=EstadoSeguimiento.objects.get(pk=1)
                    seg2.fecha_seguimiento=seg.fecha_proximo
                    seg2.added_by=request.user
                    seg2.fecha_proximo=None
                    seg2.fecha_sin_respuesta=None
                    seg2.fecha_contactado=None
                    seg2.fecha_contacto_invalido=None
                    seg2.fecha_por_contactar=date.today()
                    seg2.save()
                    for f2 in formset2:
                        if f2.is_valid():
                            ff2=f2.save(commit=False)
                            if ff2.nombre_evento and ff2.codigo_evento:
                                ff2.seguimiento_empresa=seg2
                                ff2.save()
            return JsonResponse({'msj':"Se ha guardado el seguimiento con éxito"},status=200)
        return render_to_response("seguimientos/empresa/nuevo_seguimiento_empresa.html", context={"form": form,"formset":formset,'empresa':empresa}, status=500)


def eliminar_seguimieto_empresa(request):
    seg_id=request.GET.get('seg_id')
    seg=SeguimientoEmpresa.objects.get(pk=seg_id)
    return render(request, "seguimientos/empresa/eliminar_seguimiento_empresa.html", {"seg": seg})

  
class SeguimientoEmpresaEliminar(DeleteView):
    model=SeguimientoEmpresa
    success_url=reverse_lazy('seguimiento_empresa')

class SeguimientoEmpresaEditar(UpdateView):
    model=SeguimientoEmpresa
    form_class=SeguimientoEmpresaEditarForm
    formset_class=SEFormset
    template_name="seguimientos/empresa/editar_seguimiento_empresa.html"
    success_url=reverse_lazy('seguimiento_empresa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresa']=self.object.juridica
        if 'formset' not in context:
            if self.request.POST:
                context['formset'] =self.formset_class(self.request.POST,instance=self.object)
            else:
                context['formset'] =self.formset_class(instance=self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form=self.form_class(request.POST,instance=self.object)
        formset=self.formset_class(request.POST,instance=self.object)
        if form.is_valid() and formset.is_valid():
            seg=form.save(commit=False)
            #New user overwrites old user
            #seg.added_by=request.user
            #Old user always
            seg.save()
            formset.save()
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form,formset=formset))



def index_persona_natural(request):
    f = SeguimientoNaturalFilter(
        request.GET, queryset=Seguimiento_PersonaNatural.objects.all().order_by("id"))
    return render(request, "seguimientos/index_seguimientos_personas_naturales.html", context={"filter": f})


def index_interesados(request):
    f = SeguimientoInteresadosFilter(
        request.GET, queryset=Seguimiento_Interesados.objects.all().order_by("n_registro_interesado"))
    return render(request, "seguimientos/index_seguimientos_interesados.html", context={"filter": f})


class segumientoNaturalEdit(UpdateView):
	model = Seguimiento_PersonaNatural
	template_name = 'seguimientos/seguimiento_natural_editar.html'
	form_class = Seguimiento_Natural_EditarForm
	success_url = reverse_lazy('index_seguimientos_personas_naturales')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pk=self.kwargs.get('pk',0)
		sp=Seguimiento_PersonaNatural.objects.get(pk=pk)
		context['personaN'] =Natural_Mostrar(initial={"cedula":sp.pers_natural.cedula,"nombres":sp.pers_natural.nombres,"apellidos":sp.pers_natural.apellidos})
		return context

	def form_valid(self, form):
		estado = form.instance.estado_seguimiento
		pk=self.kwargs.get('pk',0)
		sp=Seguimiento_PersonaNatural.objects.get(pk=pk)
		form.instance.asesor=sp.asesor
		return super(segumientoNaturalEdit, self).form_valid(form)

def segumientoNatural_conf_elim(request):
	seguimiento_id=request.GET.get('pk')
	seguimiento=Seguimiento_PersonaNatural.objects.get(pk=seguimiento_id)
	return render(request,"seguimientos/seguimiento_natural_delete.html",{"seguimiento":seguimiento})

class segumientoNaturalDelete(DeleteView):
    model=Seguimiento_PersonaNatural
    template_name='proforma_delete.html'
    form_class=Seguimiento_Natural_EditarForm
    success_url=reverse_lazy('index_seguimientos_personas_naturales')

def seguimientosNaturalEventos(request):
    if request.method == "POST":
        form=SeguimientoEventoCreateForm(request.POST)
        asesor=None
        if request.user.is_authenticated:
            username = request.user.username
            User= Usuario.objects.get(username=username)
            asesor=User
        if form.is_valid() :
            codO= form.cleaned_data.get("codigo_eventoO")
            part= ParticipanteIntermedio.objects.filter(cod_evento=codO)
            fechaR=form.cleaned_data.get("fecha_registro")
            fechaS=form.cleaned_data.get("fecha_seguimiento")
            estadoS=form.cleaned_data.get("estado_seguimiento")
            canal=CanalContacto.objects.get(pk=form.cleaned_data.get("canal_contacto"))
            exito=form.cleaned_data.get("exito")
            estadoP=form.cleaned_data.get("estado_participante")
            observacion=form.cleaned_data.get("observaciones")
            codD=form.cleaned_data.get("codigo_eventoD")
            nomD=form.cleaned_data.get("nombre_eventoD")
            for p in part:
                try:
                    pre=str(int(Seguimiento_PersonaNatural.objects.latest('pk').pk+1))
                    sec='0'*(4-len(pre))+pre
                except Seguimiento_PersonaNatural.DoesNotExist:
                    sec='0001' 
                newForm=Seguimiento_PersonaNatural(n_registro=sec,fecha_registro=fechaR,fecha_seguimiento=fechaS,estado_seguimiento=estadoS,canal_de_contacto=canal,exito=exito,cod_evento=codD,nombre_evento=nomD,observaciones=observacion,pers_natural=p.participante,estado_participante=estadoP,asesor=asesor)
                newForm.save()
            return HttpResponseRedirect(reverse_lazy("index_seguimientos_personas_naturales"))
    else :
        form=SeguimientoEventoCreateForm()
    return render(request, "seguimientos/seguimiento_natural_evento.html", {"form":form})

def load_eventos_participantes(request):
	codigo=[]
	nombre=[]
	codigos=[]
	participante=ParticipanteIntermedio.objects.distinct("cod_evento")
	for p in participante :
		codigos.append(p.cod_evento)
	eventos= Evento.objects.filter(codigo_evento__in=codigos,estado="Ejecutado")
	codigo=render_to_string("seguimientos/natural/dropdown_event_C.html",{"eventos":eventos})
	nombre=render_to_string("seguimientos/natural/dropdown_event_N.html",{"eventos":eventos})
	# codigo=render_to_string("seguimientos/natural/dropdown_part_event_C.html",{"participante":participante})
	# nombre=render_to_string("seguimientos/natural/dropdown_part_event_N.html",{"participante":participante})
	return JsonResponse({'cod': codigo, 'nom': nombre})

# def load_eventos_participantes_other(request):
# 	cod_evento = request.GET.get("cod_evento")
# 	codigo=[]
# 	nombre=[]
# 	participante=ParticipanteIntermedio.objects.distinct("cod_evento").exclude(cod_evento=cod_evento)
# 	codigo=render_to_string("seguimientos/natural/dropdown_part_event_C.html",{"participante":participante})
# 	nombre=render_to_string("seguimientos/natural/dropdown_part_event_N.html",{"participante":participante})
# 	return JsonResponse({'cod': codigo, 'nom': nombre})

def load_eventos_participantes_other(request):
	cod_evento = request.GET.get("cod_evento")
	codigo=[]
	nombre=[]
	estados=["Programado","Reprogramado"]
	evento=Evento.objects.exclude(codigo_evento=cod_evento).filter(estado__in=estados)
	codigo=render_to_string("seguimientos/natural/dropdown_event_C.html",{"eventos":evento})
	nombre=render_to_string("seguimientos/natural/dropdown_event_N.html",{"eventos":evento})
	return JsonResponse({'cod': codigo, 'nom': nombre})

class seguimientoInteresadoEdit(UpdateView):
    model = Seguimiento_Interesados
    second_model = Interesado
    template_name = 'seguimientos/seguimiento_interesado_editar.html'
    form_class = Seguimiento_Interesados_EditarForm
    success_url = reverse_lazy('index_seguimientos_interesados')

    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        interesado = Interesado.objects.get(seguimiento_interesados=pk)
        interesado_form = Interesado_Mostrar
        context["interesado"] = interesado_form(initial={
            "nombre":interesado.nombre,
            "apellido":interesado.apellido,
            "correo":interesado.correo,
            "celular":interesado.celular})
        return context

    
def segumientoInteresado_conf_elim(request):
	seguimiento_id=request.GET.get('pk')
	seguimiento=Seguimiento_Interesados.objects.get(pk=seguimiento_id)
	return render(request,"seguimientos/seguimiento_interesado_delete.html",{"seguimiento":seguimiento})

class segumientoInteresadoDelete(DeleteView):
    model=Seguimiento_Interesados
    template_name='proforma_delete.html'
    form_class=Seguimiento_Interesados_EditarForm
    success_url=reverse_lazy('index_seguimientos_interesados')



def load_n_participantes(request):
    cod = request.GET.get("cod")
    tipo_oferta = request.GET.get("oferta")
    n_participantes = None
    if tipo_oferta == "Proforma":
        try:
            n_participantes = Proforma.objects.get(codigo__iexact=cod).numeroParticipantes
        except Proforma.DoesNotExist:
            n_participantes = None

    elif tipo_oferta=="Propuesta":
        try:
            n_participantes = PropuestaCorporativo.objects.get(cod_propuesta__iexact=cod).numero_participantes
        except PropuestaCorporativo.DoesNotExist:
            n_participantes = None
    return HttpResponse(n_participantes, content_type="application/json")

def load_oferta(request):
    ruc = request.GET.get("ruc")
    tipo_oferta = request.GET.get("tipo")
    if tipo_oferta == "Proforma":
        ofertas=Proforma.objects.filter(ruc_ci=ruc)
    elif tipo_oferta=="Propuesta":
        ofertas=PropuestaCorporativo.objects.filter(ruc_ci=ruc)
    return render(request, "seguimientos/empresa/dropdown_oferta.html", {"ofertas": ofertas})


def load_evento_tipo(request):
    tipo = request.GET.get('tipo')
    eventos = Evento.objects.filter(publico = tipo).order_by('-pk')
    codigo= render_to_string("seguimientos/empresa/dropdown_evento_codigo.html",{"eventos": eventos})
    nombre=render_to_string("seguimientos/empresa/dropdown_evento_nombre.html",{"eventos": eventos})
    return JsonResponse({'codigo':codigo,'nombre':nombre})



