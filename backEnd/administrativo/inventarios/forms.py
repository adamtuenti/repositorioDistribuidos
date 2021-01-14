from django import forms
from datetime import date
from . import models
from .models import Inventario, BienInventario
from .forms import *
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from django.db.models import Q
import django_filters
from django.contrib.postgres.forms.ranges import DateTimeRangeField, RangeWidget
from financiero.orden_pago.models import Centro_Costos

class InventarioForm(forms.ModelForm):
    
    class Meta:
        model=Inventario

        fields= "__all__"

        labels = {
                "cod_inventario":"Código",
                "fecha":"Fecha",
                "tipo_inventario":"Tipo de inventario",
                "tipo_bienes":"Tipo de bienes",
                "fecha_inicio":"Fecha de inicio",
                "fecha_fin":"Fecha final",
                "categoria_bien":"Categoría",
                'centro_costos': 'Centro de costos',
                "usuario_responsable": "Usuario responsable",

                # "nombre_responsable_cec":"Nombre del responsable",
                # "cargo_responsable_entrega":"Cargo responsable entrega",
                # "area_departamento_cec":"Área/Departamento",

                # "unidad_responsable":"Unidad responsable",
                # "nombre_responsable_unidad":"Nombre responsable unidad",
                # "area_departamento_unidad":"Área/Departamento",
                # "cargo_responsable_unidad":"Cargo",
                # "mail_responsable_unidad":"Mail",
                # "telefono_responsable_unidad":"Teléfono",
                # "celular_responsable_unidad":"Celular",

                "observaciones":"Observaciones",
                "anexo":"Anexos",
                
        }

        
        widgets={
            "cod_inventario":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),

            "tipo_inventario":forms.Select(attrs={"class":"form-control"}),
            "tipo_bienes":forms.Select(attrs={"class":"form-control"}),
            "fecha_inicio":forms.DateInput(attrs={'class':'form-control',"type":"date", "value":date.today}),
            "fecha_fin":forms.DateInput(attrs={'class':'form-control',"type":"date", "value":date.today}),
            "categoria_bien":forms.Select(attrs={"class":"form-control"}),
            "centro_costos":forms.Select(attrs={"class":"select form-control"}),
            "usuario_responsable":forms.TextInput(attrs={"class":"form-control", "type":"text"}),
            
            "observaciones": forms.Textarea(attrs={'rows':2}),
            'anexo': forms.ClearableFileInput(),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].initial = date.today
        self.fields['fecha'].disabled = True
        self.fields['cod_inventario'].disabled = True

class UpdateSuministroForm(forms.ModelForm):
    
    class Meta:
        model=Inventario

        fields= "__all__"

        labels = {
                "cod_inventario":"Código",
                "fecha":"Fecha",
                "tipo_inventario":"Tipo de inventario",
                "tipo_bienes":"Tipo de bienes",
                "fecha_inicio":"Fecha de inicio",
                "fecha_fin":"Fecha final",
                "categoria_bien":"Categoría",
                'centro_costos': 'Centro de costos',
                "usuario_responsable": "Usuario responsable",

                # "nombre_responsable_cec":"Nombre del responsable",
                # "cargo_responsable_entrega":"Cargo responsable entrega",
                # "area_departamento_cec":"Área/Departamento",

                # "unidad_responsable":"Unidad responsable",
                # "nombre_responsable_unidad":"Nombre responsable unidad",
                # "area_departamento_unidad":"Área/Departamento",
                # "cargo_responsable_unidad":"Cargo",
                # "mail_responsable_unidad":"Mail",
                # "telefono_responsable_unidad":"Teléfono",
                # "celular_responsable_unidad":"Celular",

                "observaciones":"Observaciones",
                "anexo":"Anexos",
                
        }

        
        widgets={
            "cod_inventario":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),

            "tipo_inventario":forms.Select(attrs={"class":"form-control"}),
            "tipo_bienes":forms.Select(attrs={"class":"form-control"}),
            "fecha_inicio":forms.DateInput(attrs={'class':'form-control',"type":"date", "value":date.today}),
            "fecha_fin":forms.DateInput(attrs={'class':'form-control',"type":"date", "value":date.today}),
            "categoria_bien":forms.Select(attrs={"class":"form-control"}),
            "centro_costos":forms.Select(attrs={"class":"select form-control"}),
            "usuario_responsable":forms.TextInput(attrs={"class":"form-control", "type":"text"}),
            
            "observaciones": forms.Textarea(attrs={'rows':2}),
            'anexo': forms.ClearableFileInput(),

        }

