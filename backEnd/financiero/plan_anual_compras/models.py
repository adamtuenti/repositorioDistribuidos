from django.db import models
import financiero.validaciones
from financiero.orden_pago.models import Centro_Costos, Egresos
from administrativo.productos.models import Producto
from datetime import date
# Create your models here.


ESTADO_CHOICES = [  
        ('Grabado','Grabado'),
        ('Solicitud Enviada','Solicitud Enviada'),
        ('Autorizada','Autorizada'),
        ('Anulada','Anulada'),
	]

class PlanAnualCompras(models.Model):
	nombre = models.CharField(max_length=100, blank=True)
	año = models.PositiveIntegerField(default= date.today().year)
	fecha = models.DateField()
	fecha_envio = models.DateField(blank=True, null=True)
	fecha_aprobado = models.DateField(blank=True, null=True)
	fecha_anulado = models.DateField(blank=True, null=True)
	centro_costos = models.ForeignKey(Centro_Costos,on_delete=models.SET_NULL,null=True)
	estado = models.CharField(max_length=100,default='Grabado',choices=ESTADO_CHOICES)
	motivo_anular = models.CharField(max_length=500, null=True,blank=True)

class Partida(models.Model):
	TIPO_COMPRAS_CHOICES = [("Bien","Bien"), ("Servicio","Servicio"),("Suministro","Suministro"),]
	UNIDAD_CHOICES = [("Unidad","Unidad"),("Caja","Caja"),("Paquete","Paquete"),("Litro","Litro"),("Galón","Galón"),("Caneca","Caneca"),("Resma","Resma"),("Otros","Otros"),('Ninguno','Ninguno')]

	pac = models.ForeignKey(PlanAnualCompras, on_delete=models.CASCADE, null=True, blank=True)
	egreso=models.ForeignKey(Egresos,on_delete=models.SET_NULL,null=True)
	tipo_compra = models.CharField(max_length=10, choices=TIPO_COMPRAS_CHOICES)
	unidad_medida=models.CharField(max_length=20, choices=UNIDAD_CHOICES, default='Ninguno')
	descripcion = models.CharField(max_length=500, blank=True)
	producto = models.ForeignKey(Producto, on_delete=models.SET_NULL,null=True,blank=True)
	cantidad_anual = models.PositiveIntegerField()
	subtotal = models.DecimalField(max_digits=10 ,decimal_places=2,validators=[financiero.validaciones.validate_positivo])
	total = models.DecimalField(max_digits=10 ,decimal_places=2, validators=[financiero.validaciones.validate_positivo])
	periodo=models.CharField(max_length=200)
	iva=models.BooleanField(default=False)
	costo_unitario=models.DecimalField(max_digits=10,decimal_places=2)


