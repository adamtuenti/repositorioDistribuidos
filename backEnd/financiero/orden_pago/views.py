from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrdenPagoForm, OrdenPagoFormPagado, FileFormset,OrdenPagoFormEnviado,OrdenPagoFormAprobado
from .models import OrdenPago, Centro_Costos, Egresos, OrdenPagoFile
from ventas.personas_naturales.models import Persona_Natural
from ventas.personas_juridicas.models import Juridica
from .filters import OrdenPagoFilter
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from datetime import date
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.files import File
# The root path in this python project

# Create your views here.
def index(request):
    if (request.GET.get('estado',None)!=None and 'Anulado' in request.GET['estado']):
        ordPago_lista = OrdenPago.objects.all().order_by('pk')
    else:
        ordPago_lista = OrdenPago.objects.all().exclude(estado='Anulado').order_by('pk')
    ordPago_filter = OrdenPagoFilter(request.GET, queryset=ordPago_lista)
    return render(request, "orden_pago/ordenpago_list.html", {"ordenes_pago":ordPago_lista, "filter":ordPago_filter})


def load_egresos(request):
    centroc_id = request.GET.get("centroc")
    egresos = Egresos.objects.filter(centroc_id=centroc_id).order_by("nombre")
    return render(request, "orden_pago/dropdown_egresos.html", {"egresos":egresos})

