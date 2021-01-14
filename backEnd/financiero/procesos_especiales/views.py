
from django.shortcuts import render, redirect, render_to_response
from .filters import ProcesoEspecialFilter
from .forms import CambiarParticipanteCreateForm, CambiarEventoCreateForm, ProcesoEspecialUpdateForm, ParticipanteIntermedioFormset, ProcesoEspecialAutorizar, FileFormset, EventoDestinoFormset
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from ventas.personas_naturales.models import Persona_Natural
from financiero.orden_facturacion.models import OrdenFacturacionParticipante
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import ProcesoEspecial, ParticipanteIntermedio, ProcesoParticipante
from academico.evento.models import *
from financiero.presupuestos.models import PresupuestoEvento
from django.forms.models import model_to_dict
from ventas.personas_naturales.models import Persona_Natural
from datetime import date, datetime
from django import forms
from django.db import transaction
import json
from django.core.paginator import Paginator
from datetime import date
from academico.participante.models import *

# Create your views here.


def index(request):
    # ProcesoEspecial.objects.all().delete()
    # ProcesoParticipante.objects.all().delete()
    # ProcesoEspecialFile.objects.all().delete()
    # ParticipanteIntermedio.objects.get(id=32).delete()

    procesolista = ProcesoEspecial.objects.all().order_by('cod_proceso')
    participante = ProcesoParticipante.objects.all()
    # Filter
    filter = ProcesoEspecialFilter(request.GET, queryset=procesolista)
    # Paginator
    paginator = Paginator(filter.qs, 1000000)
    page = request.GET.get('page')
    procesoe = paginator.get_page(page)
    return render(request, "procesos_especiales/procesos_especiales_index.html", {"filter": filter, "proceso": filter.qs})



def cambiarParticipante(request):
    form = CambiarParticipanteCreateForm()
    return render(request, "CambioParticipante.html", {'form': form})


def cambiarParticipanteCreate(request):
    form_participante = CambiarParticipanteCreateForm(
        request.POST, request.FILES)
    if(request.method == "POST"):
        form_participante = CambiarParticipanteCreateForm(request.POST)
        if(form_participante.is_valid()):
            try:
                cod2 = str(int(ProcesoEspecial.objects.latest('pk').pk+1))
                codDeb = '0'*(4-len(cod2))+cod2
            except ProcesoEspecial.DoesNotExist:
                codDeb = "0001"
            conceptoDeb = "Eliminación de registro del participante "+form_participante.cleaned_data.get(
                "participante_origen_nombre") + " del evento " + form_participante.cleaned_data.get("codigo_evento")
            persona = Persona_Natural.objects.filter(
                cedula=form_participante.cleaned_data.get("participante_origen_cedula")).first()
            partint = ParticipanteIntermedio.objects.filter(
                cod_evento=form_participante.cleaned_data.get("codigo_evento"), participante=persona).first()
            desc = round((partint.descuento*partint.valor_evento)/100, 2)
            procesoDebito = ProcesoEspecial(cod_proceso=codDeb, concepto=conceptoDeb, fecha_emision=date.today(
            ), tipo_nota="Débito", categoria="Part", subtotal=partint.valor_evento, descuento_fact=partint.descuento, descuento_total=desc, valor_total=partint.valor)
            procesoDebito.save()
            conceptoCre = "Registro del participante "+form_participante.cleaned_data.get("participante_destino_nombre")+" al evento "+form_participante.cleaned_data.get(
                "codigo_evento")+" en remplazo del participante "+form_participante.cleaned_data.get("participante_origen_nombre")
            cod3 = str(int(ProcesoEspecial.objects.latest('pk').pk+1))
            codCre = '0'*(4-len(cod3))+cod3
            procesoCredito = ProcesoEspecial(cod_proceso=codCre, concepto=conceptoCre, fecha_emision=date.today(
            ), tipo_nota="Crédito", categoria="Part", subtotal=partint.valor_evento, descuento_fact=partint.descuento, descuento_total=desc, valor_total=partint.valor)
            procesoCredito.save()
            partOG = ProcesoParticipante(participante=persona, nombre_evento=form_participante.cleaned_data.get("nombre_evento"), cod_evento=form_participante.cleaned_data.get(
                "codigo_evento"), valor_evento=partint.valor_evento, descuento=partint.descuento, valor=partint.valor, proceso=procesoDebito,orden=partint.orden)
            partOG.save()
            persona2 = Persona_Natural.objects.filter(
                cedula=form_participante.cleaned_data.get("participante_destino_cedula")).first()
            partDest = ProcesoParticipante(participante=persona2, nombre_evento=form_participante.cleaned_data.get("nombre_evento"), cod_evento=form_participante.cleaned_data.get(
                "codigo_evento"), valor_evento=partint.valor_evento, descuento=partint.descuento, valor=partint.valor, proceso=procesoCredito,orden=partint.orden)
            partDest.save()
            return HttpResponseRedirect(reverse_lazy("procesos_especiales_index"))
        return render_to_response("CambioParticipante.html", {'form': form_participante}, status=500)


