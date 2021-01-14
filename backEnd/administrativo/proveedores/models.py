from django.db import models
import administrativo.validaciones
from django.db.models import Model 
from datetime import datetime
from multiselectfield import MultiSelectField

class Provincia(models.Model):
	nombre = models.CharField(max_length=50,verbose_name="Provincia")
	def __str__(self):
		return self.nombre


class Ciudad(models.Model):
	provincia=models.ForeignKey(Provincia, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50,verbose_name="Ciudad")
	def __str__(self):
		return self.nombre

class TipoEmpresa(models.Model):
	nombre = models.CharField(max_length=100,verbose_name="Tipo de Empresa")
	def __str__(self):
		return self.nombre


class TipoRubro(models.Model):
	nombre = models.CharField(max_length=100,verbose_name="Tipo de Rubro")
	def __str__(self):
		return self.nombre

class TipoProveedor(models.Model):
	nombre = models.CharField(max_length=100,verbose_name="Tipo de Proveedor")
	def __str__(self):
		return self.nombre

class Sector(models.Model):
	nombre = models.CharField(max_length=100,verbose_name="Sector")
	def __str__(self):
		return self.nombre

class Proveedor(models.Model):
	# TIPO_RUBRO_CHOICES = [("Devolución de valores","Devolución de valores"), ("Alimentación","Alimentación"), ("Honorarios profesionales de docencia","Honorarios profesionales de docencia"),("Honorarios profesionales","Honorarios profesionales"),
	# ("Hospedaje con o sin alimentación","Hospedaje con o sin alimentación"),("Movilización interna","Movilicación interna"),("Movilización externa","Movilización externa"),("Servicios aéreos","Servicios aéreos"),("Viáticos al interios","Viáticos al interior"),("Viáticos al exterior","Viáticos al exterior"),
	# ("Suministros de oficina","Suministros de oficina"),("Otros suministros","Otros suministros"),("Materiales de ferreteria","Materiales de ferreteria"),("Materiales de limpieza","Materiales de limpieza"),("Mantenimientos de instalaciones","Mantenimientos de instalaciones"),("Equipos tecnológicos","Equipos tecnológicos"),
	# ("Equipos de oficina","Equipos de oficina"),("Materiales","Materiales"),("Publicidad impresa","Publicidad impresa"),("Publicidad en medios digitales","Publicidad en medios digitales"),("Internet","Internet"),("Servicios de agua potable","Servicios de agua potable"),("Servicio de energía eléctrica y alumbrado público","Servicio de energía eléctrica y alumbrado público"),
	# ("Servicio de telefonia fija y/o móvil","Servicio de telefonia fija y/o móvil"),("Servicio de vigilancia","Servicio de vigilancia"),("Materiales didácticos","Materiales didácticos"),("Otros gastos","Otros gastos")]
	
	# TIPO_PROVEEDOR_CHOICES = [("Natural","Natural"), ("Jurídica","Jurídica")]

	cod_proveedor=models.CharField(max_length=20, blank=True)
	fecha=models.DateField(default=datetime.now, blank=True)
	ruc = models.CharField(max_length=13)
	razon = models.CharField(max_length=200)
	sector = models.ForeignKey(Sector,on_delete=models.SET_NULL, null=True)
	direccion = models.CharField(max_length=200)
	provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
	ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)

	telefono = models.CharField(max_length=20, validators=[administrativo.validaciones.validate_fono_convencional])
	celular = models.CharField(max_length=20, validators=[administrativo.validaciones.validate_celular])
	correo = models.CharField(max_length=100)
	representante = models.CharField(max_length=250, blank=True, null=True)
	# tipo_proveedor = models.CharField(max_length=50, verbose_name="Tipo de Proveedor", choices=TIPO_PROVEEDOR_CHOICES)
	
	
	tipo_proveedor = models.ForeignKey(TipoProveedor,on_delete=models.SET_NULL, null=True)
	
	tipo_rubro = models.ForeignKey(TipoRubro,on_delete=models.SET_NULL, null=True)

	observaciones = models.CharField(max_length=500, verbose_name="Observaciones", blank=True, null=True)
	
	ci_contacto_uno=models.CharField(max_length=13,  blank=True, null=True, validators=[administrativo.validaciones.validate_cedula])
	nombre_contacto_uno=models.CharField(max_length=200,  blank=True, null=True)
	apellidos_contacto_uno=models.CharField(max_length=200 , blank=True, null=True)
	cargo_contacto_uno=models.CharField(max_length=200,  blank=True, null=True)
	telefono_contacto_uno=models.CharField(max_length=20,  blank=True, null=True, validators=[administrativo.validaciones.validate_fono_convencional])
	celular_contacto_uno=models.CharField(max_length=20,  blank=True, null=True, validators=[administrativo.validaciones.validate_celular])
	correo_contacto_uno= models.CharField(max_length=100,  blank=True, null=True)

	ci_contacto_dos=models.CharField(max_length=13,  blank=True, null=True, validators=[administrativo.validaciones.validate_cedula])
	nombre_contacto_dos=models.CharField(max_length=200,  blank=True, null=True)
	apellidos_contacto_dos=models.CharField(max_length=200,  blank=True, null=True)
	cargo_contacto_dos=models.CharField(max_length=200,  blank=True, null=True)
	telefono_contacto_dos=models.CharField(max_length=20, blank=True, null=True,  validators=[administrativo.validaciones.validate_fono_convencional])
	celular_contacto_dos=models.CharField(max_length=20,  blank=True, null=True, validators=[administrativo.validaciones.validate_celular])
	correo_contacto_dos= models.CharField(max_length=100,  blank=True, null=True)

	ci_contacto_tres=models.CharField(max_length=13,  blank=True, null=True, validators=[administrativo.validaciones.validate_cedula])
	nombre_contacto_tres=models.CharField(max_length=200,  blank=True, null=True)
	apellidos_contacto_tres=models.CharField(max_length=200,  blank=True, null=True)
	cargo_contacto_tres=models.CharField(max_length=200,  blank=True, null=True)
	telefono_contacto_tres=models.CharField(max_length=20,  blank=True, null=True, validators=[administrativo.validaciones.validate_fono_convencional])
	celular_contacto_tres=models.CharField(max_length=20,  blank=True, null=True, validators=[administrativo.validaciones.validate_celular])
	correo_contacto_tres= models.CharField(max_length=100,  blank=True, null=True)

	def __str__(self):
		return self.razon