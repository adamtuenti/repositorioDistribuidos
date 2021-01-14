from .models import PresupuestoEvento, ESTADO_CHOICES, Juridica, TIPO_CHOICES, Centro_Costos
import django_filters
from django import forms
from dal import autocomplete


class PresupuestoEventoFilter(django_filters.FilterSet):
    all_Juridica=Juridica.objects.all()
    codigo = django_filters.CharFilter(lookup_expr='icontains', label="", widget=forms.TextInput(attrs={'placeholder':'Código Presupuesto'}))
    codigo_propuesta = django_filters.CharFilter(lookup_expr='icontains', label="", widget=forms.TextInput(attrs={'placeholder':'Código Propuesta'}))
    evento__nombre=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Nombre evento'}))
    evento__codigo_evento=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Código evento'}))
    fecha=django_filters.DateFilter(field_name='fecha', label='',widget=forms.DateInput(attrs={'placeholder':'Fecha Elaboración','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
    evento__fecha_inicio=django_filters.DateFilter(label='',widget=forms.DateInput(attrs={'placeholder':'Fecha Inicio Evento','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
    evento__fecha_fin=django_filters.DateFilter(label='',widget=forms.DateInput(attrs={'placeholder':'Fecha Fin Evento','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
    evento__modalidad=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Modalidad'}))

    centro_costos=django_filters.ChoiceFilter(
        label="",
        choices=Centro_Costos.objects.all().values_list('pk','nombre'),
        empty_label="Centro Costos"
    )
    razon_nombres=django_filters.CharFilter(lookup_expr='icontains', label="", widget=forms.TextInput(attrs={'placeholder':'Razón Social'}))
    ruc_ci=django_filters.CharFilter(lookup_expr='icontains', label="", widget=forms.TextInput(attrs={'placeholder':'RUC'}))

    estado = django_filters.ChoiceFilter(
        empty_label='Estado',
		choices=ESTADO_CHOICES,
        label=""
    )
    tipo = django_filters.ChoiceFilter(
        empty_label='Tipo',
        label="",
        choices=TIPO_CHOICES
    )

    class Meta:
        model = PresupuestoEvento
        
        fields=[
            'tipo',
            'codigo',
            'fecha',
            'razon_nombres',
            'ruc_ci',
            'estado',
            'codigo_propuesta',
            'centro_costos',
            "evento__nombre",
            "evento__codigo_evento",
            "evento__fecha_inicio",
            "evento__fecha_fin",
        ]
