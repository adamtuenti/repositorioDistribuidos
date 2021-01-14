from financiero.plan_anual_compras.models import PlanAnualCompras, ESTADO_CHOICES
from financiero.orden_pago.models import Centro_Costos

import django_filters
from django import forms

class PlanAnualComprasFilter(django_filters.FilterSet):

	año = django_filters.NumberFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Año','type':'number'}))
	nombre = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Nombre Plan Anual de Compras'}))
	centro_costos = django_filters.ChoiceFilter(label="",empty_label="Centro de Costos",choices=Centro_Costos.objects.all().values_list('id','nombre'))
	estado = django_filters.ChoiceFilter(label="",empty_label="Estado",choices=ESTADO_CHOICES)
	fecha=django_filters.DateFilter(field_name='fecha', label='',widget=forms.DateInput(attrs={'placeholder':'Fecha Elaboración','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
	class Meta:
		model = PlanAnualCompras
		fields = ["año", "nombre","centro_costos","fecha","estado"]