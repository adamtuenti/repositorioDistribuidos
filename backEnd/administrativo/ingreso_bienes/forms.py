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


class BienForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BienForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bien

        fields= "__all__"

        labels = {
                "cod_activo":"Código Activo",
                "cod_orden":"Código",
                "fecha_registro":"Fecha Registro",
                "fecha":"Fecha",
                "cod_bien":"Código Bien",
                "nombre":"Nombre del Activo",
                "marca":"Marca",
                "modelo":"Modelo",
                "n_Serie":"N° Serie",
                "tipo_bien":"Tipo Bien",
                "categoria":"Categoria",
                "estado":"Estado",
                "inventario":"Inventario",
                "iva":"IVA",
                "cod_inventariound":"Cód Inventario Und",
                "cod_Espoltech":"Cód Espoltech",
                "fecha_compra":"Fecha Compra",
                "frecuencia_mantenimiento":"Frecuencia Mantenimiento",
                "preventivo":"Preventivo",
                "correctivo":"Correctivo",
                "caracteristicas":"Carecterísticas",
                "subtotal":"",
                'valor_iva':'',
                "descuento":"",
                "total":"",
                "observaciones":"Observaciones",
                "centro_costos": "Centro de costos",
                "fecha_inventario":"Fecha Inventario",
                "ubicacion_inicial":"Ubicación Inicial",
                "ubicacion_final":"Ubicación Final",
                
        }
        
        widgets={
                "cod_activo":forms.TextInput(attrs={"class":"form-control",'readonly': True}),
                "cod_orden":forms.TextInput(attrs={"class":"form-control",'readonly': True}),
                "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
                "fecha_registro":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
                "cod_bien":forms.TextInput(attrs={"class":"form-control"}),
                "nombre":forms.TextInput(attrs={"class":"form-control"}),
                "marca":forms.TextInput(attrs={"class":"form-control"}),
                "modelo":forms.TextInput(attrs={"class":"form-control"}),
                "n_Serie":forms.TextInput(attrs={"class":"form-control"}),
                "tipo_bien":forms.Select(attrs={"class":"form-control"}),
                "categoria":forms.Select(attrs={"class":"form-control"}),
                "estado":forms.Select(attrs={"class":"form-control"}),
                "inventario":forms.Select(attrs={"class":"form-control"}),
                "iva":forms.Select(attrs={"class":"form-control"}),
                "cod_inventariound":forms.TextInput(attrs={"class":"form-control","type":"number"}),
                "cod_Espoltech":forms.TextInput(attrs={"class":"form-control","type":"number"}),
                "fecha_compra":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
                "frecuencia_mantenimiento":forms.Select(attrs={"class":"form-control"}),
                "preventivo":forms.Select(attrs={"class":"form-control"}),
                "correctivo":forms.Select(attrs={"class":"form-control"}),
                "caracteristicas": forms.Textarea(attrs={'rows':2}),
                "subtotal":forms.HiddenInput(),
                'valor_iva':forms.HiddenInput(),
                "descuento":forms.HiddenInput(),
                "total":forms.HiddenInput(),
                "observaciones": forms.Textarea(attrs={'rows':2}),
                "centro_costos":forms.Select(attrs={"class":"select form-control"}),
                "fecha_inventario":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
                "ubicacion_inicial":forms.TextInput(attrs={"class":"form-control"}),
                "ubicacion_final":forms.TextInput(attrs={"class":"form-control"}),
        }
        
        class PropertyModelChoiceField(forms.ModelChoiceField):
            def label_from_instance(self, obj):
                return obj.type


class BienFilter(django_filters.FilterSet):
    cod_bien = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Código'}))    
    cod_activo = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Activo'}))  
    proveedor_id = django_filters.CharFilter(label="", widget=forms.NumberInput(attrs={'placeholder': 'Ruc Proveedor'}),method='filter_by_ruc_ci')
    proveedor_nom = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={'placeholder': 'Nombre Proveedor'}),method='filter_by_razon_nombre')
    fecha = django_filters.DateFilter(field_name='fecha', label='', widget=forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}))
    fecha_facturacion = django_filters.DateFromToRangeFilter(label="",widget = RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}),attrs={'class': 'form-control '}))
    centro_costos = django_filters.ModelChoiceFilter(label="", empty_label="Centro de Costos",queryset=Centro_Costos.objects.all())


    class Meta:
        model = Bien
        fields = [
                    "cod_bien",
                    "cod_activo",
                    "proveedor",
                    'proveedor_id',
                    'proveedor_nom',
					"fecha",
                    "fecha_facturacion",
                    "centro_costos",
				]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_by_ruc_ci(self, queryset, name, value):
        return queryset.filter(Q(proveedor__ruc__icontains=value))

    def filter_by_razon_nombre(self, queryset, name, value):
        return queryset.filter(Q(proveedor__razon__icontains=value))



class RegistroForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ingreso_Bien

        fields= "__all__"

        labels = {

                "cod_orden":"Código",
                "fecha_registro":"Fecha registro",
                "fecha_factura":"Fecha Factura",
                "num_factura":"N° Factura",
                "proveedor":"Nombre Proveedor",
                "ruc_proveedor":"Ruc Proveedor",
                "subtotal":"",
                'valor_iva':'',
                "descuento":"",
                "total":"",
                "observaciones":"Observaciones",
                "centro_costos": "Centro de costos",
                
        }
        
        widgets={
                "cod_orden":forms.TextInput(attrs={"class":"form-control",'readonly': True}),
                "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
                "fecha_registro":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
                "fecha_factura":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
                "subtotal":forms.TextInput(attrs={"class":"form-control","type":"number"}),
                "num_factura":forms.TextInput(attrs={"class":"form-control","type":"number"}),
                'valor_iva':forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
                "descuento":forms.TextInput(attrs={"class":"form-control","type":"number"}),
                "total":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
                "observaciones": forms.Textarea(attrs={'rows':2}),
                "proveedor": forms.TextInput(attrs={'rows':2}),
                "ruc_proveedor": forms.TextInput(attrs={'rows':2}),
                "centro_costos":forms.Select(attrs={"class":"select form-control"}),
        }