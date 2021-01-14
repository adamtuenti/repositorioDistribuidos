from django.shortcuts import render,  redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import OrdenFacturacion, Persona_Natural, Juridica, OrdenFacturacionParticipante, Contacto_natural
from .forms import OrdenFacturacionForm, OrdenFacturacionUpdateForm, OrdenFacturacionFinalForm, OrdenFacturacionParticipanteForm, FileForm, FileFormset
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect
from datetime import date
from django.views.decorators.csrf import ensure_csrf_cookie
from .filters import OrdenFacturacionFilter
from academico.evento.models import Evento
from financiero.presupuestos.models import PresupuestoEvento
from financiero.procesos_especiales.models import ParticipanteIntermedio, ProcesoParticipante
from seguridad.models import *
# Create your views here.

def index(request):
    if (request.GET.get('estado',None)!=None and 'ANLD' in request.GET['estado']):
        ordFac_lista = OrdenFacturacion.objects.all()
    else:
        ordFac_lista = OrdenFacturacion.objects.all().exclude(estado='ANLD')
    ordFac_filter = OrdenFacturacionFilter(request.GET, queryset=ordFac_lista)
    #ordFac_filter = OrdenFacturacionFilter(request.GET, queryset=OrdenFacturacion.objects.all())
    return render(request, "orden_facturacion.html", {"filter":ordFac_filter})

class OrdenFacturacionCreate(CreateView):
    model=OrdenFacturacion
    form_class=OrdenFacturacionForm
    template_name='orden_facturacion_nuevo.html'
    success_url=reverse_lazy('orden_facturacion')

    def form_valid(self, form):
        
        try:
            pre=str(int(self.model.objects.latest('pk').pk+1))
            sec='0'*(4-len(pre))+pre
        except self.model.DoesNotExist:
            sec='0001'      
        form.instance.cod_orden_fact=sec+'-'+str(date.today().year)
        form.instance.valor_pendiente = form.instance.valor_total
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('orden_facturacion_editar', args = (self.object.id,))

    """def get_context_data(self, **kwargs):
        context=super(OrdenFacturacionCreate,self).get_context_data(**kwargs)
        context['form']=self.form_class()
        context['formn']=self.pn_form_class()
        context['formj']=self.pj_form_class()

        return context"""

