from .models import Espoltech, Fundespol
import django_filters
from django import forms
from financiero.orden_pago.models import Centro_Costos

class EspoltechFilter(django_filters.FilterSet):
	año = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Año'}))
	nombre = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Nombre de Presupuesto'}))
	centro_costos = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Centro de Costos'}))
	class Meta:
		model = Espoltech
		fields = ['año','nombre','centro_costos']

class FundespolFilter(django_filters.FilterSet):
	año = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Año'}))
	nombre = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Nombre de Presupuesto'}))
	centro_costos = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Centro de Costos'}))
	class Meta:
		model = Espoltech
		fields = ['año','nombre','centro_costos']

class RealFilter(django_filters.FilterSet):
	año = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Año'}))
	#centro_costos = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Centro de Costos'}))
	centro_costos=django_filters.ModelChoiceFilter(label="", empty_label="Centro de Costos",queryset=Centro_Costos.objects.all())
	class Meta:
		model = Espoltech
		fields = ['año','centro_costos']