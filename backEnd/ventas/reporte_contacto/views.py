from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponseRedirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .models import ReporteContacto, Capacitacion, Asesoria
from .forms import ReporteContactoForm, CapacitacionForm, AsesoriaForm
from ventas.personas_juridicas.models import Juridica
from django.urls import reverse_lazy
from django.db.models import Q
from dal import autocomplete
from datetime import date


# Create your views here.
class ReporteAutocomplete(autocomplete.Select2QuerySetView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = ReporteContacto.objects.all().order_by("ruc_ci")
        if self.q:
            qs = qs.filter(Q(ruc_ci__istartswith=self.q) | Q(cod_reporte__istartswith=self.q))
        return qs

    def has_add_permission(self, request):
        return True

class ReporteContactoCreate(CreateView):
    model=ReporteContacto
    template_name= 'reporte_form.html'
    form_class=ReporteContactoForm
    success_url='editar'
    
    def post(self, request, *args, **kwargs):
        self.object =self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            try:
                pre = str(int(self.model.objects.latest('pk').pk+1))
                sec = '0'*(4-len(pre))+pre
            except self.model.DoesNotExist:
                sec = '0001'
            form.instance.cod_reporte = 'RC-CEC-'+sec+'-'+str(date.today().year)
            reporte=form.save()
            return HttpResponseRedirect(self.get_success_url()+'/'+str(reporte.pk))
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ReporteContactoUpdate(UpdateView):
    model=ReporteContacto
    second_model=Capacitacion
    third_model=Asesoria
    template_name='reporte_update.html'
    form_class=ReporteContactoForm
    success_url=reverse_lazy('reporte_contacto')
    def get_context_data(self, **kwargs):
        context =super(ReporteContactoUpdate, self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        capacitaciones=self.second_model.objects.filter(reporte_id=pk)
        asesorias=self.third_model.objects.filter(reporte_id=pk)
        context['capacitaciones']=capacitaciones
        context['asesorias']=asesorias
        context['reporte_id']=pk
        l=[]
        vals=str(self.model.objects.get(pk=pk).servicios_requeridos).split(',')
        for s in self.model.SERVICIOS_CHOICES:
            if s[1] in vals or ' '+s[1] in vals:
                l.append(s[0])
        context['checked_servicios_requeridos']=l
        return context

class ReporteContactoDelete(DeleteView):
    model=ReporteContacto
    template_name='reporte_delete_2.html'
    success_url=reverse_lazy('reporte_contacto')
    form_class=ReporteContactoForm

def reportcontacto_conf_elim(request):
    orden_id=request.GET.get('pk')
    orden=ReporteContacto.objects.get(id=orden_id)
    form=ReporteContactoForm(instance=orden)
    return render(request,"reporte_delete_2.html",{"reporte":orden,"form":form})

class CapacitacionCreate(CreateView):
    model=Capacitacion
    form_class=CapacitacionForm
    template_name='capacitacion_form.html'
    success_url='/ventas/reporte_contacto/editar'

    def get_context_data(self, **kwargs):
        context=super(CapacitacionCreate,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        context['reporte_id']=pk
        return context

    def post(self, request,*args,**kwargs):
        self.object =self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            reporte_id=kwargs['pk']
            c=form.save(commit=False)
            c.reporte_id=reporte_id
            c.save()
            return HttpResponseRedirect(self.get_success_url()+'/'+str(reporte_id))
        else:
            return self.render_to_response(self.get_context_data(form=form))


class CapacitacionUpdate(UpdateView):
    model=Capacitacion
    form_class=CapacitacionForm
    template_name='capacitacion_editar.html'
    success_url='/ventas/reporte_contacto/editar'

    def get_context_data(self, **kwargs):
        context=super(CapacitacionUpdate,self).get_context_data(**kwargs)
        fk=self.kwargs.get('fk',0)
        context['reporte_id']=fk
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        reporte_id=kwargs['fk']
        pk=kwargs['pk']
        capacitacion=self.model.objects.get(id=pk)
        form=self.form_class(request.POST, instance=capacitacion)
        if form.is_valid():
            c=form.save(commit=False)
            c.reporte_id=reporte_id
            c.save()
            return HttpResponseRedirect(self.get_success_url()+'/'+str(reporte_id))
        else:
            return self.render_to_response(self.get_context_data(form=form))


def capacitacion_conf_elim(request):
	capacitacion_id=request.GET.get('pk')
	capacitacion=Capacitacion.objects.get(pk=capacitacion_id)
	return render(request,"capacitacion_eliminar.html",{"capacitacion":capacitacion,"fk":request.GET.get('fk')})



class CapacitacionDelete(DeleteView):
    model=Capacitacion
    form_class=CapacitacionForm
    template_name='capacitacion_eliminar.html'
    success_url='/ventas/reporte_contacto/editar'

    def get_context_data(self, **kwargs):
        context=super(CapacitacionDelete,self).get_context_data(**kwargs)
        fk=self.kwargs.get('fk',0)
        context['reporte_id']=fk
        return context

    def post(self, request, *args, **kwargs):
        
        reporte_id=kwargs['fk']
        self.object=self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url()+'/'+str(reporte_id))


class AsesoriaCreate(CreateView):
    model=Asesoria
    form_class=AsesoriaForm
    template_name='asesoria_form.html'
    success_url='/ventas/reporte_contacto/editar'

    def get_context_data(self, **kwargs):
        context=super(AsesoriaCreate,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        context['reporte_id']=pk
        return context

    def post(self, request,*args,**kwargs):
        self.object =self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            reporte_id=kwargs['pk']
            a=form.save(commit=False)
            a.reporte_id=reporte_id
            a.save()
            return HttpResponseRedirect(self.get_success_url()+'/'+str(reporte_id))
        else:
            return self.render_to_response(self.get_context_data(form=form))

class AsesoriaUpdate(UpdateView):
    model=Asesoria
    form_class=AsesoriaForm
    template_name='asesoria_editar.html'
    success_url='/ventas/reporte_contacto/editar'
    
    def get_context_data(self, **kwargs):
        context=super(AsesoriaUpdate,self).get_context_data(**kwargs)
        fk=self.kwargs.get('fk',0)
        context['reporte_id']=fk
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        reporte_id=kwargs['fk']
        pk=kwargs['pk']
        asesoria=self.model.objects.get(id=pk)
        form=self.form_class(request.POST, instance=asesoria)
        if form.is_valid():
            a=form.save(commit=False)
            a.reporte_id=reporte_id
            a.save()
            return HttpResponseRedirect(self.get_success_url()+'/'+str(reporte_id))
        else:
            return self.render_to_response(self.get_context_data(form=form))


def asesoria_conf_elim(request):
	asesoria_id=request.GET.get('pk')
	asesoria=Asesoria.objects.get(pk=asesoria_id)
	return render(request,"asesoria_eliminar.html",{"asesoria":asesoria,"fk":request.GET.get('fk')})

class AsesoriaDelete(DeleteView):
    model=Asesoria
    form_class=AsesoriaForm
    template_name='asesoria_eliminar.html'
    success_url='/ventas/reporte_contacto/editar'
    

    def get_context_data(self, **kwargs):
        context=super(AsesoriaDelete,self).get_context_data(**kwargs)
        fk=self.kwargs.get('fk',0)
        context['reporte_id']=fk
        return context

    def post(self, request, *args, **kwargs):
        reporte_id=kwargs['fk']
        self.object=self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url()+'/'+str(reporte_id))

def load_reportes(request):
    ident = request.GET.get("id")
    reportes = ReporteContacto.objects.filter(ruc_ci=ident).order_by('-cod_reporte')
    return render(request, "dropdown_reportes.html", {"reportes":reportes})