class OrdenFacturacionUpdate(UpdateView):
    model=OrdenFacturacion
    form_class=OrdenFacturacionUpdateForm
    second_form_class=OrdenFacturacionForm
    third_form_class=OrdenFacturacionFinalForm
    participantes_class=OrdenFacturacionParticipante
    template_name='orden_facturacion_editar.html'
    success_url=reverse_lazy('orden_facturacion')

    def get_context_data(self, **kwargs):
        context=super(OrdenFacturacionUpdate,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        orden=self.model.objects.get(id=pk)
        participantes=self.participantes_class.objects.filter(orden_id=pk)
        context['participantes'] = participantes
        context['orden_id']=pk
        if self.request.POST:
            if 'form' in context:
                if orden.estado=='ACTV':
                    context['form']=self.second_form_class(self.request.POST,instance=orden)
                elif orden.estado=='PNDP':
                    context['form']=self.third_form_class(self.request.POST,instance=orden)
                else:
                    context['form']=self.form_class(self.request.POST,instance=orden)
            context['formset'] = FileFormset(self.request.POST, self.request.FILES,instance=self.object)
        else:
            if 'form' in context:
                if orden.estado=='ACTV':
                    context['form']=self.second_form_class(instance=orden)
                elif orden.estado=='PNDP':
                    context['form']=self.third_form_class(instance=orden)
                else:
                    context['form']=self.form_class(instance=orden)
            context['formset'] = FileFormset(instance=orden)
        return context

    def form_valid(self, form):
        pk=self.kwargs.get('pk',0)
        orden=self.model.objects.get(id=pk)
        if not(form.instance.estado=="PNDP" or form.instance.estado=="CNCL" or form.instance.estado=="ACPF"):
            form.instance.valor_pendiente = form.instance.valor_total
        if orden.estado=='ACPF' or orden.estado=='PNDP':
            context = self.get_context_data()
            titles = context['formset']
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super().form_valid(form)

class OrdenFacturacionDelete(DeleteView):
    model=OrdenFacturacion
    template_name='orden_facturacion_eliminar.html'
    success_url=reverse_lazy('orden_facturacion')
    form_class=OrdenFacturacionForm
      

def orden_fact_conf_elim(request):
    orden_id=request.GET.get('pk')
    orden=OrdenFacturacion.objects.get(id=orden_id)
    form=OrdenFacturacionForm(instance=orden)
    return render(request,"orden_facturacion_eliminar.html",{"orden":orden,"form":form})



def cambiar_estado(request, pk):
    orden=OrdenFacturacion.objects.get(id=pk)
    orden.estado='SLCE'
    orden.save()
    return HttpResponseRedirect(reverse_lazy('orden_facturacion'))

def verificar_campos(request):
    return render(request,"orden_facturacion_confirmar.html")

def load_personas(request):
    persona = request.GET.get("persona")
    identificacion=[]
    razon_nombre=[]
    if persona=="Natural":
        personas=Persona_Natural.objects.all()
        identificacion=render_to_string("dropdown_natural_ciOF.html",{"personas":personas})
        razon_nombre=render_to_string("dropdown_natural_nombresOF.html",{"personas":personas})
    elif persona=="Jurídica":
        personas=Juridica.objects.all()
        identificacion=render_to_string("dropdown_juridica_rucOF.html",{"personas":personas})
        razon_nombre=render_to_string("dropdown_juridica_razonOF.html",{"personas":personas})
    return JsonResponse({'ruc_ci': identificacion, 'razon_nombre': razon_nombre})

def load_contactos(request):
    id = request.GET.get("id")
    contactos=Contacto_natural.objects.filter(empresa=id)
    
    listnatid=[]
    for c in contactos:
        listnatid.append(c.contacto.cedula)
        
    contactosN=Persona_Natural.objects.filter(cedula__in=listnatid)
    
    contlist=render_to_string("dropdown_contacto.html",{"contactos":contactosN})  
    return JsonResponse({'contacto': contlist})

def load_eventos(request):
    eventos=Evento.objects.all()
    eventoslist=render_to_string("dropdown_evento.html",{"eventos":eventos})  
    return JsonResponse({'eventos': eventoslist})

def load_eventoind(request):
    codigo = request.GET.get("codigo")
    evento=Evento.objects.filter(codigo_evento=codigo).first()
    presupuesto= PresupuestoEvento.objects.filter(evento=evento).first()
    if presupuesto!=None:
        return JsonResponse({'nombre': evento.nombre,'valor':presupuesto.ingreso_neto_individual})
    else :
        return JsonResponse({'nombre': evento.nombre})

def load_info(request):
    id = request.GET.get("id")
    persona= request.GET.get("persona")
    direccion=""
    telefono=""
    contacto=""
    sector=""
    tipo=""
    ##Para Natural
    email =""
    celular = ""
    cargo = ""
    nombres = ""
    apellidos = ""

    if id!="":
        if persona=="Natural":
            cliente=Persona_Natural.objects.get(pk=id)
            direccion=cliente.dir_domicilio
            telefono=cliente.tel_domicilio
            celular=cliente.celular
            email = cliente.email
            cargo = cliente.cargo
            nombres = cliente.nombres
            apellidos = cliente.apellidos
        elif persona=="Jurídica":
            cliente=Juridica.objects.get(ruc=id)
            #direccion= cliente.direccion
            #telefono= cliente.telefono
            sector= cliente.sector.nombre
            tipo= cliente.tipo_empresa.nombre

    return JsonResponse({'nombres':nombres,'apellidos':apellidos,'direccion': direccion, 'telefono': telefono, 'contacto': contacto, 'sector': sector, 'tipo': tipo,'email':email,'celular':celular,'cargo':cargo})

def load_info_veris(request):
    id = request.GET.get("id")
    persona= request.GET.get("persona")
    direccion=""
    telefono=""
    contacto=""
    sector=""
    tipo=""
    ##Para Natural
    email =""
    celular = ""
    cargo = ""

    if id!="":
        if persona=="Natural":
            cliente=Persona_Natural.objects.get(pk=id)
            direccion=cliente.dir_domicilio
            telefono=cliente.tel_domicilio
            celular=cliente.celular
            email = cliente.email
            cargo = cliente.cargo
        elif persona=="Jurídica":
            
            cliente=Juridica.objects.get(ruc=id)
            direccion= cliente.direccion
            telefono= cliente.telefono
            email= cliente.correo
            sector= cliente.sector.nombre
            tipo= cliente.tipo_empresa.nombre
    return JsonResponse({'direccion': direccion, 'telefono': telefono, 'contacto': contacto, 'sector': sector, 'tipo': tipo,'email':email,'celular':celular,'cargo':cargo})

def load_mail(request):
    cedula = request.GET.get("cedula")
    email=""
    if cedula!="":
        email=Persona_Natural.objects.get(cedula=cedula).email
    return JsonResponse({"email": email})

def load_usuarios_ventas(request):
    roles=RolPermisoUsuario.objects.filter(modulo="Comercial").values_list('usuario', flat=True)
    usuariosv=Usuario.objects.filter(pk__in=roles)
    asesores=render_to_string("dropdown_usuarios_ventas.html",{"usuariosv":usuariosv})  
    return JsonResponse({'asesores': asesores})

def load_info_ci(request):
    pk = request.GET.get("pk")
    ci=""
    if id!="":
        ci=OrdenFacturacion.objects.get(id=pk).ruc_ci
    return JsonResponse({'ci': ci})


class ParticipanteCreate(CreateView):
    model=OrdenFacturacionParticipante
    form_class=OrdenFacturacionParticipanteForm
    template_name='nuevo_participante.html'
    success_url='/financiero/orden_facturacion/editar'

    def get_context_data(self, **kwargs):
        context=super(ParticipanteCreate,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        context['orden_id']=pk
        context['orden_cod']=OrdenFacturacion.objects.get(pk=pk).cod_orden_fact
        return context

    def post(self, request,*args,**kwargs):
        self.object =self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            orden_id=kwargs['pk']
            p=form.save(commit=False)
            p.orden_id=orden_id
            p.save()
            orden=OrdenFacturacion.objects.get(pk=orden_id)
            if orden.estado=="ACPF" or orden.estado=="PNDP" or orden.estado=="CNCL":
                print("entro")
                lp=ParticipanteIntermedio.objects.filter(participante=p.participante,cod_evento=p.cod_evento)
                if len(lp)!=0:
                    pi=lp.first()
                    pi.orden=orden
                    pi.save()
                    pp=ProcesoParticipante.objects.filter(participante=pi.participante,cod_evento=pi.cod_evento).first()
                    pp.orden=orden
                    pp.save()
                valnuevo=orden.valor_pendiente+p.valor
                orden.valor_pendiente=valnuevo
                if valnuevo==0 and orden.estado=="PNDP":
                    orden.estado="CNCL"
                orden.save()
                participantesActualizar=OrdenFacturacionParticipante.objects.filter(orden=orden)
                subtotal=0
                total=0
                for partA in participantesActualizar:
                    subtotal=subtotal+partA.valor_evento
                    total=total+partA.valor
                descuento=100-(100*total)/subtotal
                descT=(subtotal*descuento)/100
                orden.subtotal=subtotal
                orden.descuento_fact=descuento
                orden.descuento_total=descT
                orden.valor_total=total
                print(subtotal)
                print(descuento)
                print(descT)
                print(total)
                orden.save()
                
            return HttpResponseRedirect(self.get_success_url()+'/'+str(orden_id))
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ParticipanteUpdate(UpdateView):
    model=OrdenFacturacionParticipante
    form_class=OrdenFacturacionParticipanteForm
    template_name='nuevo_participante.html'
    success_url='/financiero/orden_facturacion/editar'

    def get_context_data(self, **kwargs):
        context=super(ParticipanteUpdate,self).get_context_data(**kwargs)
        pk=self.kwargs.get('fk',0)
        context['orden_id']=pk
        context['orden_cod']=OrdenFacturacion.objects.get(pk=pk).cod_orden_fact
        
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        orden_id=kwargs['fk']
        pk=kwargs['pk']
        participante=self.model.objects.get(id=pk)
        form=self.form_class(request.POST, instance=participante)
        if form.is_valid():
            p=form.save(commit=False)
            p.orden_id=orden_id
            p.save()
            return HttpResponseRedirect(self.get_success_url()+'/'+str(orden_id))
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ParticipanteDelete(DeleteView):
    model=OrdenFacturacionParticipante
    form_class=OrdenFacturacionParticipanteForm
    template_name='eliminar_participante.html'
    success_url='/financiero/orden_facturacion/editar'

    """def get_context_data(self, **kwargs):
        context=super(ParticipanteDelete,self).get_context_data(**kwargs)
        fk=self.kwargs.get('fk',0)
        context['orden_id']=fk
        context['orden_cod']=OrdenFacturacion.objects.get(pk=fk).cod_orden_fact
        return context
"""
    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        orden_id=kwargs['fk']
        orden=OrdenFacturacion.objects.get(pk=orden_id)
        if orden.estado=="ACPF" or orden.estado=="PNDP" or orden.estado=="CNCL":
            valnuevo=orden.valor_pendiente-self.object.valor
            orden.valor_pendiente=valnuevo
            if valnuevo!=0 and orden.estado=="CNCL":
                orden.estado="PNDP"
            orden.save() 
        self.object.delete()

        if orden.estado=="ACPF" or orden.estado=="PNDP" or orden.estado=="CNCL":
            participantesActualizar=OrdenFacturacionParticipante.objects.filter(orden=orden)
            subtotal=0
            total=0
            for partA in participantesActualizar:
                subtotal=subtotal+partA.valor_evento
                total=total+partA.valor
            if subtotal!=0:
                descuento=100-(100*total)/subtotal
            else:
                descuento=0
            descT=(subtotal*descuento)/100
            orden.subtotal=subtotal
            orden.descuento_fact=descuento
            orden.descuento_total=descT
            orden.valor_total=total
            orden.save()
        #p_id=kwargs['pk']
        #p=OrdenFacturacionParticipante.objects.get(id=p_id)
        #p.delete()
        return HttpResponseRedirect(self.get_success_url()+'/'+str(orden_id))

def participante_conf_elim(request):
    p_id=request.GET.get('pk')
    orden_id=request.GET.get('fk')
    p=OrdenFacturacionParticipante.objects.get(id=p_id)
    return render(request,"eliminar_participante.html",{"p":p, "orden_id":orden_id})

def aprobar_orden_facturacion(request, pk):
    if(request.method == 'POST'):
        p = get_object_or_404(OrdenFacturacion, pk=pk)
        p.estado="ACPF"
        participantes= OrdenFacturacionParticipante.objects.filter(orden=p)
        for part in participantes:
            evento=Evento.objects.get(codigo_evento=part.cod_evento)
            pIntl=ParticipanteIntermedio.objects.filter(orden=None, participante=part.participante,cod_evento=part.cod_evento)
            if len(pIntl)!=0:
                pInt=pIntl.first()
                pInt.orden=p
                pInt.save()
                partpro=ProcesoParticipante.objects.get(participante=part.participante,cod_evento=part.cod_evento)
                partpro.orden=p
                partpro.save()
            else:
                newpart=ParticipanteIntermedio(participante=part.participante,nombre_evento=part.nombre_evento,cod_evento=part.cod_evento,valor_evento=part.valor_evento,descuento=part.descuento,valor=part.valor,orden=p,evento=evento)
                newpart.save()
        p.save()
        return redirect('pendiente_aprobacion')
    else:
        p = get_object_or_404(OrdenFacturacion, pk=pk)
        form = OrdenFacturacionFinalForm(instance=p)
        participantes=OrdenFacturacionParticipante.objects.filter(orden_id=pk)
        return render(request, 'orden_facturacion_aprobar.html', {'form': form, 'participantes':participantes, "orden":p})


def anular_orden_facturacion(request, pk):
    if(request.method == 'POST'):
        p = get_object_or_404(OrdenFacturacion, pk=pk)
        p.estado="ANLD"
        motivo=dict(request.POST).get("motivo_anular")[0]
        p.motivo_anular=motivo
        p.save()
        return redirect('pendiente_aprobacion')
    else:
        p = get_object_or_404(OrdenFacturacion, pk=pk)
        form = OrdenFacturacionFinalForm(instance=p)
        participantes=OrdenFacturacionParticipante.objects.filter(orden_id=pk)
        return render(request, 'orden_facturacion_aprobar.html', {'form': form, 'participantes':participantes, "orden":p})

def anular_orden_facturacionMenu(request, pk):
    if(request.method == 'POST'):
        p = get_object_or_404(OrdenFacturacion, pk=pk)
        p.estado="ANLD"
        motivo=dict(request.POST).get("motivo_anular")[0]
        p.motivo_anular=motivo
        p.save()
        return redirect('orden_facturacion')
    else:
        p = get_object_or_404(OrdenFacturacion, pk=pk)
        form = OrdenFacturacionFinalForm(instance=p)
        participantes=OrdenFacturacionParticipante.objects.filter(orden_id=pk)
        return render(request, 'orden_facturacion_aprobar.html', {'form': form, 'participantes':participantes, "orden":p})


def verificar_participante(request):
    codigo=request.GET.get('codigo')
    participantes=ParticipanteIntermedio.objects.filter(cod_evento=codigo).exclude(orden=None).values_list('participante', flat=True)
    personas=Persona_Natural.objects.exclude(cedula__in=participantes)
    participante=render_to_string("dropdown_participanteOF.html",{"personas":personas}) 
    return JsonResponse({'participantes': participante})

def verificar_participante_eliminacion_PROESP(request):
    cedula=request.GET.get('cedula')
    codigo=request.GET.get('codigo')
    participante=ParticipanteIntermedio.objects.get(cod_evento=codigo,participante__cedula=cedula)
    bandera=True
    if participante.orden==None:
        bandera=False
    return JsonResponse({'bandera': bandera,'cedula':cedula,'codigo':codigo})

