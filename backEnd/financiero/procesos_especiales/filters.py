import django_filters
from django import forms
from django.http import QueryDict
from .models import *
from django.contrib.postgres.forms.ranges import DateTimeRangeField, RangeWidget
from django.template import loader
from django.utils.safestring import mark_safe


class ProcesoEspecialFilter(django_filters.FilterSet):
    
    class Meta:
        model = ProcesoEspecial
        fields = "__all__"
    procesoparticipante__cod_evento = django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Código Evento'}))
    procesoparticipante__nombre_evento = django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Nombre Evento'}))
    procesoparticipante__orden__ruc_ci=django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'RUC/CI'}))
    procesoparticipante__orden__razon_nombres=django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Razon/Nombres'}))
    estado = django_filters.ChoiceFilter(label="", empty_label="Estado Proceso Especial",choices = ProcesoEspecial.ESTADO_CHOICES)
    tipo_nota = django_filters.ChoiceFilter(label="", empty_label="Tipo nota",choices = ProcesoEspecial.TIPO_NOTA_CHOICES)
    categoria = django_filters.ChoiceFilter(label="", empty_label="Categoría",choices = ProcesoEspecial.CATEGORIA)
    fechas_emision= django_filters.DateFromToRangeFilter(field_name ='fecha_emision',widget = RangeWidget(forms.DateInput(),attrs={'class': 'form-control ',"onfocus":"(this.type='date')"}))
    