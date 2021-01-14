from django import forms
from datetime import date
from . import models
from .models import Mantenimiento
from .forms import *
from django.forms import modelformset_factory
from django.db.models import Q
import django_filters
from django.contrib.postgres.forms.ranges import DateTimeRangeField, RangeWidget
from financiero.orden_pago.models import Centro_Costos
from administrativo.proveedores.models import Proveedor

class MantenimientoForm(forms.ModelForm):
    
    class Meta:
        model=Mantenimiento

        fields= "__all__"

        labels = {
                "detalle_mantenimiento":"Detalle Mantenimiento",
                "cod_mantenimiento":"Código",
                "fecha":"Fecha",
                "tipo_bien":"Tipo bien",
                "bien":"Nombre",
                "cod_bien":"Código bien",
                "ingreso_bien":"Ingreso de bienes",
                "egresos":"Partida Presupuestaria",
                "proveedor":"Razón social/Nombre",
                "subtotal":"",
                'valor_iva': '',
                'descuento':"",
                "total":"",
                "observaciones":"Observaciones",
                "anexo":"Anexos",
                
        }

        
        widgets={
            "detalle_mantenimiento": forms.Textarea(attrs={"class":"form-control",'rows':2}),
            "cod_mantenimiento":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
            "tipo_bien":forms.Select(attrs={"class":"form-control"}),
            "observaciones": forms.Textarea(attrs={'rows':2}),
            
            "tipo_proveedor":forms.Select(attrs={"class":"form-control"}),
            "proveedor":forms.HiddenInput(),
            "bien":forms.HiddenInput(),
            "ingreso_bien":forms.HiddenInput(),
            "egresos":forms.Select(attrs={"class":"form-control"}),

            'subtotal': forms.HiddenInput(),
            'descuento':forms.HiddenInput(),
            'valor_iva': forms.HiddenInput(),
            'total': forms.HiddenInput(),

            'anexo': forms.ClearableFileInput(),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].initial = date.today
        self.fields['fecha'].disabled = True
        self.fields['cod_mantenimiento'].disabled = True

    def clean_fecha_facturacion(self):
        fecha_inicio = self.cleaned_data["fecha"]
        fecha_fin = self.cleaned_data["fecha_facturacion"]
        return validate_date_with_offset(fecha_inicio,fecha_fin,15)

class MantenimientoUpdateForm(forms.ModelForm):
    
    class Meta:
        model=Mantenimiento

        fields= "__all__"

        labels = {
                "detalle_mantenimiento":"Detalle Mantenimiento",
                "cod_mantenimiento":"Código",
                "fecha":"Fecha",
                "tipo_bien":"Tipo bien",
                "bien":"Nombre",
                "cod_bien":"Código bien",
                "ingreso_bien":"Ingreso de bienes",
                "egresos":"Partida Presupuestaria",
                "proveedor":"Razón social/Nombre",
                "subtotal":"",
                'valor_iva': '',
                'descuento':"",
                "total":"",
                "observaciones":"Observaciones",
                "anexo":"Anexos",
                
        }

        
        widgets={
            "detalle_mantenimiento": forms.Textarea(attrs={"class":"form-control",'rows':2}),
            "cod_mantenimiento":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
            "tipo_bien":forms.Select(attrs={"class":"form-control"}),
            "observaciones": forms.Textarea(attrs={'rows':2}),
            
            "tipo_proveedor":forms.Select(attrs={"class":"form-control"}),
            "proveedor":forms.HiddenInput(),
            "bien":forms.HiddenInput(),
            "ingreso_bien":forms.HiddenInput(),
            "egresos":forms.Select(attrs={"class":"form-control"}),

            'subtotal': forms.HiddenInput(),
            'descuento':forms.HiddenInput(),
            'valor_iva': forms.HiddenInput(),
            'total': forms.HiddenInput(),

            'anexo': forms.ClearableFileInput(),
            
        }