def load_eventos(request):
    tipo = request.GET.get("tipo")
    eventoslist=None
    if tipo=="Part":
        participantes = ParticipanteIntermedio.objects.all().distinct("cod_evento")
        listaEstados = ["Programado", "Reprogramado", "Activo"]
        listae = []
        for p in participantes:
            listae.append(p.cod_evento)
        eventos = Evento.objects.filter(
            codigo_evento__in=listae, estado__in=listaEstados)
        eventoslist = render_to_string(
            "dropdown_evento.html", {"eventos": eventos})
    elif tipo=="Event":
        listaEstados = ["Programado", "Reprogramado", "Activo"]
        presupuesto=PresupuestoEvento.objects.filter(evento__estado__in=listaEstados)
        eventoslist = render_to_string("dropdown_PreEventcod.html", {
                              "presupuestos": presupuesto})
    elif tipo=="Dev":
        listaEstados = ["Ejecutado", "Activo", "Programado","Reprogramado","No ejecutado"]
        ev=PresupuestoEvento.objects.filter(evento__estado__in=listaEstados)
        listaC=[]
        for e in ev:
            if e.evento.estado=="Ejecutado" or e.evento.estado=="No ejecutado" or e.evento.estado=="Programado":
                fechaIn=e.evento.fecha_fin
                delta = datetime.now().date() - fechaIn
                if delta.days<=366:
                    listaC.append(e.evento.codigo_evento)
            else:
                listaC.append(e.evento.codigo_evento)
        eventos=Evento.objects.filter(codigo_evento__in=listaC)
        eventoslist = render_to_string("dropdown_evento.html", {"eventos": eventos})
    elif tipo=="Grat":
        listaEstados = ["Ejecución", "Activo", "Programado","Reprogramado"]
        presupuesto=PresupuestoEvento.objects.filter(evento__estado__in=listaEstados)
        eventoslist = render_to_string("dropdown_PreEventcod.html", {
                              "presupuestos": presupuesto})
    return JsonResponse({'eventos': eventoslist})


def load_eventosInd(request):
    codigo = request.GET.get("codigo")
    evento = Evento.objects.filter(codigo_evento=codigo).first()
    presupuesto = PresupuestoEvento.objects.filter(evento=evento).first()
    return JsonResponse({'evento': model_to_dict(evento), 'valor': presupuesto.ingreso_neto_individual})


def load_naturales_no_evento(request):
    codigo = request.GET.get("codigo")
    identificacion = []
    razon_nombre = []
    participante = ParticipanteIntermedio.objects.filter(cod_evento=codigo)
    listap = []
    for p in participante:
        listap.append(p.participante.cedula)
    naturales = Persona_Natural.objects.exclude(cedula__in=listap)
    identificacion = render_to_string(
        "dropdown_natci.html", {"personas": naturales})
    razon_nombre = render_to_string(
        "dropdown_natnombres.html", {"personas": naturales})
    return JsonResponse({'ruc_ci': identificacion, 'razon_nombre': razon_nombre})


