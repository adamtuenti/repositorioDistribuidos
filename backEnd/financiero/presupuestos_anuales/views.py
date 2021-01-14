from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from .forms import EspoltechForm, FundespolForm
from .models import Espoltech, Fundespol
from .filters import EspoltechFilter, FundespolFilter,RealFilter
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from datetime import date
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
#Modelos de financiero
from financiero.orden_facturacion.models import OrdenFacturacion
from financiero.orden_ingreso.models import OrdenIngreso
import datetime
import numpy as np
from financiero.orden_pago.models import OrdenPago,Egresos
# Create your views here.

def index(request):
	# presupuesto_lista = Espoltech.objects.filter(centro_costos='ESPOLTECH')
	# presupuesto_filter = EspoltechFilter(request.GET, queryset=presupuesto_lista)
	# presupuesto_lista_f = Espoltech.objects.filter(centro_costos='FUNDESPOL')
	# presupuesto_filter_f = EspoltechFilter(request.GET, queryset=presupuesto_lista_f)
	presupuestolista=Espoltech.objects.all().order_by('-num','año','centro_costos','version',)
	filter = RealFilter(request.GET, queryset=presupuestolista)
	#return render(request, "presupuestos_anuales/presupuestos_anuales_list.html", {"presupuestos_an":presupuesto_lista, "filter":presupuesto_filter, "presupuesto_an_f":presupuesto_lista_f, "filter_f":presupuesto_filter_f})
	return render(request, "presupuestos_anuales/presupuestos_anuales_list.html", {"filter":filter,"presupuesto":filter.qs})

# def prueba():
# 	pagosD={}
# 	egreso=Egresos.objects.all()
# 	for e in egreso:
# 		print(e.nombre +"/")
# 	pago=OrdenPago.objects.filter(estado="Pagado")
# 	for p in pago:
# 		if p.egreso.nombre in pagosD:
# 			pagosD[p.egreso.nombre]=pagosD[p.egreso.codigo]+p.total
# 		else :
# 			pagosD[p.egreso.nombre]=p.total
# 	print(pagosD)
# 	return pagosD

# ------------------ FUNCION DE OBTENER VALORES INGRESOS APORTACIONES ACTUALIZADOS---------------------------
def get_ingresos_aportaciones_update(year,centro_costos):
	pk = 1
	mult_tasa_general = 0.005
	mult_centro_ingresos = 0.07
	mult_espol_ingresos_part = 0.07 
	mult_participacion_unidad = 0.11
	if (centro_costos == "FUNDESPOL"):
		print("ERES FUNDESPOL")
		pk = 2
		mult_centro_ingresos = 0.045
		mult_espol_ingresos_part = 0.10 
		mult_participacion_unidad = 0.11
	
	#Query para obtener todas las ordenes de facturacion del año actual  que sean del centro_costo respectivo (FUNDESPOL tiene el pk=2 y ESPOLTECH tiene el pk= 1)
	totales_lista = OrdenFacturacion.objects.filter(fecha__year = year, centro_costos__pk = pk).values_list('valor_total', flat=True).exclude(estado= 'ANLD')
	#Query para obtener todas las ordenes de ingreso del año actual  con estado activa y cuyas ordenes de facturacion tengan el estado pendientes de cobto que sean del centro_costo respectivo (FUNDESPOL tiene el pk=2 y ESPOLTECH tiene el pk= 1)
	totales_ording = OrdenIngreso.objects.filter(fecha__year__lt = year, estado= 'ACTV', orden_facturacion__estado='PNDP', centro_costos__pk = pk ).values_list('valor', flat=True)
	for i in totales_lista:
		print(i)

	#Se convierten en un arreglo y se suman las ordenes de facturacion
	total_facturacion_actual = np.array(totales_lista).sum()
	#Se convierten en un arreglo y se suman las ordenes de ingreso 
	total_ording_actual = np.array(totales_ording).sum()
	#Gastos corrientes , tasas generales ESPOLTECH
	tasa_general = total_facturacion_actual * mult_tasa_general
	#Porcentajes de aportaciones de acuerdo a lineamientos FUNDESPOL
	fundespol_ingresos = total_facturacion_actual * mult_centro_ingresos
	espol_ingresos = total_facturacion_actual * mult_espol_ingresos_part
	participacion_unidad = total_facturacion_actual * mult_participacion_unidad
	
	return {
	"total_facturacion_actual":total_facturacion_actual,
	"total_ording_actual":total_ording_actual,
	"tasa_general":tasa_general,
	"centro_costo_ingresos":fundespol_ingresos,
	"participacion_ingresos_espol":espol_ingresos,
	"participacion_unidad":participacion_unidad
	}