class BienInventarioForm(forms.ModelForm):

    class Meta: 
        model= BienInventario 
        exclude=()

BienInventarioFormset = inlineformset_factory(
    Inventario, BienInventario, form=BienInventarioForm,
    fields=['fecha_inventario','constatacion','observaciones','usuario_responsable','sede','estado','bien',],
     extra=1,can_delete=True
    )

class InventarioFilter(django_filters.FilterSet):
    TIPO_BIEN_CHOICES=[("Activo","Activo"), ("Bien Sujeto a control administrativo","Bien Sujeto a control administrativo"),]
    TIPO_INVENTARIO_CHOICES=[("Inicial", "Inicial"),("Final", "Final"),]
    CATEGORIA_CHOICES=[("Categoria1","Categoria1"), ("Categoria2","Categoria2"),]
    ESTADO_CHOICES = [("En buen estado", "En buen estado"),("Dañado", "Dañado"),("Dado de baja", "Dado de baja"),
    ("Por reparar", "Por reparar")]

    cod_bien = django_filters.CharFilter(label="", widget=forms.NumberInput(attrs={'placeholder': 'Código Bien'}),method='filter_by_bien_cod')
    bien_nom = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={'placeholder': 'Nombre del bien'}),method='filter_by_bien_nombre')
    tipo_bien = django_filters.ChoiceFilter(label="", empty_label="Tipo de bienes", choices=TIPO_BIEN_CHOICES, method='filter_by_tipo_bien')
    tipo_inventario = django_filters.ChoiceFilter(label="", empty_label="Tipo de inventario", choices=TIPO_INVENTARIO_CHOICES, method='filter_by_tipo_inventario')
    categoria = django_filters.ChoiceFilter(label="", empty_label="Categoría", choices=CATEGORIA_CHOICES, method='filter_by_categoria')
    centro_costos=django_filters.ModelChoiceFilter(label="", empty_label="Centro de Costos",queryset=Centro_Costos.objects.all(),method='filter_by_centro_costos')
    fecha = django_filters.DateFromToRangeFilter(label="",widget = RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}),attrs={'class': 'form-control '}))
    estado = django_filters.ChoiceFilter(label="", empty_label="Estado del bien", choices=ESTADO_CHOICES, method='filter_by_bien_estado')

    class Meta:
        model = Inventario
        fields = [
                    'cod_bien',
                    'bien_nom',
                    'tipo_bien',
                    'tipo_inventario',
                    'categoria',
                    'centro_costos',
					'fecha',
                    'estado',
                    
				]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_by_bien_nombre(self, queryset, name, value):
        instances = BienInventario.objects.filter(bien__nombre__icontains=value)
        inventories = [instance.inventario for instance in instances]
        return queryset.filter(Q(cod_inventario__in=inventories))

    def filter_by_bien_cod(self, queryset, name, value):
        instances = BienInventario.objects.filter(bien__cod_bien__icontains=value)
        inventories = [instance.inventario for instance in instances]
        return queryset.filter(Q(cod_inventario__in=inventories))

    def filter_by_bien_estado(self, queryset, name, value):
        instances = BienInventario.objects.filter(estado__icontains=value)
        inventories = [instance.inventario for instance in instances]
        return queryset.filter(Q(cod_inventario__in=inventories))

    def filter_by_tipo_inventario(self, queryset, name, value):
        return queryset.filter(Q(tipo_inventario__icontains=value))

    def filter_by_categoria(self, queryset, name, value):
        return queryset.filter(Q(categoria_bien__icontains=value))        
        
    def filter_by_centro_costos(self, queryset, name, value):
        return queryset.filter(Q(centro_costos__nombre__icontains=value))

    def filter_by_tipo_bien(self, queryset, name, value):
        return queryset.filter(Q(tipo_bienes__icontains=value))