class OrdenPagoCreate(CreateView):
    model=OrdenPago
    form_class=OrdenPagoForm
    formset_class=FileFormset
    template_name="orden_pago/ordenpago_nuevo.html"
    success_url=reverse_lazy('orden_pago_lista')

    def get_context_data(self, **kwargs):
        context=super(OrdenPagoCreate,self).get_context_data(**kwargs)
        formset=self.formset_class()
        if formset not in context:
            context['formset']=formset
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form=self.form_class(request.POST)
        formset=self.formset_class(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            try:
                pre = str(int(OrdenPago.objects.latest('pk').pk)+1)
                sec = '0'*(4-len(pre))+pre
            except OrdenPago.DoesNotExist:
                sec = '0001'
            orden=form.save(commit=False)
            orden.cod_ord_pago = sec+'-'+str(date.today().year)
            orden.save()
            for f in formset:
                if f.is_valid():
                    ff=f.save(commit=False)
                    ff.orden_pago=orden
                    ff.save()
            return redirect("orden_pago_lista")
        else:
            return self.render_to_response(self.get_context_data(form=form,formset=formset))


class OrdenPagoUpdate(UpdateView):
    model=OrdenPago
    second_model=OrdenPagoFile
    form_class=OrdenPagoForm
    formset_class=FileFormset
    template_name="orden_pago/ordenpago_nuevo.html"
    success_url=reverse_lazy('orden_pago_lista')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk',0)
        files=self.second_model.objects.filter(orden_pago_id=pk).count()
        context["files"]=files
        if self.request.POST:
            context['formset']=self.formset_class(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset']=self.formset_class(instance=self.object)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        pk=self.kwargs.get('pk',0)
        orden= self.model.objects.get(pk=pk)
        form=self.form_class(request.POST, instance=self.object)
        formset=self.formset_class(request.POST, request.FILES,instance=self.object)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            # if request.FILES:
            #     for ff in files:
            #         ff.delete()

            #     for i, value in enumerate(request.FILES.keys()):
            #         for afile in request.FILES.getlist(value):
            #             f=OrdenPagoFile(file=afile,orden_pago=orden)
            #             f.save()

            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrdenPagoEnviadoUpdate(OrdenPagoUpdate):
    form_class=OrdenPagoFormEnviado
    template_name="orden_pago/ordenpago_editar_1.html"


class OrdenPagoAprobadoUpdate(OrdenPagoUpdate):
    form_class=OrdenPagoFormAprobado
    template_name="orden_pago/ordenpago_editar_2.html"

class OrdenPagoPagadoUpdate(OrdenPagoUpdate):
    form_class=OrdenPagoFormPagado
    template_name="orden_pago/ordenpago_editar_2.html"


class OrdenPagoAprobarUpdate(OrdenPagoUpdate):
    form_class=OrdenPagoForm
    template_name="orden_pago/ordenpago_autorizar.html"
    success_url=reverse_lazy('pendiente_aprobacion')

class OrdenPagoDelete(DeleteView):
    model = OrdenPago
    template_name = 'orden_pago/ordenpago_eliminar.html'
    success_url = reverse_lazy('orden_pago_lista')
    form_class = OrdenPagoForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = "Anulado"
        motivo = dict(request.POST).get("motivo_anular")[0]
        fanulado = dict(request.POST).get("fecha_anulado")[0]
        self.object.motivo_anular = motivo
        self.object.fecha_anulado = fanulado
        self.object.save()
        return redirect(self.get_success_url())


def ordenpago_conf_elim(request):
    orden_id = request.GET.get('pk')
    orden = OrdenPago.objects.get(id=orden_id)
    form = OrdenPagoForm(instance=orden)
    return render(request, "orden_pago/ordenpago_anular.html", {"object": orden, "form": form})

# def orden_pago_editar(request, pk):
# 	if(request.method == 'POST'):
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoForm(request.POST, instance=p)
# 		if(form.is_valid()):
# 			form.save()
# 			return redirect('orden_pago_lista')
# 	else:
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoForm(instance=p)
# 	return render(request, 'orden_pago/ordenpago_editar_1.html', {'form': form})


# def orden_pago_editarAUTR_analista(request, pk):
# 	if(request.method == 'POST'):
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoEditarSecondForm(request.POST, instance=p)
# 		if(form.is_valid()):
# 			form.save()
# 			return redirect('orden_pago_lista')
# 	else:
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoEditarSecondForm(instance=p)
# 	return render(request, 'orden_pago/ordenpago_editar_1.html', {'form': form})


# def orden_pago_editarAUTR(request, pk):
# 	if(request.method == 'POST'):
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoEditarSecondForm(request.POST, instance=p)
# 		if(form.is_valid()):
# 			form.save()
# 			return redirect('pendiente_aprobacion')
# 	else:
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoEditarSecondForm(instance=p)
# 	return render(request, 'orden_pago/ordenpago_autorizar.html', {'form': form, "p":p})

# def orden_pago_editarPOST_AUTR(request, pk):
# 	if(request.method == 'POST'):
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoEditarThirdForm(request.POST, request.FILES, instance=p)
# 		if(form.is_valid()):
# 			form.save()
# 			p = get_object_or_404(OrdenPago, pk=pk)
# 			p.estado = 'PGDO'
# 			p.save()
# 			return redirect('orden_pago_lista')
# 	else:
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoEditarThirdForm(instance=p)
# 	return render(request, 'orden_pago/ordenpago_editar_2.html', {'form': form})

# def orden_pago_editarPGDO(request, pk):
# 	if(request.method == 'POST'):
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoEditarFinalForm(request.POST, instance=p)
# 		if(form.is_valid()):
# 			form.save()
# 			return redirect('orden_pago_lista')
# 	else:
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoEditarFinalForm(instance=p)
# 	return render(request, 'orden_pago/ordenpago_editar_2.html', {'form': form, "p":p})


# def orden_pago_enviar(request, pk):
# 	p = get_object_or_404(OrdenPago, cod_ord_pago=pk)
# 	p.estado = 'ENVD'
# 	p.save()
# 	return redirect('orden_pago_lista')


# def orden_pago_autorizar(request, pk):
# 	p = get_object_or_404(OrdenPago, cod_ord_pago=pk)
# 	p.estado = 'AUTR'
# 	p.save()
# 	return redirect('pendiente_aprobacion')


# def orden_pago_anular(request, pk=None):
# 	if(request.method == "POST"):
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoForm(request.POST,instance=p)
# 		if(form.is_valid()):
# 			form.instance.estado = 'ANLD'
# 			form.save()
# 		return redirect('orden_pago_lista')
# 	else:
# 		pk = request.GET.get('pk')
# 		p = get_object_or_404(OrdenPago, pk=pk)
# 		form = OrdenPagoForm(instance=p)
# 		return render(request, 'orden_pago/ordenpago_anular.html', {'object':p, 'form':form})