class MantenimientoFilter(django_filters.FilterSet):
    TIPO_BIEN_CHOICES=[("Activo","Activo"), ("Bien Sujeto a control administrativo","Bien Sujeto a control administrativo"),]
    TIPO_MANTENIMIENTO_CHOICES=[("Preventivo","Preventivo"), ("Correctivo","Correctivo"),]
    MANTENIMIENTO_CHOICES= [("Diario","Diario"), ("Quincenal","Quincenal"),("Mensual","Mensual"),("Trimestral","Trimestral"),("Cuatrimestral","Cuatrimestral"),("Quimestral","Quimestral"),("Semestral","Semestral"),("Anual","Anual"),("No Aplica","No Aplica")]

    cod_bien = django_filters.CharFilter(label="", widget=forms.NumberInput(attrs={'placeholder': 'Código Bien'}),method='filter_by_bien_cod')
    bien_nom = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={'placeholder': 'Nombre del Activo'}),method='filter_by_bien_nombre')
    tipo_bien = django_filters.ChoiceFilter(label="", empty_label="Tipo bien", choices=TIPO_BIEN_CHOICES)
    tipo_mantenimiento = django_filters.ChoiceFilter(label="", empty_label="Tipo mantenimiento", choices=TIPO_MANTENIMIENTO_CHOICES, method='filter_by_tipo_mantenimiento')
    cod_mantenimiento = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Código Mantenimiento'}))
    ubicacion = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Ubicación'}),method='filter_by_ubicacion')
    proveedor_id = django_filters.CharFilter(label="", widget=forms.NumberInput(attrs={'placeholder': 'RUC Proveedor'}),method='filter_by_ruc_ci')
    proveedor_nom = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={'placeholder': 'Nombre Proveedor'}),method='filter_by_razon_nombre')
    num_facturacion = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={'placeholder': 'N° Factura'}),method='filter_by_num_factura')
    centro_costos=django_filters.ModelChoiceFilter(label="", empty_label="Centro de Costos",queryset=Centro_Costos.objects.all(),method='filter_by_centro_costos')
    mantenimiento_tipo = django_filters.ChoiceFilter(label="", empty_label="Tipo Mantenimiento", choices=MANTENIMIENTO_CHOICES,method='filter_by_freq_mantenimiento')
    fecha=django_filters.DateFromToRangeFilter(label="",widget = RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}),attrs={'class': 'form-control '}))
    


    class Meta:
        model = Mantenimiento
        fields = [
                    'cod_bien',
                    'bien_nom',
                    'tipo_bien',
                    'tipo_mantenimiento',
                    'cod_mantenimiento',
                    'ubicacion',
                    'proveedor_id',
                    'proveedor_nom',
                    'num_facturacion',
                    'centro_costos',
                    'mantenimiento_tipo',
					'fecha',
                    
				]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_by_ruc_ci(self, queryset, name, value):
        return queryset.filter(Q(ingreso_bien__proveedor__ruc__icontains=value))

    def filter_by_razon_nombre(self, queryset, name, value):
        return queryset.filter(Q(ingreso_bien__proveedor__razon__icontains=value))

    def filter_by_bien_nombre(self, queryset, name, value):
        return queryset.filter(Q(bien__nombre__icontains=value))

    def filter_by_bien_cod(self, queryset, name, value):
        return queryset.filter(Q(bien__cod_bien__icontains=value))

    def filter_by_num_factura(self, queryset, name, value):
        return queryset.filter(Q(ingreso_bien__num_facturacion__icontains=value))

    def filter_by_tipo_mantenimiento(self, queryset, name, value):
        return queryset.filter(Q(bien__tipo_mantenimiento__icontains=value))

    def filter_by_ubicacion(self, queryset, name, value):
        return queryset.filter(Q(bien__ubicacion_Actual__icontains=value))
        
    def filter_by_centro_costos(self, queryset, name, value):
        return queryset.filter(Q(ingreso_bien__centro_costos__nombre__icontains=value))
        
    def filter_by_freq_mantenimiento(self, queryset, name, value):
        return queryset.filter(Q(bien__frecuencia_Mantenimiento__icontains=value))