def load_participantes_eventos(request):
    codigo = request.GET.get("codigo")
    identificacion = []
    razon_nombre = []
    part = []
    participante = None
    evento = Evento.objects.get(codigo_evento=codigo)
    # if evento.estado == "Activo":
    #     horaLimite = (int(evento.duracion)*20/100)
    #     horaEjecutadas = 0
    #     horasAsistidas = {}
    #     for parti in ParticipanteIntermedio.objects.filter(cod_evento=codigo):
    #         horasAsistidas[parti.participante.cedula]=0
    #     asistencia = Asistencia.objects.filter(evento=evento)
    #     for a in asistencia:
    #         horario = CalendarioEvento.objects.get(
    #             fecha=a.fecha, evento=evento)
    #         horaInicio = horario.hora_inicio
    #         horaFin = horario.hora_fin
    #         deltaBeta = datetime.combine(date.today(), horaFin) - datetime.combine(date.today(), horaInicio)
    #         delta = deltaBeta.days * 24 + deltaBeta.seconds / 3600.0
            
    #         horaEjecutadas = horaEjecutadas+delta
    #         for p in a.registro:
    #             ced = p["participante_id"]
    #             partM=Participante.objects.get(pk=int(ced))
    #             cedpartM=partM.identificacion

    #             if cedpartM in horasAsistidas.keys():
    #                 if p["is_presente"]:
    #                     horasAsistidas[cedpartM] = horasAsistidas[cedpartM] + delta
    #             else:
    #                 if p["is_presente"]:
    #                     horasAsistidas[cedpartM] = delta
    #     if horaEjecutadas <= horaLimite:
    #         participante = ParticipanteIntermedio.objects.filter(
    #             cod_evento=codigo)
    #     else:
    #         for ced in horasAsistidas:
    #             if horasAsistidas[ced] <= horaLimite:
    #                 part.append(ced)
    #         personas = list(Persona_Natural.objects.filter(cedula__in=part))
    #         if len(personas)==0:
    #             participante = ParticipanteIntermedio.objects.filter(
    #                     cod_evento=codigo)
    #         else:
    #             participante = ParticipanteIntermedio.objects.filter(
    #                     cod_evento=codigo, participante__in=personas)
    # else:
    participante = ParticipanteIntermedio.objects.filter(cod_evento=codigo)
    identificacion = render_to_string(
        "dropdown_ci_CP.html", {"participante": participante})
    razon_nombre = render_to_string("dropdown_nombre_CP.html", {
                                    "participante": participante})
    return JsonResponse({'ruc_ci': identificacion, 'razon_nombre': razon_nombre})


def cambiarEventorender(request):
    form = CambiarEventoCreateForm()
    eventoFS = EventoDestinoFormset()
    return render(request, "cambioEvento.html", {'form': form, "eventoFS": eventoFS})


