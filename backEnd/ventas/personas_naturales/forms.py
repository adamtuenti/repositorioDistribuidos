from django import forms
from django.forms import ModelForm
from .models import Persona_Natural

class Natural_NuevoForm(forms.ModelForm):
	class Meta:
		model = Persona_Natural
		fields = ['cedula','apellidos','nombres','pais','fecha_nacimiento','tel_domicilio','celular','email','ci_domicilio','dir_domicilio','nivel_estudio',
		"institucion_primaria","progreso_primaria","institucion_secundaria","progreso_secundaria",
		'ti_tercernivel','un_tercernivel',"pais_estudio_tercer",'tercer_progreso','ti_postgrado','un_postgrado',"pais_estudio_postgrado",'postgrado_progreso','profesion','forma_trabajo','empresa','cargo','ci_trabajo','area',
		'dir_trabajo','tel_trabajo','medios', 'novedad_medios','genero','celular2','email2','email_empresa','motivo_eliminacion'
		
		
		]
		
		widgets = {
			'cedula': forms.TextInput(attrs={'type':'number'}),
			'nivel_estudio': forms.RadioSelect(attrs={'onclick':'nivel_de_estudio()','class':'required'}),
			'fecha_nacimiento': forms.DateInput(attrs={'type':'date'}),
			'novedad_medios': forms.Textarea(attrs={'rows':2}),
		}
		