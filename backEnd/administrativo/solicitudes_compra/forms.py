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


class ComprasForm(forms.ModelForm):
    
    class Meta:
        model = SolicitudCompra
        fields = "__all__"

        labels = {
                "cod_solicitud": "Código",
                "fecha": "Fecha solicitud",
                "tipo_proceso": "Tipo Proceso",
                "procedimiento_sugerido": "Procedimiento sugerido",
                "tipo_compra": "Tipo compra",
                "periodo_compra": "Periodo de compra",
                'centro_costos': 'Centro de costos',
                "estado": "Estado",
                "fecha_requerimiento":"Fecha Requerimiento",
                "sede_responsable":"Sede",
                
                "subtotal_0": "",
                "subtotal_iva": "",
                "iva": "",
                'valor_iva': '',
                "total": "",
                
        }
        
        widgets = {
            "cod_solicitud":forms.TextInput(attrs={"class":"form-control", "type":"number", 'readonly':'readonly'}),
            "fecha":forms.DateInput(attrs={"readonly":True, 'class':'form-control', "type":"date", "value":date.today}),
            "tipo_proceso":forms.Select(attrs={"class":"form-control"}),
            "procedimiento_sugerido":forms.Select(attrs={"class":"form-control"}),
            "tipo_compra":forms.Select(attrs={"class":"form-control"}),
            "tipo_compra":forms.Select(attrs={"class":"form-control"}),
            "centro_costos":forms.Select(attrs={"class":"select form-control"}),
            "estado":forms.Select(attrs={"class":"select form-control"}),
            "fecha_requerimiento":forms.DateInput(attrs={'class':'form-control',"type":"date", "value":date.today}),
            "sede_responsable":forms.Select(attrs={"class":"form-control"}),
            'subtotal_0': forms.HiddenInput(),
            'subtotal_iva': forms.HiddenInput(),
            'iva': forms.HiddenInput(),
            'valor_iva': forms.HiddenInput(),
            'total': forms.HiddenInput(),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].initial = datetime.date.today
        self.fields['fecha'].disabled = True
        self.fields['cod_solicitud'].disabled = True

    def clean_fecha_aprobacion(self):
        fecha_inicio = self.cleaned_data["fecha"]
        fecha_fin = self.cleaned_data["fecha_aprobacion"]
        if (fecha_fin is not None):
            return validate_date_with_offset(fecha_inicio, fecha_fin, 15)


class ComprasUpdateForm(forms.ModelForm):
    
    class Meta:
        model = SolicitudCompra
        fields = "__all__"

        labels = {
                "cod_solicitud": "Código",
                "fecha": "Fecha solicitud",
                "tipo_proceso": "Tipo Proceso",
                "procedimiento_sugerido": "Procedimiento sugerido",
                "tipo_compra": "Tipo compra",
                "periodo_compra": "Periodo de compra",
                'centro_costos': 'Centro de costos',
                "estado": "Estado",
                "fecha_requerimiento":"Fecha Requerimiento",
                "sede_responsable":"Sede",
                
                "subtotal_0": "",
                "subtotal_iva": "",
                "iva": "",
                'valor_iva': '',
                "total": "",
                
        }
        
        widgets = {
            "cod_solicitud":forms.TextInput(attrs={"class":"form-control", "type":"number", 'readonly':'readonly'}),
            "fecha":forms.DateInput(attrs={"readonly":True, 'class':'form-control', "type":"date", "value":date.today}),
            "tipo_proceso":forms.Select(attrs={"class":"form-control"}),
            "procedimiento_sugerido":forms.Select(attrs={"class":"form-control"}),
            "tipo_compra":forms.Select(attrs={"class":"form-control"}),
            "tipo_compra":forms.Select(attrs={"class":"form-control"}),
            "centro_costos":forms.Select(attrs={"class":"select form-control"}),
            "estado":forms.Select(attrs={"class":"select form-control"}),
            "fecha_requerimiento":forms.DateInput(attrs={'class':'form-control',"type":"date", "value":date.today}),
            "sede_responsable":forms.Select(attrs={"class":"form-control"}),
            'subtotal_0': forms.HiddenInput(),
            'subtotal_iva': forms.HiddenInput(),
            'iva': forms.HiddenInput(),
            'valor_iva': forms.HiddenInput(),
            'total': forms.HiddenInput(),
            
        }

