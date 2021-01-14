from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms

def validate_positivo(value):
	if(int(value)<0):
		raise ValidationError(
			_("Valor no puede ser negativo"),
			code="valor_negativo"
		)

def validate_porcentaje(valor):
	if(valor==None):
		return valor
	elif(valor<0):
		raise forms.ValidationError("El porcentaje no puede ser negativo")
	elif(valor>100):
		raise forms.ValidationError("El porcentaje no puede ser mayor a 100")
	else:
		return valor