from django import forms
from .models import Producto
import django_filters
from . import models
from datetime import date

class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)

    class Meta:
        model= Producto
        fields=[
            'cod_producto',
            'nombre',
            'fecha',
            'tipo',
            'unidad_medida',
            'estado',
            'dias_entrega',
            'controlable',
            'iva',
            'punto_reorden',
            'tolerancia',
            'cant_maxima',
            'stock_actual',
            'descripcion',
            ]

        labels={
            'cod_producto':'Codigo de Producto',
            'nombre':'Nombre del Producto',
            'fecha':'Fecha',
            'tipo':'Tipo de Producto',
            'unidad_medida':'Unidad de Medida',
            'estado':'Estado',
            'dias_entrega':'Dias de Entrega',
            'controlable':'Controlable',
            'iva':'IVA',
            'punto_reorden':'Punto de Reorden',
            'tolerancia':'Tolerancia',
            'cant_maxima':'Cantidad Máxima',
            'stock_actual':'Stock Actual',
            'descripcion':"Descripción",
            }

        widgets={
            # "cod_producto":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "cod_producto":forms.TextInput(attrs={"class":"form-control",'readonly': True}),

            "nombre":forms.TextInput(attrs={"class":"form-control"}),
			"tipo":forms.Select(attrs={"class":"form-control"}),
			"unidad_medida":forms.Select(attrs={"class":"form-control"}),
			"estado":forms.Select(attrs={"class":"form-control"}),
            # "fecha":forms.TextInput(attrs={"class":"form-control","type":"date",'readonly':'readonly'}),
			"fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),

            "controlable":forms.RadioSelect,
            "iva":forms.RadioSelect,

            "dias_entrega":forms.TextInput(attrs={"class":"form-control","type":"number"}),
			"punto_reorden":forms.TextInput(attrs={"class":"form-control","type":"number"}),
			"tolerancia":forms.TextInput(attrs={"class":"form-control","type":"number"}),
			"cant_maxima":forms.TextInput(attrs={"class":"form-control","type":"number"}),
			"stock_actual":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "descripcion": forms.Textarea(attrs={'rows':2}),


        }


        class PropertyModelChoiceField(forms.ModelChoiceField):
            def label_from_instance(self, obj):
                return obj.type


class ProductoUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model= Producto
        fields=[
            'cod_producto',
            'nombre',
            'fecha',
            'tipo',
            'unidad_medida',
            'estado',
            'dias_entrega',
            'controlable',
            'iva',
            'punto_reorden',
            'tolerancia',
            'cant_maxima',
            'stock_actual',
            'descripcion',
            ]

        labels={
            'cod_producto':'Codigo de Producto',
            'nombre':'Nombre del Producto',
            'fecha':'Fecha',
            'tipo':'Tipo de Producto',
            'unidad_medida':'Unidad de Medida',
            'estado':'Estado',
            'dias_entrega':'Dias de Entrega',
            'controlable':'Controlable',
            'iva':'IVA',
            'punto_reorden':'Punto de Reorden',
            'tolerancia':'Tolerancia',
            'cant_maxima':'Cantidad Máxima',
            'stock_actual':'Stock Actual',
            'descripcion':"Descripción",
            }

        widgets={
            # "cod_producto":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "cod_producto":forms.TextInput(attrs={"class":"form-control",'readonly': True}),

            "nombre":forms.TextInput(attrs={"class":"form-control"}),
			"tipo":forms.Select(attrs={"class":"form-control"}),
			"unidad_medida":forms.Select(attrs={"class":"form-control"}),
			"estado":forms.Select(attrs={"class":"form-control"}),
            # "fecha":forms.TextInput(attrs={"class":"form-control","type":"date",'readonly':'readonly'}),
			"fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),

            "controlable":forms.RadioSelect,
            "iva":forms.RadioSelect,

            "dias_entrega":forms.TextInput(attrs={"class":"form-control","type":"number"}),
			"punto_reorden":forms.TextInput(attrs={"class":"form-control","type":"number"}),
			"tolerancia":forms.TextInput(attrs={"class":"form-control","type":"number"}),
			"cant_maxima":forms.TextInput(attrs={"class":"form-control","type":"number"}),
			"stock_actual":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "descripcion": forms.Textarea(attrs={'rows':2}),


        }


        class PropertyModelChoiceField(forms.ModelChoiceField):
            def label_from_instance(self, obj):
                return obj.type



class ProductoFilter(django_filters.FilterSet):
    TIPO_PRODUCTO_CHOICES = [("Bienes","Bienes"), ("Servicios","Servicios"),]
    UNIDAD_MEDIDA_CHOICES = [("Unidad","Unidad"), ("Caja","Caja"), ("Caneca","Caneca"), ("Resma","Resma"), ("Paquete","Paquete"), ("Galón","Galón"), ("Litro","Litro"), ("Otros","Otros"),]
    ESTADO_CHOICES = [("Activo","Activo"), ("Inactivo","Inactivo"),]
    CONTROLABLE_CHOICES = [("SI","SI"), ("NO","NO"),]
    STATE_CHOICES = (
        (True, u'Si'),
        (False, u'No'),
    )

    cod_producto = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Código del Producto'}))
    nombre = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Nombre del Producto'}))
    tipo= django_filters.ChoiceFilter(label="", empty_label="Tipo de Producto", choices=TIPO_PRODUCTO_CHOICES)
    unidad_medida = django_filters.ChoiceFilter(label="", empty_label="Unidad de Medida", choices=UNIDAD_MEDIDA_CHOICES)
    estado = django_filters.ChoiceFilter(label="", empty_label="Tipo de Rubro", choices=ESTADO_CHOICES)
    controlable = django_filters.ChoiceFilter(label="", empty_label="Controlable", choices=STATE_CHOICES)
    iva = django_filters.ChoiceFilter(label="", empty_label="IVA", choices=STATE_CHOICES)


class Meta:
    model=models.Producto
    fields= [
        'cod_producto',
        'nombre',
        'tipo',
        'unidad_medida',
        'estado',
        'dias_entrega',
        'controlable',
        'iva',
        'punto_reorden',
        'tolerancia',
        'cant_maxima',
        'stock_actual',
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)