import django_filters
from django import forms
from .models import *
from ..personas_juridicas.models import TipoEmpresa
from django.contrib.postgres.forms.ranges import DateTimeRangeField, RangeWidget
from ..interesados.models import CanalContacto
from django.db.models import Q
from seguridad.models import *

class SeguimientoEmpresaFilter(django_filters.FilterSet):

    seguimientoempresaeventos__evento__nombre=django_filters.CharFilter(label="",widget=forms.TextInput(attrs={'placeholder':'Nombre evento'}),method='filter_by_evento_nombre')
    seguimientoempresaeventos__evento__codigo_evento=django_filters.CharFilter(label="",widget=forms.TextInput(attrs={'placeholder':'Código evento'}),method='filter_by_evento_codigo')
    juridica__nombre=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Razon Social'}))
    juridica__ruc=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'RUC'}))
    estado=django_filters.ChoiceFilter(empty_label="Estado del seguimiento",label='',choices=EstadoSeguimiento.objects.all().values_list('pk','nombre'))
    canal=django_filters.ChoiceFilter(empty_label="Canal de Contacto",label='',choices=CanalContacto.objects.all().values_list('pk','nombre'))
    tipo_evento=django_filters.ChoiceFilter(empty_label="Tipo de Evento",label='',choices=TIPO_EVENTO)
    tipo_oferta=django_filters.ChoiceFilter(empty_label="Tipo de Oferta",label='',choices=TIPO_OFERTA)
    juridica__tipo_empresa=django_filters.ChoiceFilter(empty_label="Tipo de Empresa",label='',choices=TipoEmpresa.objects.all().values_list('pk','nombre'))
    fecha_seguimiento__gte = django_filters.DateFilter(label="",field_name='fecha_seguimiento', lookup_expr='gte',widget=forms.DateInput(attrs={'placeholder':'Fecha Seguimiento Inicial','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
    fecha_seguimiento__lte = django_filters.DateFilter(label="",field_name='fecha_seguimiento', lookup_expr='lte',widget=forms.DateInput(attrs={'placeholder':'Fecha Seguimiento Final','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
    fecha__gte = django_filters.DateFilter(label="",field_name='fecha', lookup_expr='gte',widget=forms.DateInput(attrs={'placeholder':'Fecha Registro Inicial','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
    fecha__lte = django_filters.DateFilter(label="",field_name='fecha', lookup_expr='lte',widget=forms.DateInput(attrs={'placeholder':'Fecha Registro Final','onfocus':"(this.type='date')",'onfocusout':"DateToText(this)",'class':'fecha'}))
    exito=django_filters.ChoiceFilter(empty_label="Éxito",label='',choices=EXITO_CHOICES)
    roles=RolPermisoUsuario.objects.filter(modulo="Comercial").values_list('usuario', flat=True)
    users=Usuario.objects.filter(pk__in=roles)
    added_by=django_filters.ModelChoiceFilter(empty_label="Asesor/a",label="",queryset=users)
    class Meta:
        model = SeguimientoEmpresa
        
        fields = "__all__"
    
    def filter_by_evento_nombre(self, queryset, name, value):
        return queryset.filter(Q(seguimientoempresaeventos__evento__nombre__icontains=value)).distinct()
    
    def filter_by_evento_codigo(self, queryset, name, value):
        return queryset.filter(Q(seguimientoempresaeventos__evento__codigo_evento__icontains=value)).distinct()

       

class SeguimientoNaturalFilter(django_filters.FilterSet):
    fecha_seguimiento= django_filters.DateFromToRangeFilter(field_name ='fecha_seguimiento',widget = RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}),attrs={'class': 'form-control '}))
    fecha_registro= django_filters.DateFromToRangeFilter(field_name ='fecha_registro',widget = RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}),attrs={'class': 'form-control '}))
    cod_evento=django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Código Evento'}))
    nombre_evento=django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Nombre Evento'}))
    estado_seguimiento=django_filters.ChoiceFilter(label="", empty_label="Estado",choices = ESTADO_CHOICES)
    canal_de_contacto=django_filters.ModelChoiceFilter(label="", empty_label="Canal de contacto",queryset=CanalContacto.objects.all())
    exito=django_filters.ChoiceFilter(label="", empty_label="Éxito",choices = EXITO_CHOICES)
    pers_natural__cedula= django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Cédula Participante'}))
    pers_natural__nombres= django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Nombre Participante'}))
    tipo_inscripcion= django_filters.ChoiceFilter(label="", empty_label="Tipo Inscripcion",choices = INSCRIPCION_CHOICES)
    roles=RolPermisoUsuario.objects.filter(modulo="Comercial").values_list('usuario', flat=True)
    users=Usuario.objects.filter(pk__in=roles)
    asesor=django_filters.ModelChoiceFilter(label="", empty_label="Asesor",queryset=users)
    #asesor=django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Asesor'}))


    class Meta:
        model = Seguimiento_PersonaNatural
        
        fields = "__all__"

class SeguimientoInteresadosFilter(django_filters.FilterSet):
    fecha_seguimiento= django_filters.DateFromToRangeFilter(field_name ='fecha_seguimiento',widget = RangeWidget(forms.DateInput(),attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')",'class': 'form-control '}))
    fecha_registro= django_filters.DateFromToRangeFilter(field_name ='fecha_registro',widget = RangeWidget(forms.DateInput(attrs={'placeholder':'Fecha',"class":"textbox-n", "onfocus":"(this.type='date')"}),attrs={'class': 'form-control '}))
    cod_evento=django_filters.CharFilter(label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Código Evento'}))
    nombre_evento=django_filters.CharFilter(lookup_expr='icontains',label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Nombre Evento'}))
    estado_seguimiento=django_filters.ChoiceFilter(label="", empty_label="Estado",choices = ESTADO_CHOICES)
    canal_de_contacto=django_filters.ModelChoiceFilter(label="", empty_label="Canal de contacto",queryset=CanalContacto.objects.all())
    exito=django_filters.ChoiceFilter(label="", empty_label="Éxito",choices = EXITO_CHOICES)
    asesor=django_filters.ModelChoiceFilter(label="", empty_label="Asesor",queryset=SeguimientoNaturalFilter.users)
    inters__nombre= django_filters.CharFilter(lookup_expr='icontains',label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Nombre Participante'}))
    inters__apellido= django_filters.CharFilter(lookup_expr='icontains',label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Apellido Participante'}))
    inters__celular= django_filters.CharFilter(lookup_expr='icontains',label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Celular Participante'}))
    inters__correo= django_filters.CharFilter(lookup_expr='icontains',label = "",widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Correo Electrónico Participante'}))

    
    estado_participante= django_filters.ChoiceFilter(label="", empty_label="Estado Participante",choices = Seguimiento_PersonaNatural.ESTADO_PARTICIPANTE_CHOICES)

    class Meta:
        model = Seguimiento_Interesados
        fields = "__all__"