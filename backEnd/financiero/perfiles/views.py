from django.shortcuts import render, redirect
from financiero.presupuestos.models import PresupuestoEvento
from financiero.plan_anual_compras.models import PlanAnualCompras

from financiero.orden_facturacion.models import OrdenFacturacion
from financiero.orden_pago.models import OrdenPago
from financiero.procesos_especiales.models import CambioEvento
from financiero.presupuestos_anuales.models import Espoltech, Fundespol
from financiero.procesos_especiales.models import ProcesoEspecial
from django.http import JsonResponse, HttpResponseRedirect


# Create your views here.

def index(request):
	return render(request, 'perfiles_index.html')

def index_analista(request):
	return render(request, 'base_analista.html')

def index_coordinador(request):
	return render(request, 'base_coordinador.html')

def por_aprobar(request):
	presupuestos_ev = PresupuestoEvento.objects.filter(estado='Solicitud Enviada').order_by("-codigo","-version")
	pac = PlanAnualCompras.objects.filter(estado='Solicitud Enviada').order_by("año")
	orden_fact=OrdenFacturacion.objects.filter(estado='SLCE')
	orden_pago = OrdenPago.objects.filter(estado='Enviado').order_by("-id")
	presupuestos_an = Espoltech.objects.filter(estado='ENVD')
	presupuestos_an_fundespol = Fundespol.objects.filter(estado='ENVD')
	proceso_especial = ProcesoEspecial.objects.filter(estado='SOLI')
	return render(request, 'por_aprobar.html', {"presupuestos_ev":presupuestos_ev, "orden_fact":orden_fact, "orden_pago":orden_pago, "presupuestos_an":presupuestos_an,
		 "presupuestos_an_fundespol":presupuestos_an_fundespol,"pac":pac,"proceso":proceso_especial})

def aprobar_orden_fact(request, pk):
	orden=OrdenFacturacion.objects.get(pk=pk)
	orden.estado="ACPF"
	orden.save()
	return HttpResponseRedirect("/financiero/perfiles/pendiente_aprobacion/")

def anular_orden_fact(request, pk):
	orden=OrdenFacturacion.objects.get(pk=pk)
	orden.estado="ANLD"
	orden.save()
	return HttpResponseRedirect("/financiero/perfiles/pendiente_aprobacion/")

