from ventas.reporte_contacto.models import ReporteContacto
from ventas.personas_juridicas.models import Juridica, Sector, TipoEmpresa
from ventas.interesados.models import CanalContacto
import django_filters
from django import forms


class ReporteContactoFilter(django_filters.FilterSet):
    cod_reporte = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Código de reporte'}))
    """empresa_nombre=django_filters.CharFilter(lookup_expr='icontains',label='Empresa')"""
    
    ruc_ci = django_filters.CharFilter(label='', widget=forms.TextInput(attrs={'placeholder': 'RUC'}))
    razon_nombres = django_filters.CharFilter(label='', widget=forms.TextInput(attrs={'placeholder': 'Empresa'}))
    #ruc_ci = django_filters.ModelChoiceFilter(label="", empty_label="RUC", field_name='ruc_ci',queryset=Juridica.objects.values_list('ruc', flat=True))
    #razon_nombres = django_filters.ModelChoiceFilter(label="", empty_label="Empresa", field_name='razon_nombres', queryset=Juridica.objects.values_list('nombre', flat=True))
    sector = django_filters.ModelChoiceFilter(label="", empty_label="Sector",queryset=Sector.objects.all())
    tipo_empresa = django_filters.ModelChoiceFilter(label="", empty_label="Tipo de Empresa",queryset=TipoEmpresa.objects.all())
    canal_de_contacto = django_filters.ModelChoiceFilter(label="", empty_label="Canal de contacto",queryset=CanalContacto.objects.all())
    #canal_de_contacto = django_filters.CharFilter(label='', widget=forms.TextInput(attrs={'placeholder': 'Canal de contacto'}))
    fecha=django_filters.DateFilter(field_name='fecha', label='',widget=forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}))



    class Meta:
        model = ReporteContacto
        
        fields=[
            'cod_reporte',
            'razon_nombres',
            'ruc_ci',
            'canal_de_contacto',
            'tipo_empresa',
            'sector',
            'fecha',
        ]

        
		