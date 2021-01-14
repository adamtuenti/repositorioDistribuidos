from dal import autocomplete
from . import models
from django import forms
import django_filters
from .models import *
from django.forms import modelformset_factory
from datetime import date
from django.forms.models import inlineformset_factory
from .models import Suministro_Egreso, Suministro_EgresoFile
from ventas.validaciones import validate_porcentaje, validate_positive, validate_anexo_corp
from django.contrib.postgres.forms.ranges import DateTimeRangeField, RangeWidget
import datetime
from datetime import date
from ventas.validaciones import validate_date_with_offset
from django.db.models import Q


class Suministro_EgresoForm(forms.ModelForm):
    class Meta:
        model=Suministro_Egreso

        fields= "__all__"

        labels = {
                "cod_suministro_egreso":"Código",
                "fecha":"Fecha",
                "fecha_egreso":"Fecha Egreso",
                "proveedor":"Razón social/Nombre",
                "tipo_consumo":"Tipo de Consumo",
                "cantidad_participantes":"Cantidad de Participantes",
                'usuario': 'Usuario',
                "area":"Área Requerida",
                "observaciones":"Observaciones",
                "producto":"",
                'cantidad_solicitada': '',
                "cantidad_despachada":"",
                
        }

        
        widgets={
            "evento":forms.HiddenInput(),
            "cod_suministro_egreso":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
            "fecha_egreso":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
            # "evento":forms.HiddenInput(),
            "observaciones": forms.Textarea(attrs={'rows':2}),
            
        }


class FileForm(forms.ModelForm):

    class Meta: 
        model= Suministro_EgresoFile 
        exclude=()

FileFormset = inlineformset_factory(
    Suministro_Egreso, Suministro_EgresoFile, form=FileForm,
    fields=['file'],widgets={"file":forms.ClearableFileInput(attrs={'class':'proformaf','accept':'image/*,.pdf'})},
     extra=1,can_delete=True
    )



class Suministro_EgresoFilter(django_filters.FilterSet):

    CONSUMO_CHOICES = [("Recursos del Evento", "Recursos del Evento"),("Consumo Interno", "Consumo Interno"),]
    AREA_CHOICES =[("Dirección","Dirección") , ("Académico","Académico") , ("Comercial","Comercial") , ("Logística","Logística") , ("Administrativo-Financiero","Administrativo-Financiero") , ("Control Académico","Control Académico") , ("Calidad","Calidad") , ("Marketing y Publicidad","Marketing y Publicidad") , ("TIC's","TIC's"),]

    cod_suministro_egreso = django_filters.CharFilter(lookup_expr='icontains', label='', widget=forms.TextInput(attrs={'placeholder': 'Código del Producto'}))    
    fecha=django_filters.DateFilter(field_name='fecha', label='', widget=forms.DateInput(attrs={'placeholder':'Fecha Calificación',"class":"textbox-n", "onfocus":"(this.type='date')"}))
    fecha_egreso=django_filters.DateFromToRangeFilter(label="",widget = RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}),attrs={'class': 'form-control '}))
    
    evento__nombre=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Nombre evento'}))
    evento__codigo_evento=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Código evento'}))
    usuario = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Usuario'}))
    tipo_consumo=django_filters.ChoiceFilter(label="", empty_label="Tipo Consumo", choices=CONSUMO_CHOICES)
    area=django_filters.ChoiceFilter(label="", empty_label="Área Requerida", choices=AREA_CHOICES)
   


    class Meta:
        model = Suministro_Egreso
        fields = [
                    "cod_suministro_egreso",
                    'evento__nombre',
                    'evento__codigo_evento',
					"fecha",
                    "fecha_egreso",
				]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_by_ruc_ci(self, queryset, name, value):
        return queryset.filter(Q(proveedor__ruc__icontains=value))

    def filter_by_razon_nombre(self, queryset, name, value):
        return queryset.filter(Q(proveedor__razon__icontains=value))

    
class ProductoSuministroEgresoForm(forms.ModelForm):

    class Meta: 
        model= ProductoSuministroEgreso 
        exclude=()

SuministroEgresoProductoFormset = inlineformset_factory(
    Suministro_Egreso, ProductoSuministroEgreso, form=ProductoSuministroEgresoForm,
    fields=['producto','cantidad_solicitada','cantidad_despachada'],
     extra=1,can_delete=True
    )