def cambiarEventoCreate(request):
    form_evento = CambiarEventoCreateForm(request.POST)
    eventos = EventoDestinoFormset(request.POST)
    if(request.method == "POST"):
        bandera = False
        for form in eventos:
            if form.is_valid():
                if form.cleaned_data.get("evento_destino_codigo") != None:
                    bandera = True
            if(form_evento.is_valid() and bandera):
                try:
                    cod2 = str(int(ProcesoEspecial.objects.latest('pk').pk+1))
                    codDeb = '0'*(4-len(cod2))+cod2
                except ProcesoEspecial.DoesNotExist:
                    codDeb = "0001"

                conceptoDeb = "Eliminación de registro del participante "+form_evento.cleaned_data.get(
                    "participante_nombre") + " del evento " + form_evento.cleaned_data.get("evento_origen_codigo")
                persona = Persona_Natural.objects.filter(
                    cedula=form_evento.cleaned_data.get("participante_cedula")).first()
                partint = ParticipanteIntermedio.objects.filter(cod_evento=form_evento.cleaned_data.get(
                    "evento_origen_codigo"), participante=persona).first()
                desc = round((partint.descuento*partint.valor_evento)/100, 2)
                procesoDebito = ProcesoEspecial(cod_proceso=codDeb, concepto=conceptoDeb, fecha_emision=date.today(
                ), tipo_nota="Débito", categoria="Event", subtotal=partint.valor_evento, descuento_fact=partint.descuento, descuento_total=desc, valor_total=partint.valor)
                procesoDebito.save()

                partOG = ProcesoParticipante(participante=persona, nombre_evento=form_evento.cleaned_data.get("evento_origen_nombre"), cod_evento=form_evento.cleaned_data.get(
                    "evento_origen_codigo"), valor_evento=partint.valor_evento, descuento=partint.descuento, valor=partint.valor, proceso=procesoDebito,orden=partint.orden)
                partOG.save()

                conceptoCre = "Registro del participante " + \
                    form_evento.cleaned_data.get(
                        "participante_nombre")+" al evento "
                subtotal = 0
                total = 0
                descuentoN = 0
                if eventos.is_valid():
                    for form in eventos:
                        if form.cleaned_data.get("evento_destino_codigo") != None:
                            conceptoCre = conceptoCre + \
                                form.cleaned_data.get(
                                    "evento_destino_codigo")+","
                            subtotal = subtotal + \
                                float(form.cleaned_data.get(
                                    "evento_destino_valor"))
                            descuentoN = descuentoN + \
                                round(
                                    (partint.descuento*float(form.cleaned_data.get("evento_destino_valor")))/100, 2)
                            total = total + \
                                float(form.cleaned_data.get(
                                    "evento_destino_valor"))-descuentoN
                descuentoP = round((100*total)/subtotal, 2)
                cod3 = str(int(ProcesoEspecial.objects.latest('pk').pk+1))
                codCre = '0'*(4-len(cod3))+cod3
                #Linea para quitar la ultima coma
                print("momazo antes de quitar el caaracter")
                conceptoCreF=conceptoCre[:-1]
                print("momazo despues de quitar el caaracter")
                print(conceptoCreF)
                procesoCredito = ProcesoEspecial(cod_proceso=codCre, concepto=conceptoCreF, fecha_emision=date.today(
                ), tipo_nota="Crédito", categoria="Event", subtotal=subtotal, descuento_fact=descuentoP, descuento_total=descuentoN, valor_total=total)
                procesoCredito.save()
                if eventos.is_valid():
                    for form in eventos:
                        if form.cleaned_data.get("evento_destino_codigo") != None:
                            t = float(form.cleaned_data.get("evento_destino_valor"))-(
                                (float(form.cleaned_data.get("evento_destino_valor"))*partint.descuento)/100)
                            partDest = ProcesoParticipante(participante=persona, nombre_evento=form.cleaned_data.get("evento_destino_nombre"), cod_evento=form.cleaned_data.get(
                                "evento_destino_codigo"), valor_evento=float(form.cleaned_data.get("evento_destino_valor")), descuento=partint.descuento, valor=t, proceso=procesoCredito,orden=partint.orden)
                            partDest.save()
                return HttpResponseRedirect(reverse_lazy("procesos_especiales_index"))
        return render_to_response("cambioEvento.html", {'form': form_evento, "eventoFS": eventos}, status=500)


def load_participantes_todos(request):
    identificacion = []
    razon_nombre = []
    participante = ParticipanteIntermedio.objects.distinct('participante')

    identificacion = render_to_string(
        "dropdown_ci_CP.html", {"participante": participante})
    razon_nombre = render_to_string("dropdown_nombre_CP.html", {
                                    "participante": participante})
    return JsonResponse({'ruc_ci': identificacion, 'razon_nombre': razon_nombre})