# ------------------ FUNCIONES DE CREAR---------------------------


#VISTA PARA CREAR NUEVO PRESUPUESTO DE ESPOLTECH
def presupuestos_anuales_nuevo(request):
	dt = datetime.datetime.today()

	if(request.method == 'POST'):
		form = EspoltechForm(request.POST)
		try:
			num = Espoltech.objects.all().order_by('num').latest('num').num
			newnum= int(num)+1
			form.instance.num=newnum
			print("entro a siguiente")
		except Espoltech.DoesNotExist:
			newnum = 1
			form.instance.num=newnum
			print("entro a exception")
		
		if(form.is_valid()):
			form.save()
			return redirect("presupuesto_anual_lista")
	else:
		form = EspoltechForm(initial={'año':dt.year})
	return render(request, "presupuestos_anuales/espoltech_nuevo.html", {
		"form":form,
		"tipo":"ESPOLTECH"
		})

	# return render(request, "presupuestos_anuales/espoltech_nuevo.html", {
	# 	"form":form,
	# 	"ingreso_orden":diccionario["total_facturacion_actual"],
	# 	"ingreso_ording":diccionario["total_ording_actual"],
	# 	"tasa_general":diccionario["tasa_general"],
	# 	"espol_tech_ingresos":diccionario["centro_costo_ingresos"],
	# 	"participacion_espol":diccionario["participacion_ingresos_espol"],
	# 	"participacion_unidad":diccionario["participacion_unidad"],
	# 	"tipo":"ESPOLTECH"
	# 	})


def modal_actualizar(request):
	return render_to_response("presupuestos_anuales/actualizar_presupuesto_anual.html")



def casillasEjecutado_ingresos_aportaciones(request):
	centro=request.GET.get('centro')
	year=request.GET.get('year')
	diccionario = get_ingresos_aportaciones_update(year,centro)
	print(diccionario)
	return HttpResponse(json.dumps(diccionario, cls=DjangoJSONEncoder,ensure_ascii=False))
	

	
	
def casillasEjecutado(request):
	listIng=["Venta de Bienes y Servicios (Otros Servicios Técnicos y Especializados: análisis de laboratorio, ensayos, pruebas, etc)","Venta de Bienes y Servicios (Cursos, Seminarios y Maestrías)","Transferencia y Donaciones Corrientes Sector Público Provenientes del Gobierno Central","Transferencia y Donaciones Corrientes Sector Público Provenientes de Entidades Descentralizadas y Autónomas","Transferencia y Donaciones Corrientes Sector Público Provenientes de Empresas Públicas","Transferencia y Donaciones Corrientes Sector Público Provenientes de Gobiernos Autónomos Descentralizados","Otros no especificados","Saldos de Fondos de Autogestión (Saldos de los centros de costos. Cabe indicar que estos valores deberán ser modificados una vez cerrado el ejercicio fiscal 2019)","Cuentas por cobrar de años anteriores","Transferencia y Donaciones Capital e Inversión Sector Público  Provenientes del Gobierno Central","Transferencia y Donaciones Capital e Inversión Sector Público  Provenientes de Entidades Descentralizadas y Autónomas","Transferencia y Donaciones Capital e Inversión Sector Público Provenientes de Empresas Públicas","Transferencia y Donaciones Capital e Inversión Sector Público Provenientes de Gobiernos Autónomos Descentralizados","Donaciones Capital del Sector Externo Provenientes de Gobiernos y Organismos Gubernamentales"]
	pagosD={}
	pagosD["Impuesto al Valor Agregado (debe hacerse el cálculo estimadodel IVA de todos los gastos contemplados en el presente presupuesto, excepto los que gravan tarifa 0%)"]=0
	centro=request.GET.get('centro')
	year=request.GET.get('year')
	# print(centro)
	# print(year)
	# egreso=Egresos.objects.all()
	# for e in egreso:
	# 	print(e.nombre +"/")
	pago=OrdenPago.objects.filter(estado="Pagado",fecha_pago__year=year,centro_costos__nombre=centro)
	for p in pago:
		nombre=p.egreso.nombre
		if nombre in pagosD:
			pagosD[nombre]=pagosD[p.egreso.nombre]+p.subtotal
		else :
			pagosD[nombre]=p.subtotal
		if nombre not in listIng:
			pagosD["Impuesto al Valor Agregado (debe hacerse el cálculo estimadodel IVA de todos los gastos contemplados en el presente presupuesto, excepto los que gravan tarifa 0%)"]=pagosD["Impuesto al Valor Agregado (debe hacerse el cálculo estimadodel IVA de todos los gastos contemplados en el presente presupuesto, excepto los que gravan tarifa 0%)"]+p.valor_iva
	#print(pagosD)
	return HttpResponse(json.dumps(pagosD, cls=DjangoJSONEncoder,ensure_ascii=False))



