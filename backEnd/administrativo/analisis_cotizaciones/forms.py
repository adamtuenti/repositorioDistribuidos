from dal import autocomplete
from . import models
from django import forms
import django_filters
from .models import *
from django.forms import modelformset_factory
from datetime import date
from django.forms.models import inlineformset_factory
from django.contrib.postgres.forms.ranges import DateTimeRangeField, RangeWidget
import datetime
from datetime import date
from ventas.validaciones import validate_date_with_offset
from django.db.models import Q
from .models import Proveedor
from .models import SolicitudCompra


class CotizacionesForm(forms.ModelForm):
    
    class Meta:
        model = AnalisisCotizaciones
        fields = "__all__"

        labels = {
                "cod_analisis": "Código Análisis",
                "fecha": "Fecha solicitud",
                "tipo_proveedor": "Tipo Proveedor",
                "proveedor": "Proveedor",
                "ruc": "RUC",
                "razon_social": "Razón Social",
                "tipo_proceso": "Tipo Proceso",
                "procedimiento_sugerido": "Procedimiento sugerido",
                "tipo_compra": "Tipo compra",
                "detalle_proceso": "Detalle Proceso",
                'centro_costos': 'Centro de costos',
                "estado": "Estado",
                "fecha_facturacion":"Fecha Fact.",
                "criterio_seleccion": "Criterio de Selección",
                "valor_letras": "Son valor en letras",
                "anexos": "Anexos",
                "subtotal": "",
                "iva": "",
                'valor_iva': '',
                "total": "",
                
        }
        
        widgets = {
            "cod_sanalisis":forms.TextInput(attrs={"class":"form-control", "type":"number", 'readonly':'readonly'}),
            "fecha":forms.DateInput(attrs={"readonly":True, 'class':'form-control', "type":"date", "value":date.today}),
            "tipo_proveedor":forms.Select(attrs={"class":"form-control"}),
            "ruc":forms.TextInput(attrs={"class":"form-control","type":"number"}),
			"razon_social":forms.TextInput(attrs={"class":"form-control"}),
            "tipo_proceso":forms.Select(attrs={"class":"form-control"}),
            "procedimiento_sugerido":forms.Select(attrs={"class":"form-control"}),
            "tipo_compra":forms.Select(attrs={"class":"form-control"}),
            "detalle_proceso":forms.TextInput(attrs={"class":"form-control"}),
            "centro_costos":forms.Select(attrs={"class":"select form-control"}),
            "estado":forms.Select(attrs={"class":"select form-control"}),
            "fecha_facturacion":forms.DateInput(attrs={"type":"date"}),
            "criterio_seleccion":forms.TextInput(attrs={"class":"form-control"}),
            "valor_letras":forms.TextInput(attrs={"class":"form-control"}),
            "anexos":forms.TextInput(attrs={"class":"form-control"}),
            'subtotal': forms.HiddenInput(),
            'iva': forms.HiddenInput(),
            'valor_iva': forms.HiddenInput(),
            'total': forms.HiddenInput(),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].initial = datetime.date.today
        self.fields['fecha'].disabled = True
        self.fields['cod_analisis'].disabled = True

    def clean_fecha_aprobacion(self):
        fecha_inicio = self.cleaned_data["fecha"]
        fecha_fin = self.cleaned_data["fecha_aprobacion"]
        return validate_date_with_offset(fecha_inicio, fecha_fin, 15)


class AnalisisFilter(django_filters.FilterSet):
    ESTADO_CHOICES = [("Elaborado", "Elaborado"), ("Aprobado", "Aprobado"), ("Anulada", "Anulada")]
    TIPO_PROVEEDOR_CHOICES = [("Natural","Natural"), ("Jurídica","Jurídica")]
    TIPO_PROCESO_CHOICES = [("Bienes y Servicios Normalizados", "Bienes y Servicios Normalizados"), ("Bienes y Servicios No Normalizados", "Bienes y Servicios No Normalizados"),
    ("Obras", "Obras"), ("Consultoría", "Consultoría")]
    PROCESO_SUGERIDO_CHOICES = [("Catálogo Electrónico", "Catálogo Electrónico"), ("Subasta Inversa", "Subasta Inversa"), ("Ínfima Cuantía", "Ínfima Cuantía"),
    ("Menor Cuantía", "Menor Cuantía"), ("Cotización", "Cotización"), ("Licitación", "Licitación"), ("Contratación Directa", "Contratación Directa"),
     ("Contratación  integral por Precio Fijo", "Contratación  integral por Precio Fijo"), ("Lista Corta", "Lista Corta"), ("Concurso Público", "Concurso Público")]

    cod_analisis = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Código de la solicitud'}))    
    tipo_proveedor = django_filters.ChoiceFilter(label="", empty_label="Tipo de Proveedor", choices=TIPO_PROVEEDOR_CHOICES)
    tipo_proceso = django_filters.ChoiceFilter(label="", empty_label="Tipo de Proceso", choices=TIPO_PROCESO_CHOICES)
    procedimiento_sugerido = django_filters.ChoiceFilter(label="", empty_label="Procedimiento sugerido", choices=PROCESO_SUGERIDO_CHOICES)
    estado = django_filters.ChoiceFilter(label="", empty_label="Estado", choices=ESTADO_CHOICES)
    ruc = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control","type":"number",'placeholder': 'RUC'}))
    razon = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Razón Social'}))
    fecha = django_filters.DateFilter(field_name='fecha', label='', widget=forms.DateInput(attrs={'placeholder':'Fecha', "class":"textbox-n", "onfocus":"(this.type='date')"}))
    fecha_facturacion = django_filters.DateFromToRangeFilter(label="", widget=RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha', "class":"textbox-n", "onfocus":"(this.type='date')"}), attrs={'class': 'form-control '}))
    centro_costos = django_filters.ModelChoiceFilter(label="", empty_label="Centro de Costos", queryset=Centro_Costos.objects.all())

    class Meta:
        model = AnalisisCotizaciones
        fields = [
                    "cod_analisis",
                    "tipo_proveedor",
                    "tipo_proceso",
                    "procedimiento_sugerido",
                    "fecha",
                    "estado",
                    "ruc",
                    "razon",
                    "centro_costos",
				]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