def load_eventos_participantes(request):
    cedula = request.GET.get("cedula")
    codigo=[]
    nombre=[]
    listaC=[]
    persona=Persona_Natural.objects.get(cedula=cedula)
    participanteEV=ParticipanteIntermedio.objects.filter(participante=persona)
    for part in participanteEV:
        listaC.append(part.cod_evento)
    listaEstados=["Programado","Activo","Reprogramado"]
    eventos=Evento.objects.filter(estado__in=listaEstados,codigo_evento__in=listaC)
    codigo=render_to_string("dropdown_codigoEvent.html",{"eventos":eventos})
    nombre=render_to_string("dropdown_nombreEvent.html",{"eventos":eventos})
    return JsonResponse({'cod': codigo, 'nom': nombre})



def load_eventosNo_participantes(request):
    cedula = request.GET.get("cedula")
    codigo = []
    nombre = []
    eventos = []
    persona = Persona_Natural.objects.get(cedula=cedula)
    part = ParticipanteIntermedio.objects.filter(participante=persona)
    for p in part:
        eventos.append(p.cod_evento)
    events = list(Evento.objects.exclude(codigo_evento__in=eventos))
    listaEstados=["Programado","Activo","Reprogramado"]
    presupuesto=PresupuestoEvento.objects.filter(evento__in=events,evento__estado__in=listaEstados)
    codigo = render_to_string("dropdown_PreEventcod.html", {
                              "presupuestos": presupuesto})
    nombre = render_to_string("dropdown_PreEventnom.html", {
                              "presupuestos": presupuesto})
    return JsonResponse({'cod': codigo, 'nom': nombre})


