from django import forms
from .models import Proforma, ProformaFile
from dal import autocomplete
from ventas.validaciones import validate_porcentaje, validate_positive, validate_anexo_corp
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory

class ProformaForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProformaForm, self).__init__(*args, **kwargs)
		self.fields['version'].disabled = True
		self.fields['version'].initial = 1
		self.fields['sector'].disabled = True
		self.fields['tipoEmpresa'].disabled = True
        #self.fields['ruc_ci'].disabled = True
        #self.fields['razon_nombres'].disabled = True

	class Meta:
		model=Proforma

		fields=[
			'codigo',
			'tipo_cliente',
			'ruc_ci',
            'razon_nombres',
			'version',
			'asesor',
			'tipoEmpresa',
			#"empresa",
			'sector',
			'fechaSolicitud',
			'fechaEnvio',
			'numeroParticipantes',
			'horas',
			'cantidadCursos',
			'estado',
			'porcentExito',
			'porcentDesc',
			'montoProforma',
			'montoDesc',
			'observacion',
			'fechaRespuesta',
			'montoAceptado',
			'montoEjecutado',
			'montoPorEjecutarse',
			'active',
		]

		labels={
			'codigo': 'Código',
			'tipo_cliente': 'Cliente',
			'ruc_ci': 'RUC',
            'razon_nombres': 'Razón social',
			'version':'Versión',
			'asesor':'Asesor',

			#'empresa':'Empresa',
			
			'tipoEmpresa':'Tipo Empresa',
			'sector':'Sector',
			'fechaSolicitud':'Fecha Solicitud',
			'fechaEnvio':'Fecha Envío',
			'numeroParticipantes':'Número Participantes',
			'horas':'Total Horas',
			'cantidadCursos':'Cantidad Cursos',

			'porcentExito':"% Éxito",
			'porcentDesc':"% Descuento",
			'montoProforma':'Monto Proforma',
			'montoDesc':'Monto Descuento',
			'observacion':'Observación',
			'fechaRespuesta':'Fecha Respuesta',
			'montoAceptado':'Monto Aceptado',
			'montoEjecutado':'Monto Ejecutado',
			'montoPorEjecutarse':'Monto por Ejecutarse',

		}

		widgets={
			'codigo': forms.TextInput(attrs={'class':'form-control'}),
			'version': forms.NumberInput(attrs={'class':'form-control','min': 0}),

			'asesor': forms.TextInput(attrs={'class':'form-control'}),

			
			'fechaSolicitud': forms.DateInput(attrs={'class':'form-control',"type":"date"}),
			'fechaEnvio':forms.DateInput(attrs={'class':'form-control',"type":"date"}),
			'numeroParticipantes': forms.NumberInput(attrs={'class':'form-control'}),
			'horas': forms.NumberInput(attrs={'class':'form-control'}),
			'cantidadCursos': forms.NumberInput(attrs={'class':'form-control'}),
			'estado':forms.Select(choices=[(None,"---------"),("Aceptada","Aceptada"),
				("No aceptada","No aceptada"), ("Seguimiento","Seguimiento") ,("Por Enviar","Por Enviar")],
				attrs={'class':'form-control', "id":"seleccion","onchange":"run()"}),
			'porcentExito': forms.NumberInput(attrs={'class':'form-control','min': 0, 'max': 100}),
			'porcentDesc': forms.NumberInput(attrs={'class':'form-control','min': 0, 'max': 100}),
			'montoProforma': forms.NumberInput(attrs={'class':'form-control','min': 0}),
			'montoDesc': forms.NumberInput(attrs={'class':'form-control','min': 0}),
			'observacion': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
			'fechaRespuesta': forms.DateInput(attrs={'class':'form-control',"type":"date"}),
			'montoAceptado': forms.NumberInput(attrs={'class':'form-control','min': 0}),
			'montoEjecutado': forms.NumberInput(attrs={'class':'form-control','min': 0}),
			'montoPorEjecutarse': forms.NumberInput(attrs={'class':'form-control','min': 0}),
			'razon_nombres': forms.Select(attrs={'class': 'form-control select2'}),
            'ruc_ci': forms.Select(attrs={'class': 'form-control select2'}),
			'active':forms.HiddenInput()
		}


	def clean_porcentExito(self):
		exito = self.cleaned_data["porcentExito"]
		return validate_porcentaje(exito)
	
	def clean_porcentDesc(self):
		desc = self.cleaned_data["porcentDesc"]
		return validate_porcentaje(desc)

class ProformaUpdateForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProformaUpdateForm, self).__init__(*args, **kwargs)
		
		self.fields['sector'].disabled = True
		self.fields['tipoEmpresa'].disabled = True
        #self.fields['ruc_ci'].disabled = True
        #self.fields['razon_nombres'].disabled = True

	class Meta:
		model=Proforma

		fields=[
			'codigo',
			'tipo_cliente',
			'ruc_ci',
            'razon_nombres',
			'version',
			'asesor',
			'tipoEmpresa',
			#"empresa",
			'sector',
			'fechaSolicitud',
			'fechaEnvio',
			'numeroParticipantes',
			'horas',
			'cantidadCursos',
			'estado',
			'porcentExito',
			'porcentDesc',
			'montoProforma',
			'montoDesc',
			'observacion',
			'fechaRespuesta',
			'montoAceptado',
			'montoEjecutado',
			'montoPorEjecutarse',
			'active',
		]

		labels={
			'codigo': 'Código',
			'tipo_cliente': 'Cliente',
			'ruc_ci': 'RUC',
            'razon_nombres': 'Razón social',
			'version':'Versión',
			'asesor':'Asesor',

			#'empresa':'Empresa',
			
			'tipoEmpresa':'Tipo Empresa',
			'sector':'Sector',
			'fechaSolicitud':'Fecha Solicitud',
			'fechaEnvio':'Fecha Envío',
			'numeroParticipantes':'Número Participantes',
			'horas':'Total Horas',
			'cantidadCursos':'Cantidad Cursos',

			'porcentExito':"% Éxito",
			'porcentDesc':"% Descuento",
			'montoProforma':'Monto Proforma',
			'montoDesc':'Monto Descuento',
			'observacion':'Observación',
			'fechaRespuesta':'Fecha Respuesta',
			'montoAceptado':'Monto Aceptado',
			'montoEjecutado':'Monto Ejecutado',
			'montoPorEjecutarse':'Monto por Ejecutarse',

		}

		widgets={
			'codigo': forms.TextInput(attrs={'class':'form-control'}),
			'version': forms.NumberInput(attrs={'class':'form-control','min': 0}),

			'asesor': forms.TextInput(attrs={'class':'form-control'}),

			
			'fechaSolicitud': forms.DateInput(attrs={'class':'form-control',"type":"date"}),
			'fechaEnvio':forms.DateInput(attrs={'class':'form-control',"type":"date"}),
			'numeroParticipantes': forms.NumberInput(attrs={'class':'form-control'}),
			'horas': forms.NumberInput(attrs={'class':'form-control'}),
			'cantidadCursos': forms.NumberInput(attrs={'class':'form-control'}),
			'estado':forms.Select(choices=[(None,"---------"),("Aceptada","Aceptada"),
				("No aceptada","No aceptada"), ("Seguimiento","Seguimiento") ,("Por Enviar","Por Enviar")],
				attrs={'class':'form-control', "id":"seleccion","onchange":"run()"}),
			'porcentExito': forms.NumberInput(attrs={'class':'form-control','min': 0, 'max': 100}),
			'porcentDesc': forms.NumberInput(attrs={'class':'form-control','min': 0, 'max': 100}),
			'montoProforma': forms.NumberInput(attrs={'class':'form-control','min': 0,'step':'0.01','value':'0.00'}),
			'montoDesc': forms.NumberInput(attrs={'class':'form-control','min': 0}),
			'observacion': forms.Textarea(attrs={'class':'form-control', 'rows':2}),
			'fechaRespuesta': forms.DateInput(attrs={'class':'form-control',"type":"date"}),
			'montoAceptado': forms.NumberInput(attrs={'class':'form-control','min': 0}),
			'montoEjecutado': forms.NumberInput(attrs={'class':'form-control','min': 0}),
			'montoPorEjecutarse': forms.NumberInput(attrs={'class':'form-control','min': 0}),
			'razon_nombres': forms.Select(attrs={'class': 'form-control select2'}),
            'ruc_ci': forms.Select(attrs={'class': 'form-control select2'}),
			'active':forms.HiddenInput()
		}


	def clean_porcentExito(self):
		exito = self.cleaned_data["porcentExito"]
		return validate_porcentaje(exito)
	
	def clean_porcentDesc(self):
		desc = self.cleaned_data["porcentDesc"]
		return validate_porcentaje(desc)


class FileForm(forms.ModelForm):

    class Meta: 
        model= ProformaFile 
        exclude=()

FileFormset = inlineformset_factory(
    Proforma, ProformaFile, form=FileForm,
    fields=['file'],widgets={"file":forms.ClearableFileInput(attrs={'class':'proformaf','accept':'image/*,.pdf'})},
     extra=1,can_delete=True
    )
