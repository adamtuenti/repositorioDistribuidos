from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,JsonResponse
from django.views.generic import CreateView,UpdateView,DeleteView
from .models import OrdenIngreso
from .forms import OrdenIngresoForm, OrdenIngresoUpdateForm, OrdenIngresoPrintForm, FileFormset
from django.urls import reverse_lazy
from datetime import date,datetime
from financiero.orden_facturacion.models import OrdenFacturacion
from django.db import transaction
# Create your views here.



class OrdenIngresoCreate(CreateView):
    model=OrdenIngreso
    form_class=OrdenIngresoForm
    template_name='ordenIngreso_form.html'
    success_url=reverse_lazy('ordenIngreso')
    def get_initial(self):
        initial = super(OrdenIngresoCreate, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        try:
            datos = OrdenFacturacion.objects.get(pk=self.kwargs.get('pk'))
            
            if(datos!=None):
                initial["ruc_ci"]=datos.ruc_ci
                initial["orden_facturacion"] = datos.id
                initial["tipo_cliente"]="Natural"
        except:
            pass
        return initial
    
    def get_context_data(self, **kwargs):
        context=super(OrdenIngresoCreate,self).get_context_data(**kwargs)
        context['formset'] = FileFormset()
        return context
        
    def post(self, request,*args,**kwargs):
        self.object =self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            obj=(form.instance.orden_facturacion)
            obj.valor_pendiente-=form.instance.valor;
            if(obj.valor_pendiente==0):
                obj.estado='CNCL'
            obj.save()
            self.form_class.genera_codigo(form)
            form.instance.saldo_facturacion = obj.valor_pendiente
            self.object = form.save()
            
            titles = FileFormset(self.request.POST,self.request.FILES)
            if titles.is_valid():
                
                
                titles.instance = self.object
                titles.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
            
    # def get_success_url(self, **kwargs):         
    #         return reverse_lazy('ordenIngreso')
   
        

class OrdenIngresoUpdate(UpdateView):
    
    model=OrdenIngreso
    form_class=OrdenIngresoUpdateForm
    template_name='ordenIngreso_editar.html'
    success_url=reverse_lazy('ordenIngreso')
    def get_context_data(self, **kwargs):
        context = super(OrdenIngresoUpdate, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        if self.request.POST:
            context['formset'] = FileFormset(self.request.POST,self.request.FILES, instance=self.object)
        else:
            context['formset'] =FileFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(OrdenIngresoUpdate, self).form_valid(form)
    

class OrdenIngresoPrint(UpdateView):
    model=OrdenIngreso
    form_class=OrdenIngresoPrintForm
    success_url=reverse_lazy('ordenIngreso')

class OrdenIngresoDelete(DeleteView):
    model=OrdenIngreso
    template_name='ordenIngreso_eliminar.html'
    success_url=reverse_lazy('ordenIngreso')
    def post(self, request, *args, **kwargs):
        
        self.object=self.get_object()
        self.object.estado="ANLD" 
        self.object.fecha_anulacion = datetime.now().strftime('%Y-%m-%d')
        orden_facturacion = OrdenFacturacion.objects.get(pk= self.object.orden_facturacion.pk)
        print(orden_facturacion.valor_pendiente)
        orden_facturacion.valor_pendiente = orden_facturacion.valor_pendiente + self.object.valor
        print(orden_facturacion.valor_pendiente)
            
        if(orden_facturacion.estado == "CNCL"):
            orden_facturacion.estado = "PNDP"
        if(orden_facturacion.valor_pendiente == 0):
            orden_facturacion.estado = "CNCL"
        orden_facturacion.save()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    

def orden_ing_conf_elim(request):
    orden_id=request.GET.get('pk')

    orden=OrdenIngreso.objects.get(id=orden_id)

    return render(request,"ordenIngreso_eliminar.html",{"ordenIngreso":orden})

def load_orden_facturacion(request):
    ordenes = OrdenFacturacion.objects.all()
    opciones=render_to_string("dropdown_orden_facturacion.html",{"orden_facturacion":ordenes})
    return JsonResponse({'ordenes_facturacion': opciones})
        