class ProcesoEspecialUpdate(UpdateView):
    model = ProcesoEspecial
    form_class = ProcesoEspecialUpdateForm
    template_name = 'ProcesoEspecialEditar.html'
    success_url = reverse_lazy('procesos_especiales_index')

    def get_context_data(self, **kwargs):
        data = super(ProcesoEspecialUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['participantesPE'] = ParticipanteIntermedioFormset(
                self.request.POST, instance=self.object)
            data['formset'] = FileFormset(
                self.request.POST, self.request.FILES, instance=self.object)

        else:
            data['participantesPE'] = ParticipanteIntermedioFormset(
                instance=self.object)
            data['formset'] = FileFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        participantes = context['participantesPE']
        archivos = context['formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if participantes.is_valid():
                participantes.instance = self.object
                participantes.save()
            if archivos.is_valid():
                archivos.instance = self.object
                archivos.save()
        return super(ProcesoEspecialUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('procesos_especiales_index')


def cambiarEvento(request):
    codigo = request.GET.get("codigo")
    print(codigo)
    valor = request.GET.get("valor")
    print(valor)
    tipo = request.GET.get("tipo")
    print(tipo)
    participantes=None
    if tipo=="Dev":
        # evento = Evento.objects.get(codigo_evento=codigo)
        # horaLimite = (int(evento.duracion)*20/100)
        # part = []
        # horasAsistidas = {}
        # for parti in ParticipanteIntermedio.objects.filter(cod_evento=codigo):
        #     horasAsistidas[parti.participante.cedula]=0
        # asistencia = Asistencia.objects.filter(evento=evento)
        # for a in asistencia:
        #     horario = CalendarioEvento.objects.get(
        #         fecha=a.fecha, evento=evento)
        #     horaInicio = horario.hora_inicio
        #     horaFin = horario.hora_fin
        #     deltaBeta = datetime.combine(date.today(), horaFin) - datetime.combine(date.today(), horaInicio)
        #     delta = deltaBeta.days * 24 + deltaBeta.seconds / 3600.0
        #     for p in a.registro:
        #         ced = p["participante_id"]
        #         partM=Participante.objects.get(pk=int(ced))
        #         cedpartM=partM.identificacion

        #         if cedpartM in horasAsistidas.keys():
        #             if p["is_presente"]:
        #                 horasAsistidas[cedpartM] = horasAsistidas[cedpartM] + delta
        #         else:
        #             if p["is_presente"]:
        #                 horasAsistidas[cedpartM] = delta
        # for ced in horasAsistidas:
        #     if horasAsistidas[ced] <= horaLimite:
        #         part.append(ced)
        # personas = list(Persona_Natural.objects.filter(cedula__in=part))
        # if len(personas)==0:
            participantes = ParticipanteIntermedio.objects.filter(
                     cod_evento=codigo)
        # else:
        # participantes = ParticipanteIntermedio.objects.filter(
        #             cod_evento=codigo, participante__in=personas)
    elif tipo=="Event":
        participantes = ParticipanteIntermedio.objects.filter(cod_evento=codigo)
    elif tipo=="Part":
        evento = Evento.objects.get(codigo_evento=codigo)
        identificacion = []
        razon_nombre = []
        part = []
        participantes = None
        if evento.estado == "Activo":
            horaLimite = (int(evento.duracion)*20/100)
            horaEjecutadas = 0
            horasAsistidas = {}
            asistencia = Asistencia.objects.filter(evento=evento)
            for a in asistencia:
                horario = CalendarioEvento.objects.get(
                    fecha=a.fecha, evento=evento)
                horaInicio = horario.hora_inicio
                horaFin = horario.hora_fin
                deltaBeta = datetime.combine(date.today(), horaFin) - datetime.combine(date.today(), horaInicio)
                delta = deltaBeta.days * 24 + deltaBeta.seconds / 3600.0
                
                horaEjecutadas = horaEjecutadas+delta
                for p in a.registro:
                    ced = p["participante_id"]
                    partM=Participante.objects.get(pk=int(ced))
                    cedpartM=partM.identificacion

                    if cedpartM in horasAsistidas.keys():
                        if p["is_presente"]:
                            horasAsistidas[cedpartM] = horasAsistidas[cedpartM] + delta
                    else:
                        if p["is_presente"]:
                            horasAsistidas[cedpartM] = delta
            if horaEjecutadas <= horaLimite:
                participantes = ParticipanteIntermedio.objects.filter(
                    cod_evento=codigo)
            else:
                for ced in horasAsistidas:
                    if horasAsistidas[ced] <= horaLimite:
                        part.append(ced)
                personas = list(Persona_Natural.objects.filter(cedula__in=part))
                if len(personas)==0:
                    participantes = ParticipanteIntermedio.objects.filter(
                            cod_evento=codigo)
                else:
                    participantes = ParticipanteIntermedio.objects.filter(
                            cod_evento=codigo, participante__in=personas)
        else:
            participantes = ParticipanteIntermedio.objects.filter(cod_evento=codigo)
            print("sem")
    return render(request, "participantes.html", {'cod': codigo, 'val': valor, 'participantes': participantes})


def load_participantes_list(request):
    lista = json.loads(request.GET.get("lista"))
    personas = list(Persona_Natural.objects.filter(cedula__in=lista['lista']))
    participantes = ParticipanteIntermedio.objects.filter(
        cod_evento=lista['codigo'], participante__in=personas)
    return JsonResponse({'participantes': list(participantes.values())})


def agregarPersonaNatural(request):
    codigo = request.GET.get("codigo")
    participantes = ParticipanteIntermedio.objects.filter(
        cod_evento=codigo).distinct("participante")
    personas = []
    identificacion = []
    razon_nombre = []
    for part in participantes:
        personas.append(part.participante.cedula)
    personas = Persona_Natural.objects.exclude(cedula__in=personas)
    identificacion = render_to_string(
        "dropdown_natci.html", {"personas": personas})
    razon_nombre = render_to_string(
        "dropdown_natnombres.html", {"personas": personas})
    return JsonResponse({'cedula': identificacion, 'nombre': razon_nombre})


def agregarPersonaNaturalModal(request):
    codigo = request.GET.get("codigo")
    return render(request, "personas_naturales.html", {'cod': codigo})

def alertaPersonCuponGratis(request):
    codigo = request.GET.get("codigo")
    cedula = request.GET.get("cedula")
    nombre = request.GET.get("nombre")
    bandera=False
    evento=Evento.objects.get(codigo_evento=codigo)
    dis=evento.diseno
    evento= Evento.objects.filter(diseno=dis)
    listaC=[]
    for e in evento:
        listaC.append(e.codigo_evento)
    eventoPart= ParticipanteIntermedio.objects.filter(cod_evento__in=listaC,participante__cedula=cedula)
    if eventoPart.count()>0:
        bandera=True
    return JsonResponse({'alerta': bandera,'nombre':nombre})

def verificarAsistencia(request):
    codigo = request.GET.get("codigo")
    cedula = request.GET.get("cedula")
    nombre = request.GET.get("nombre")
    
    evento = Evento.objects.get(codigo_evento=codigo)
    horaLimite = (int(evento.duracion)*20/100)
    horasAsistidas = 0
    asistencia = Asistencia.objects.filter(evento=evento)
    bandera=None
    bandera2=None
    for a in asistencia:
        horario = CalendarioEvento.objects.get(
            fecha=a.fecha, evento=evento)
        horaInicio = horario.hora_inicio
        horaFin = horario.hora_fin
        deltaBeta = datetime.combine(date.today(), horaFin) - datetime.combine(date.today(), horaInicio)
        delta = deltaBeta.days * 24 + deltaBeta.seconds / 3600.0
        for p in a.registro:
            ced = p["participante_id"]
            partM=Participante.objects.get(pk=int(ced))
            cedpartM=partM.identificacion
            if cedpartM==cedula:
                if p["is_presente"]:
                    horasAsistidas= horasAsistidas + delta
    if horasAsistidas==0:
        bandera=False
        bandera2=False
    elif horasAsistidas <= horaLimite:
        bandera=True
    else :
        bandera2=True
    print(bandera)
    print(bandera2)
    return JsonResponse({'bandera': bandera,'nombre':nombre,'bandera2':bandera2})
    
def verificarAsistenciaCambPart(request):
    codigo = request.GET.get("codigo")
    cedula = request.GET.get("cedula")
    nombre = request.GET.get("nombre")
    
    evento = Evento.objects.get(codigo_evento=codigo)
    evEstado=evento.estado
    horaLimite = (int(evento.duracion)*20/100)
    horasAsistidas = 0
    asistencia = Asistencia.objects.filter(evento=evento)
    bandera=None
    bandera2=None
    for a in asistencia:
        horario = CalendarioEvento.objects.get(
            fecha=a.fecha, evento=evento)
        horaInicio = horario.hora_inicio
        horaFin = horario.hora_fin
        deltaBeta = datetime.combine(date.today(), horaFin) - datetime.combine(date.today(), horaInicio)
        delta = deltaBeta.days * 24 + deltaBeta.seconds / 3600.0
        for p in a.registro:
            ced = p["participante_id"]
            partM=Participante.objects.get(pk=int(ced))
            cedpartM=partM.identificacion
            if cedpartM==cedula:
                if p["is_presente"]:
                    horasAsistidas= horasAsistidas + delta
    if horasAsistidas==0 and evEstado=="Activo":
        bandera2=False
    elif horasAsistidas > horaLimite and evEstado=="Activo":
        bandera2=True
    print(bandera)
    print(bandera2)
    return JsonResponse({'nombre':nombre,'bandera2':bandera2})    

class CuponGratis(CreateView):
    model = ProcesoEspecial
    form_class = ProcesoEspecialUpdateForm
    template_name = 'ProcesoEspecialEditar.html'
    success_url = reverse_lazy('procesos_especiales_index')

    def get_context_data(self, **kwargs):
        data = super(CuponGratis, self).get_context_data(**kwargs)
        if self.request.POST:
            data['participantesPE'] = ParticipanteIntermedioFormset(
                self.request.POST)
            data['formset'] = FileFormset(
                self.request.POST, self.request.FILES)
        else:
            data['participantesPE'] = ParticipanteIntermedioFormset()
            data['formset'] = FileFormset()
            data['cat'] = "Grat"
        return data

    def form_valid(self, form):
        try:
            cod2 = str(int(ProcesoEspecial.objects.latest('pk').pk+1))
            codDeb = '0'*(4-len(cod2))+cod2
        except ProcesoEspecial.DoesNotExist:
            codDeb = "0001"
        form.instance.cod_proceso = codDeb
        context = self.get_context_data()
        participantes = context['participantesPE']
        archivos = context['formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if participantes.is_valid():
                participantes.instance = self.object
                participantes.save()
            if archivos.is_valid():
                archivos.instance = self.object
                archivos.save()
        return super(CuponGratis, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('procesos_especiales_index')


class Devolucion(CreateView):
    model = ProcesoEspecial
    form_class = ProcesoEspecialUpdateForm
    template_name = 'ProcesoEspecialEditar.html'
    success_url = reverse_lazy('procesos_especiales_index')

    def get_context_data(self, **kwargs):
        data = super(Devolucion, self).get_context_data(**kwargs)
        if self.request.POST:
            data['participantesPE'] = ParticipanteIntermedioFormset(
                self.request.POST)
            data['formset'] = FileFormset(
                self.request.POST, self.request.FILES)
        else:
            data['participantesPE'] = ParticipanteIntermedioFormset()
            data['formset'] = FileFormset()
            data['cat'] = "Dev"
        return data

    def form_valid(self, form):
        try:
            cod2 = str(int(ProcesoEspecial.objects.latest('pk').pk+1))
            codDeb = '0'*(4-len(cod2))+cod2
        except ProcesoEspecial.DoesNotExist:
            codDeb = "0001"
        form.instance.cod_proceso = codDeb
        context = self.get_context_data()
        participantes = context['participantesPE']
        archivos = context['formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if participantes.is_valid():
                participantes.instance = self.object
                participantes.save()
            if archivos.is_valid():
                archivos.instance = self.object
                archivos.save()
        return super(Devolucion, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('procesos_especiales_index')


class ProcesoEspecialAutorizar(UpdateView):
    model = ProcesoEspecial
    form_class = ProcesoEspecialAutorizar
    template_name = 'ProcesoEspecialAutorizar.html'
    success_url = reverse_lazy('financiero')

    def get_context_data(self, **kwargs):
        data = super(ProcesoEspecialAutorizar, self).get_context_data(**kwargs)
        if self.request.POST:
            data['participantesPE'] = ParticipanteIntermedioFormset(
                self.request.POST, instance=self.object)
            data['formset'] = FileFormset(
                self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['participantesPE'] = ParticipanteIntermedioFormset(
                instance=self.object)
            data['formset'] = FileFormset(instance=self.object)
            pk = self.kwargs.get('pk', 0)
            data['proceso'] = ProcesoEspecial.objects.get(id=pk)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        participantes = context['participantesPE']
        archivos = context['formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if participantes.is_valid():
                participantes.instance = self.object
                participantes.save()
            if archivos.is_valid():
                archivos.instance = self.object
                archivos.save()
        return super(ProcesoEspecialAutorizar, self).form_valid(form)


def aprobar_proceso_especial(request, pk):
    if(request.method == 'POST'):
        p = get_object_or_404(ProcesoEspecial, pk=pk)
        p.estado = "APRB"
        p.fecha_aprobacion = date.today()
        p.save()
        pp = ProcesoParticipante.objects.filter(proceso=p)
        if p.tipo_nota == "Débito":
            for propart in pp:
                pint = ParticipanteIntermedio.objects.get(
                    participante=propart.participante, cod_evento=propart.cod_evento)
                pint.delete()
        else:
            for propart in pp:
                evento=Evento.objects.get(codigo_evento=propart.cod_evento)
                pint = ParticipanteIntermedio(participante=propart.participante, cod_evento=propart.cod_evento,
                                              nombre_evento=propart.nombre_evento, valor_evento=propart.valor_evento, descuento=propart.descuento ,valor=propart.valor,evento=evento)
                pint.save()
        return redirect('pendiente_aprobacion')


def anular_proceso_especial(request, pk):
    if(request.method == 'POST'):
        p = get_object_or_404(ProcesoEspecial, pk=pk)
        p.estado = "ANLD"
        motivo = dict(request.POST).get("motivo")[0]
        p.motivo = motivo
        p.save()
        return redirect('pendiente_aprobacion')
