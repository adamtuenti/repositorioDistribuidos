from .models import OrdenFacturacion
from financiero.orden_facturacion.models import OrdenFacturacion, ESTADO_CHOICES, TIPO_EVENTO
import django_filters
from django import forms
from financiero.orden_pago.models import Centro_Costos
from seguridad.models import *

class OrdenFacturacionFilter(django_filters.FilterSet):
    cod_orden_fact = django_filters.CharFilter(lookup_expr='icontains', label="", widget=forms.TextInput(attrs={'placeholder':'Código orden'}))
    fecha=django_filters.DateFilter(field_name='fecha', label='', widget=forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}))
    ruc_ci=django_filters.CharFilter(lookup_expr='icontains',label="", widget=forms.TextInput(attrs={'placeholder':'RUC o CI'}))
    razon_nombres=django_filters.CharFilter(lookup_expr='icontains',label="", widget=forms.TextInput(attrs={'placeholder':'Nombre Cliente'}))
    estado = django_filters.ChoiceFilter(
        empty_label='Estado',
		choices=ESTADO_CHOICES,
        label=""
    )
    #asesor=django_filters.CharFilter(lookup_expr='icontains', label="", widget=forms.TextInput(attrs={'placeholder':'Asesor'}))
    n_tramite=django_filters.CharFilter(lookup_expr='icontains', label="", widget=forms.TextInput(attrs={'placeholder':'# Trámite'}))
    n_factura=django_filters.CharFilter(lookup_expr='icontains', label="", widget=forms.TextInput(attrs={'placeholder':'# Factura'}))
    centro_costos=django_filters.ModelChoiceFilter(label="", empty_label="Centro de Costos",queryset=Centro_Costos.objects.all())
    roles=RolPermisoUsuario.objects.filter(modulo="Comercial").values_list('usuario', flat=True)
    users=Usuario.objects.filter(pk__in=roles)
    asesor=django_filters.ModelChoiceFilter(label="", empty_label="Asesor",queryset=users)
    class Meta:
        model = OrdenFacturacion
        
        fields=[
            'cod_orden_fact',
            'fecha',
            'ruc_ci',
            'razon_nombres',
            'estado',
            'asesor',
            'n_tramite',
            'n_factura',
            'centro_costos',
            
        ]