# def presupuestos_anuales_nuevo_fundespol(request):
# 	if(request.method == 'POST'):
# 		form = FundespolForm(request.POST)
# 		if(form.is_valid()):
# 			form.save()
# 			return redirect("presupuesto_anual_lista")
# 	else:
# 		form = FundespolForm()
# 	return render(request, "presupuestos_anuales/fundespol_nuevo.html", {"form":form})


#VISTA PARA CREAR NUEVO PRESUPUESTO DE FUNDESPOL
def presupuestos_anuales_nuevo_fundespol(request):
	dt = datetime.datetime.today()
	
	if(request.method == 'POST'):
		form = EspoltechForm(request.POST)
		if(form.is_valid()):
			try:
				num = Espoltech.objects.all().order_by('num').latest('num').num
				newnum= int(num)+1
				form.instance.num=newnum
				print("entro a siguiente")
			except Espoltech.DoesNotExist:
				newnum = 1
				form.instance.num=newnum
				print("entro a exception")
			
			# Cambio para reutilizar todo de ESPOLTECH y que conste como presupuesto de FUNDESPOL
			form.instance.centro_costos = "FUNDESPOL"
			form.save()
			return redirect("presupuesto_anual_lista")
	else:
		form = EspoltechForm(initial={'año':dt.year})

	return render(request, "presupuestos_anuales/fundespol_nuevo.html", {
		"form":form,
		"tipo":"FUNDESPOL"
		})
	# return render(request, "presupuestos_anuales/fundespol_nuevo.html", {
	# 	"form":form,
	# 	"ingreso_orden":diccionario["total_facturacion_actual"],
	# 	"ingreso_ording":diccionario["total_ording_actual"],
	# 	"tasa_general":diccionario["tasa_general"],
	# 	"fundespol_ingresos":diccionario["centro_costo_ingresos"],
	# 	"espol_ingresos":diccionario["participacion_ingresos_espol"],
	# 	"participacion_unidad":diccionario["participacion_unidad"],
	# 	"tipo":"FUNDESPOL"
	# 	})


# ------------------ FUNCIONES DE EDITAR ---------------------------
def presupuesto_anual_editar(request, pk):
	if(request.method == 'POST'):
		p = get_object_or_404(Espoltech, pk=pk)
		# form = EspoltechForm(request.POST, instance=p)
		form = EspoltechForm(request.POST)
		if(form.is_valid()):
			if p.version!=form.instance.version:
				print("entro a nueva version")
				p.active=False
				p.save()
				form.instance.num=p.num
				form.save()
				return redirect("presupuesto_anual_lista")
			else:
				print("entro a actual version")
				formAct = EspoltechForm(request.POST, instance=p)
				formAct.save()
				return redirect("presupuesto_anual_lista")
	else:
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(instance=p)
	return render(request, "presupuestos_anuales/espoltech_editar.html", {'form': form, 'p':p,"tipo":"ESPOLTECH"})

