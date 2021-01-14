from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms

def validate_cedula(value):
	if(len(value)!=10 or not value.isdigit()):
		raise ValidationError(
            _('%(value)s no es una cédula válida'),
            code="invalid",
            params={'value': value},
        )
	else:
		impares = int(value[1]) + int(value[3]) + int(value[5]) + int(value[7])
		pares = 0
		for i in range(0,9):
			if(i%2==0):
				res = int(value[i])*2
				if(res>=10):
					res = res-9
				pares = pares+res
		total = impares+pares
		dig_validador = (((total+10)//10)*10)-total
		if(dig_validador==10):
			dig_validador = 0
		if (not(int(value[0:2])>=1 and int(value[0:2])<=24 and int(value[-1])==dig_validador)):
			raise ValidationError(
	            _('%(value)s no es una cédula válida'),
	            code="invalid",
	            params={'value': value},
	        )

def ruc_natural(value):
	impares = int(value[1]) + int(value[3]) + int(value[5]) + int(value[7])
	pares = 0
	for i in range(0,9):
		if(i%2==0):
			res = int(value[i])*2
			if(res>=10):
				res = res-9
			pares = pares+res
	total = impares+pares
	dig_validador = (((total+10)//10)*10)-total
	if(dig_validador==10):
		dig_validador = 0
	return int(value[0:2])>=1 and int(value[0:2])<=24 and int(value[9])==dig_validador and int(value[10:13])>=1

#Tercer dígito 9
def ruc_juridica(value):
	d1 = int(value[0])*4
	d2 = int(value[1])*3
	d3 = int(value[2])*2
	d4 = int(value[3])*7
	d5 = int(value[4])*6
	d6 = int(value[5])*5
	d7 = int(value[6])*4
	d8 = int(value[7])*3
	d9 = int(value[8])*2
	total = d1+d2+d3+d4+d5+d6+d7+d8+d9
	dig_validador = 0
	residuo = total%11
	if(residuo!=0):
		dig_validador = 11-residuo
	return int(value[0:2])>=1 and int(value[0:2])<=24 and int(value[2])==9 and int(value[9])==dig_validador and int(value[10:13])>=1

#Tercer dígito 6
def ruc_publica(value):
	d1 = int(value[0])*3
	d2 = int(value[1])*2
	d3 = int(value[2])*7
	d4 = int(value[3])*6
	d5 = int(value[4])*5
	d6 = int(value[5])*4
	d7 = int(value[6])*3
	d8 = int(value[7])*2
	total = d1+d2+d3+d4+d5+d6+d7+d8
	dig_validador = 0
	residuo = total%11
	if(residuo!=0):
		dig_validador = 11-residuo
	return int(value[0:2])>=1 and int(value[0:2])<=24 and int(value[2])==6 and int(value[8])==dig_validador and int(value[9:13])>=1

def validate_ruc(value):
	if (not value.isdigit() or not len(value)==13 or not(ruc_natural(value) or ruc_juridica(value) or ruc_publica(value))):
		raise ValidationError(
            _('%(value)s no es un RUC válido'),
            code="invalid",
            params={'value': value},
        )

def validate_letras(value):
	if (not all(x.isalpha() or x.isspace() for x in value)):
		raise ValidationError(
            _('%(value)s no contiene únicamente letras'),
            code="invalid",
            params={'value': value},
        )

def validate_fono_convencional(value):
	if (not value.isdigit() or not(len(value)==7 or len(value)==9)):
		raise ValidationError(
			_('%(value)s no es un teléfono convencional correcto'),
            code="invalid",
            params={'value': value},
		)

def validate_celular(value):
	if (not value.isdigit() or not len(value)>=10):
		raise ValidationError(
			_('%(value)s no es un celular correcto'),
            code="invalid",
            params={'value': value},
		)		

def validate_fecha(fecha_inicio,fecha_fin):
	i = str(fecha_inicio)
	f = str(fecha_fin)
	valores_inicio = i.split("-")
	valores_fin = f.split("-")
	print(valores_fin)
	print(valores_inicio)
	if (valores_fin[0] < valores_inicio[0]):
		raise forms.ValidationError("La fecha de fin es menor que la fecha de inicio")
	elif (valores_fin[0] ==  valores_inicio[0] and valores_fin[1] < valores_inicio[1]):
		raise forms.ValidationError("La fecha de fin es menor que la fecha de inicio")
	elif (valores_fin[0] ==  valores_inicio[0] and valores_fin[1] == valores_inicio[1] and valores_fin[2] < valores_inicio[2]):
		raise forms.ValidationError("La fecha de fin es menor que la fecha de inicio")
	else:
		return fecha_fin

def validate_positive(value):
	print(value)
	if(value<0):
		raise ValidationError(
			_('%(values)s no es un numero positivo'),
			code="invalid",
            params={'value': value},
		)


def validate_horarios(hora_inicio,hora_fin):
	i= str(hora_inicio)
	f = str(hora_fin)
	valores_inicio = i.split(":")
	valores_fin = f.split(":")

	if(valores_fin[0]< valores_inicio[0]):
		raise forms.ValidationError("La hora de fin es menor que la hora de inicio")
	elif(valores_fin[0]== valores_inicio[0] and valores_fin[1] < valores_inicio[1]):
		raise forms.ValidationError("Los minutos de la hora de fin son menores que los de la hora de inicio")
	elif(valores_fin[0]== valores_inicio[0] and valores_fin[1] == valores_inicio[1]):
		raise forms.ValidationError("La hora de inicio no puede ser igual a la hora de fin")	
	else:
		return hora_fin

def validate_porcentaje(valor):
	if(valor<0):
		raise forms.ValidationError("El porcentaje no puede ser negativo")
	elif(valor>100):
		raise forms.ValidationError("El porcentaje no puede ser mayor a 100")
	else:
		return valor

def validate_anexo_corp(valor):
	val= valor.name.split(".")
	extension=val[1]
	types=["pdf","xlsx","jpg","jpeg","png"]
	if(extension in types):
		return valor
	else:
		raise forms.ValidationError("Este tipo de documento no es aceptado")
	
	
		
def validate_positivo(value):
	if(int(value)<0):
		raise ValidationError(
			_("Valor no puede ser negativo"),
			code="valor_negativo"
		)