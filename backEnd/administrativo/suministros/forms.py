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



class SuministroForm(forms.ModelForm):
    
    class Meta:
        model=Suministro

        fields= "__all__"

        labels = {
                "cod_suministro":"Código",
                "fecha":"Fecha",
                "fecha_facturacion":"Fecha Fact.",
                "tipo_proveedor":"Tipo de proveedor",
                "proveedor":"Razón social/Nombre",
                "numero_factura":"Nº Factura",
                'centro_costos': 'Centro de costos',
                "observaciones":"Observaciones",
                "subtotal":"",
                "iva":"",
                'valor_iva': '',
                "total":"",
                
        }

        
        widgets={
            "cod_suministro":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            # "proveedor":forms.HiddenInput(),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
            "fecha_facturacion":forms.DateInput(attrs={"type":"date"}),
            "observaciones": forms.Textarea(attrs={'rows':2}),
            "tipo_proveedor":forms.Select(attrs={"class":"form-control"}),
            "proveedor":forms.HiddenInput(),
            "centro_costos":forms.Select(attrs={"class":"select form-control"}),

            'subtotal': forms.HiddenInput(),
            'iva': forms.HiddenInput(),
            'valor_iva': forms.HiddenInput(),
            'total': forms.HiddenInput(),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].initial = datetime.date.today
        self.fields['fecha'].disabled = True
        self.fields['cod_suministro'].disabled = True

    def clean_fecha_facturacion(self):
        fecha_inicio = self.cleaned_data["fecha"]
        fecha_fin = self.cleaned_data["fecha_facturacion"]
        return validate_date_with_offset(fecha_inicio,fecha_fin,15)


class UpdateSuministroForm(forms.ModelForm):
    
    class Meta:
        model=Suministro

        fields= "__all__"

        labels = {
                "cod_suministro":"Código",
                "fecha":"Fecha",
                "tipo_proveedor":"Tipo de proveedor",
                "proveedor":"Razón social/Nombre",
                "numero_factura":"Nº Factura",
                "fecha_facturacion":"Fecha Fact.",
                'centro_costos': 'Centro de costos',
                "observaciones":"Observaciones",
                "subtotal":"",
                "iva":"",
                'valor_iva': '',
                "total":"",
                
        }

        
        widgets={
            "cod_suministro":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "proveedor":forms.HiddenInput(),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
            "fecha_facturacion":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
            "observaciones": forms.Textarea(attrs={'rows':2}),
            'subtotal': forms.HiddenInput(),
            "tipo_proveedor":forms.Select(attrs={"class":"form-control"}),
            "proveedor":forms.HiddenInput(),
            'iva': forms.HiddenInput(),
            'valor_iva': forms.HiddenInput(),
            'total': forms.HiddenInput(),
            "centro_costos":forms.Select(attrs={"class":"select form-control",'disabled':True}),

            
        }

class ProductoSuministroForm(forms.ModelForm):

    class Meta: 
        model= ProductoSuministro 
        exclude=()

SuministroProductoFormset = inlineformset_factory(
    Suministro, ProductoSuministro, form=ProductoSuministroForm,
    fields=['cantidad','precio','descuento','subtotal','producto',],
     extra=1,can_delete=True
    )


class SuministroFilter(django_filters.FilterSet):
    cod_suministro = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Código del Producto'}))    
    proveedor_id = django_filters.CharFilter(label="", widget=forms.NumberInput(attrs={'placeholder': 'Identificación Proveedor'}),method='filter_by_ruc_ci')
    proveedor_nom = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={'placeholder': 'Nombre Proveedor'}),method='filter_by_razon_nombre')
    fecha = django_filters.DateFilter(field_name='fecha', label='', widget=forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}))
    fecha_facturacion=django_filters.DateFromToRangeFilter(label="",widget = RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}),attrs={'class': 'form-control '}))
    centro_costos=django_filters.ModelChoiceFilter(label="", empty_label="Centro de Costos",queryset=Centro_Costos.objects.all())


    class Meta:
        model = Suministro
        fields = [
                    "cod_suministro",
                    "proveedor",
                    'proveedor_id',
                    'proveedor_nom',
					"fecha",
                    "centro_costos",
				]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_by_ruc_ci(self, queryset, name, value):
        return queryset.filter(Q(proveedor__ruc__icontains=value))

    def filter_by_razon_nombre(self, queryset, name, value):
        return queryset.filter(Q(proveedor__razon__icontains=value))
        