class ProductoSolicitudForm(forms.ModelForm):

    class Meta: 
        model= ProductoSolicitud 
        exclude=()

SolicitudProductoFormset = inlineformset_factory(
    SolicitudCompra, ProductoSolicitud, form=ProductoSolicitudForm,
    fields=['otros','caracteristicas','cantidad','precio_referencial','iva','subtotal','producto',],
     extra=1,can_delete=True
    )

class ComprasFilter(django_filters.FilterSet):
    ESTADO_CHOICES = [("Elaborado", "Elaborado"), ("Aprobado", "Aprobado"), ("Anulada", "Anulada"), ]
    PROCESO_SUGERIDO_CHOICES = [("Catálogo Electrónico", "Catálogo Electrónico"), ("Subasta Inversa", "Subasta Inversa"), ("Ínfima Cuantía", "Ínfima Cuantía"),
    ("Menor Cuantía", "Menor Cuantía"), ("Cotización", "Cotización"), ("Licitación", "Licitación"), ("Contratación Directa", "Contratación Directa"),
     ("Contratación  integral por Precio Fijo", "Contratación  integral por Precio Fijo"), ("Lista Corta", "Lista Corta"), ("Concurso Público", "Concurso Público"), ]
    PERIODO_COMPRA_CHOICES = [("Diario", "Diario"), ("Quincenal", "Quincenal"), ("Mensual", "Mensual"),
    ("Trimestral", "Trimestral"), ("Cuatrimestral", "Cuatrimestral"), ("Semestral", "Semestral"),
    ("Anual", "Anual"), ("No aplica", "No aplica"), ]
    TIPO_PROCESO_CHOICES = [("Bienes y Servicios Normalizados", "Bienes y Servicios Normalizados"), ("Bienes y Servicios No Normalizados", "Bienes y Servicios No Normalizados"),
    ("Obras", "Obras"), ("Consultoría", "Consultoría"), ]
    TIPO_COMPRA_CHOICES = [("Bienes", "Bienes"), ("Servicios", "Servicios"), ]

    cod_solicitud = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Código de la solicitud'}))    
    estado = django_filters.ChoiceFilter(label="", empty_label="Estado", choices=ESTADO_CHOICES)
    tipo_proceso = django_filters.ChoiceFilter(label="", empty_label="Tipo de proceso", choices=TIPO_PROCESO_CHOICES)
    procedimiento_sugerido = django_filters.ChoiceFilter(label="", empty_label="Procedimiento sugerido", choices=PROCESO_SUGERIDO_CHOICES)
    periodo_compra = django_filters.ChoiceFilter(label="", empty_label="Periodo de compra", choices=PERIODO_COMPRA_CHOICES)
    tipo_compra = django_filters.ChoiceFilter(label="", empty_label="Tipo de compra", choices=TIPO_COMPRA_CHOICES)
    fecha = django_filters.DateFromToRangeFilter(label="", widget=RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha', "class":"textbox-n", "onfocus":"(this.type='date')"}), attrs={'class': 'form-control '}))
    centro_costos = django_filters.ModelChoiceFilter(label="", empty_label="Centro de Costos", queryset=Centro_Costos.objects.all())

    class Meta:
        model = SolicitudCompra
        fields = [
                    "cod_solicitud",
                    "estado",
                    "tipo_proceso",
                    "procedimiento_sugerido",
                    "periodo_compra",
                    'tipo_compra',
                    'fecha',
                    "centro_costos",
				]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