def presupuesto_anual_editar_fundespol(request, pk):
	if(request.method == 'POST'):
		p = get_object_or_404(Espoltech, pk=pk)
		#form = EspoltechForm(request.POST, instance=p)
		form = EspoltechForm(request.POST)

		if(form.is_valid()):
			if p.version!=form.instance.version:
				print("entro a nueva version")
				p.active=False
				p.save()
				form.instance.num=p.num
				form.instance.centro_costos="FUNDESPOL"
				form.save()
				return redirect("presupuesto_anual_lista")
			else:
				print("entro a actual version")
				formAct = EspoltechForm(request.POST, instance=p)
				formAct.save()
				return redirect("presupuesto_anual_lista")
			
	else:
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(instance=p)
	return render(request, "presupuestos_anuales/fundespol_editar.html", {'form': form, 'p':p,"tipo":"FUNDESPOL"})



# FUNCIONES DE EDITAR UNA VEZ ENVIADA LA SOLICITUD DE APROBACION
def presupuesto_anual_editarAUTR(request, pk):
	if(request.method == 'POST'):
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(request.POST, instance=p)
		if(form.is_valid()):
			form.save()
			return redirect("pendiente_aprobacion")
	else:
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(instance=p)
	return render(request, "presupuestos_anuales/espoltech_aprobar.html", {'form': form, 'p':p})

def presupuesto_anual_editarAUTR_fundespol(request, pk):
	if(request.method == 'POST'):
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(request.POST, instance=p)
		if(form.is_valid()):
			form.save()
			return redirect("pendiente_aprobacion")
	else:
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(instance=p)
	return render(request, "presupuestos_anuales/fundespol_aprobar.html", {'form': form, 'p':p})



# FUNCIONES DE ENVIAR SOLICITUD
def presupuesto_anual_enviar(request, pk):
	p = get_object_or_404(Espoltech, pk=pk)
	p.estado = 'ENVD'
	p.save()
	return redirect('presupuesto_anual_lista')

#Enviar presupuesto para aprobar FUNDESPOL
def presupuesto_anual_enviar_fundespol(request, pk):
	p = get_object_or_404(Espoltech, pk=pk)
	p.estado = 'ENVD'
	p.save()
	return redirect('presupuesto_anual_lista')



# FUNCIONES DE AUTORIZAR PRESUPUESTO
def presupuesto_anual_autorizar(request, pk):
	p = get_object_or_404(Espoltech, pk=pk)
	p.estado = 'AUTR'
	p.save()
	return redirect('pendiente_aprobacion')

#REVISAR ESTO
#DEBERIA FUNCIONAR SI SE CAMBIA FUNDESPOL POR ESPOLTECH
def presupuesto_anual_autorizar_fundespol(request, pk):
	p = get_object_or_404(Espoltech, pk=pk)
	p.estado = 'AUTR'
	p.save()
	return redirect('pendiente_aprobacion')



# FUNCIONES DE ANULAR PRESUPUESTO
def presupuesto_anual_anular(request, pk=None):
	if(request.method == "POST"):
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(request.POST, instance=p)
		if(form.is_valid()):
			form.instance.estado = 'ANLD'
			form.save()
		return redirect('presupuesto_anual_lista')
	else:
		pk = request.GET.get('pk')
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(instance=p)
		return render(request, 'presupuestos_anuales/presupuestos_anuales_anular.html', {'object':p, 'form':form})

#YA HA SIDO CORREGIDO PARA QUE ANULE DE "FUNDESPOL"
#YA QUE SE UTILIZA EL MISMO MODELO (ESPOLTECH) PARA ANULAR, ES CORRECTO QUE AQUI SE USE ESPOLTECH
def presupuesto_anual_anular_fundespol(request, pk=None):
	if(request.method == "POST"):
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(request.POST, instance=p)
		if(form.is_valid()):
			form.instance.estado = 'ANLD'
			form.save()
		return redirect('presupuesto_anual_lista')
	else:
		pk = request.GET.get('pk')
		p = get_object_or_404(Espoltech, pk=pk)
		form = EspoltechForm(instance=p)
		return render(request, 'presupuestos_anuales/presupuestos_anuales_anular.html', {'object':p, 'form':form})

