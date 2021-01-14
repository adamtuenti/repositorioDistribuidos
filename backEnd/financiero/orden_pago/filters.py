from .models import OrdenPago
import django_filters
from django import forms
from financiero.orden_pago.models import ESTADO_CHOICES
from django.db.models import Q

class OrdenPagoFilter(django_filters.FilterSet):
	cod_ord_pago = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Código orden pago'}))
	estado = django_filters.ChoiceFilter(label="", empty_label='Estado', choices=ESTADO_CHOICES)
	#fecha = django_filters.DateFilter(label="", widget=forms.DateInput(attrs={'placeholder':'Fecha: dd-mm-aaaa','type':'date'}))
	#fecha = django_filters.DateFromToRangeFilter(label="",widget=RangeWidget(attrs={'placeholder': 'Fecha','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'type':'date','class':'fecha form-control'}))
	fecha__gte = django_filters.DateFilter(label="",field_name='fecha', lookup_expr='gte',widget=forms.DateInput(attrs={'placeholder':'Fecha Inicio','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
	fecha__lte = django_filters.DateFilter(label="",field_name='fecha', lookup_expr='lte',widget=forms.DateInput(attrs={'placeholder':'Fecha Fin','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
	evento__nombre=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Nombre evento'}))
	evento__codigo_evento=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Código evento'}))
	proveedor_id = django_filters.CharFilter(label="", widget=forms.NumberInput(attrs={'placeholder': 'Identificación Proveedor'}),method='filter_by_ruc_ci')
	proveedor_nom = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={'placeholder': 'Nombre Proveedor'}),method='filter_by_razon_nombre')
	egreso__codigo=django_filters.CharFilter(label="",lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"N° Partida Presupuestaria",}))
	egreso__nombre=django_filters.CharFilter(label="",lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"Partida Presupuestaria",}))
	n_tramite=django_filters.CharFilter(label="",lookup_expr='icontains',widget=forms.TextInput(attrs={"placeholder":"N° Trámite"}))
	fecha_tramite = django_filters.DateFilter(label="", lookup_expr='exact',widget=forms.DateInput(attrs={'placeholder':'Fecha Trámite','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))

	#Falta agregar filtro por codigo de evento

	class Meta:
		model = OrdenPago
		fields = ["cod_ord_pago", "estado", "fecha", "proveedor","fecha__gte","fecha__lte",'evento__nombre','evento__codigo_evento','proveedor_id','proveedor_nom','egreso__codigo','egreso__nombre','n_tramite']
	
	def filter_by_ruc_ci(self, queryset, name, value):
		return queryset.filter(Q(proveedor__ruc__icontains=value))

	def filter_by_razon_nombre(self, queryset, name, value):
		return queryset.filter(Q(proveedor__razon__icontains=value))