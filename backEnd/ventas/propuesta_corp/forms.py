from django import forms
from .models import PropuestaCorporativo,PropuestaFile
from ventas.personas_juridicas.models import Sector
from ventas.validaciones import validate_porcentaje, validate_positive, validate_anexo_corp
from dal import autocomplete
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory

class PropuestaCorporativoForm(forms.ModelForm):

   

    class Meta:
        model = PropuestaCorporativo

        fields=[
            'cod_propuesta',
            'version',
            'ruc_ci',
            'razon_nombres',
            'tipo_empresa',
            'reporte',
            'estado',
            'sector',
            'fecha_solicitud',
            'numero_participantes',
            'total_horas',
            'cantidad_cursos',
            'monto_propuesta',
            'margen_contribucion',
            'utilidad_esperada',
            'exito',
            'lugar',
            'servicios_incluidos',
            'fecha_inicio_estimada',
            'observacion',
            'area_capacitacion',
            'asesor',
            'fecha_envio',
            'fecha_respuesta',
            'active'
        ]

        labels = {
            'cod_propuesta':'Código de la propuesta',
            'ruc_ci': 'RUC',
            'razon_nombres': 'Razón social',
            'version':'Versión',
            'tipo_empresa':'Tipo de Empresa',
            'reporte':'Reporte de contacto asociado',
            'estado':'Estado',
            'sector':'Sector',
            'fecha_solicitud':'Fecha de solicitud',
            'numero_participantes':'Número de participantes',
            'total_horas':'Total horas',
            'cantidad_cursos':'Cantidad de Cursos',
            'monto_propuesta':'Monto propuesta',
            'margen_contribucion':'% Margen de contribución',
            'utilidad_esperada':'Utilidad esperada',
            'exito':'% Éxito',
            'lugar':'Lugar',
            'servicios_incluidos':'Servicios incluidos',
            'fecha_inicio_estimada':'Fecha de inicio estimada',
            'observacion':'Observación',
            'area_capacitacion':'Área de capacitación ',
            'asesor': 'Asesor',
            'fecha_envio':"Fecha de Envio",
            'fecha_respuesta':'Fecha de Respuesta',
        }
        
        widgets={
            'reporte':autocomplete.ModelSelect2(url='reporte-autocomplete'),
            'razon_nombres': forms.Select(attrs={'class': 'form-control select3'}),
            'ruc_ci': forms.Select(attrs={'class': 'form-control select3'}),
            'observacion':forms.Textarea(attrs={'rows':2}),
            'fecha_solicitud':forms.DateInput(attrs={'type':'date'}),
            'fecha_inicio_estimada':forms.DateInput(attrs={'type':'date'}),
            'fecha_envio':forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta':forms.DateInput(attrs={'type':'date'}),
            'exito':forms.NumberInput(attrs={'type':'number'}),
            'active':forms.HiddenInput()
        }
    def __init__(self, *args, **kwargs):
        super(PropuestaCorporativoForm, self).__init__(*args, **kwargs)
        self.fields['asesor'].disabled = True
        self.fields['version'].disabled = True
        self.fields['version'].initial = 1
        self.fields['sector'].disabled = True
        self.fields['tipo_empresa'].disabled = True
        self.fields['reporte'].required = True

    def clean_exito(self):
        exito = self.cleaned_data["exito"]
        return validate_porcentaje(exito)
    
    def clean_margen_contribucion(self):
        margen = self.cleaned_data["margen_contribucion"]
        return validate_porcentaje(margen)
    

class PropuestaCorporativoUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PropuestaCorporativoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['sector'].disabled = True
        self.fields['tipo_empresa'].disabled = True
        self.fields['reporte'].required = True
        self.fields['asesor'].disabled = True

    class Meta:
        model = PropuestaCorporativo

        fields=[
            'cod_propuesta',
            'version',
            'ruc_ci',
            'razon_nombres',
            'tipo_empresa',
            'reporte',
            'estado',
            'sector',
            'fecha_solicitud',
            'numero_participantes',
            'total_horas',
            'cantidad_cursos',
            'monto_propuesta',
            'margen_contribucion',
            'utilidad_esperada',
            'exito',
            'lugar',
            'servicios_incluidos',
            'fecha_inicio_estimada',
            'observacion',
            'area_capacitacion',
            'asesor',
            'fecha_envio',
            'fecha_respuesta',
            'active'
        ]

        labels = {
            'cod_propuesta':'Código de la propuesta',
            'ruc_ci': 'RUC',
            'razon_nombres': 'Razón social',
            'version':'Versión',
            'tipo_empresa':'Tipo de Empresa',
            'reporte':'Reporte de contacto asociado',
            'estado':'Estado',
            'sector':'Sector',
            'fecha_solicitud':'Fecha de solicitud',
            'numero_participantes':'Número de participantes',
            'total_horas':'Total horas',
            'cantidad_cursos':'Cantidad de Cursos',
            'monto_propuesta':'Monto propuesta',
            'margen_contribucion':'% Margen de contribución',
            'utilidad_esperada':'Utilidad esperada',
            'exito':'% Éxito',
            'lugar':'Lugar',
            'servicios_incluidos':'Servicios incluidos',
            'fecha_inicio_estimada':'Fecha de inicio estimada',
            'observacion':'Observación',
            'area_capacitacion':'Área de capacitación ',
            'asesor': 'Asesor',
            'fecha_envio':"Fecha de Envio",
            'fecha_respuesta':'Fecha de Respuesta'
        }
        
        widgets={
            'reporte':autocomplete.ModelSelect2(url='reporte-autocomplete'),
            'razon_nombres': forms.Select(attrs={'class': 'form-control select3'}),
            'ruc_ci': forms.Select(attrs={'class': 'form-control select3'}),
            'observacion':forms.Textarea(attrs={'rows':2}),
            'fecha_solicitud':forms.DateInput(attrs={'type':'date'}),
            'fecha_inicio_estimada':forms.DateInput(attrs={'type':'date'}),
            'fecha_envio':forms.DateInput(attrs={'type':'date'}),
            'fecha_respuesta':forms.DateInput(attrs={'type':'date'}),
            'exito':forms.NumberInput(attrs={'type':'number'}),
            'active':forms.HiddenInput()
        }
    
    def clean_exito(self):
        exito = self.cleaned_data["exito"]
        return validate_porcentaje(exito)
    
    def clean_margen_contribucion(self):
        margen = self.cleaned_data["margen_contribucion"]
        return validate_porcentaje(margen)
    
class FileForm(forms.ModelForm):

    class Meta: 
        model= PropuestaFile 
        exclude=()



FileFormset = inlineformset_factory(
    PropuestaCorporativo, PropuestaFile, form=FileForm,
    fields=['file'],widgets={"file":forms.ClearableFileInput(attrs={'class':' anexo','accept':'image/*,.pdf,.xlsx,.xlsm,.xlsb,.xltx,.xltm,.xls,.xlt,.xml,.xlam,.xla,.xlw,.XLR,csv '})},
     extra=1,can_delete=True
    )
