from .models import Proforma
import django_filters
from django import forms
from dal import autocomplete


class ProformaFilter(django_filters.FilterSet):
    "quité type:date de ambos campos de fecha"
    ESTADO_CHOICES= [("Aceptada","Aceptada"),("No aceptada","No aceptada"), ("Seguimiento","Seguimiento") ,("Por Enviar","Por Enviar")]
    codigo=django_filters.CharFilter(lookup_expr='icontains',label='', widget=forms.TextInput(attrs={'placeholder': 'Código'}))
    
    #empresa= autocomplete.ModelSelect2(url='empresa-autocomplete',attrs={'placeholder':'Empresa'})
    ruc_ci = django_filters.CharFilter(label='', widget=forms.TextInput(attrs={'placeholder': 'RUC'}))
    razon_nombres = django_filters.CharFilter(label='', widget=forms.TextInput(attrs={'placeholder': 'Empresa'}))
    
    asesor = django_filters.CharFilter(label="", lookup_expr='icontains', widget=forms.TextInput(attrs={'placeholder': 'Asesor'}))


    fechaSolicitud=django_filters.DateFilter(field_name='fechaSolicitud', label='', widget=forms.DateInput(attrs={'placeholder':'Fecha de Solicitud',"class":"textbox-n", "onfocus":"(this.type='date')"}))
    fechaEnvio=django_filters.DateFilter(field_name='fechaEnvio',label='', widget=forms.DateInput(attrs={'placeholder':'Fecha de Envío',"class":"textbox-n", "onfocus":"(this.type='date')"}))
    estado=django_filters.ChoiceFilter(label="", empty_label="Estado", choices=ESTADO_CHOICES)
    class Meta:
        model = Proforma
        
        fields=[
            'codigo',
            #'empresa',
            'razon_nombres',
            'ruc_ci',
            'asesor',
            'fechaSolicitud',
            'fechaEnvio',
            'estado',
        ]
    

