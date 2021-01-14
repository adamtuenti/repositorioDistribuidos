from django.db import models
from financiero.orden_facturacion.models import OrdenFacturacion
import financiero.validaciones as val_fin
from financiero.orden_facturacion.models import Centro_Costos
# Create your models here.
class OrdenIngreso(models.Model):
	class Meta:
		ordering = ['-cod_orden_ing']

	FORMAS_PAGO=[
		("Cheque","Cheque"),
		("Transferencia","Transferencia"),
		("Depósito","Depósito"),
		("Tarjeta de Crédito","Tarjeta de Crédito"),
	]
	TARJETAS=[
		("Visa","Visa"),
		("Mastercard","Mastercard"),
		("American Express","American Express"),
		("Diners","Diners"),
		("Discover","Discover"),
	]
	TIPO_CHOICES=[('Natural','Natural'),('Jurídica','Jurídica'),]
	ESTADO_CHOICES = [  
        ('ACTV','Activa'),
        ('ANLD','Anulada'),
	]

	
	cod_orden_ing=models.CharField(max_length=15, blank=True)
	tipo_cliente=models.CharField(max_length=15, choices=TIPO_CHOICES)
	fecha=models.DateField(blank=True, null=True)
	n_tramite=models.CharField(max_length=15,blank=True, null=True, default='No asignado')

	fecha_tramite=models.DateField(blank=True, null=True,verbose_name="Fecha trámite")
	fecha_anulacion=models.DateField(blank=True, null=True, verbose_name="")
	estado = models.CharField(max_length=5,default='ACTV',choices=ESTADO_CHOICES, blank=True, null=True,verbose_name="Estado Orden Ingreso")
	saldo_facturacion=models.DecimalField(max_digits=10,decimal_places=2,validators=[val_fin.validate_positivo], blank=True, null=True,default=0)
	centro_costos = models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, blank=False, null=True)


	n_factura=models.CharField(max_length=15,blank=True, null=True, default='No asignado')
	ruc_ci=models.CharField(max_length=13)

	orden_facturacion = models.ForeignKey(OrdenFacturacion, on_delete=models.SET_NULL, blank=False, null=True)
	
	razon_nombres=models.CharField(max_length=50)
	descripcion=models.CharField(max_length=150)
	formaPago=models.CharField(max_length=30, choices=FORMAS_PAGO,default='cheque')
	# valor=models.DecimalField(max_digits=15,decimal_places=2,validators=[val_fin.validate_positivo])
	valor=models.FloatField(blank=True, null=True,default=0.0,validators=[val_fin.validate_positivo])
	
	fechaPago=models.CharField(max_length=12)
	numeroDocumento=models.PositiveIntegerField()
	banco=models.CharField(max_length=30)
	emisoraTarjeta=models.CharField(max_length=20,choices=TARJETAS, blank=True)
	# def formfield_for_foreignKey(self,db_field,request, **kwargs):
	# 	if db_field.name == "orden_facturacion":
	# 		kwargs["queryset"]= OrdenFacturacion.objects.filter(estado="PNDP")
	# 	return super(OrdenIngreso,self).formfield_for_foreignkey(self,db_field,request, **kwargs)


	def delete(self, *arg, **kwargs):
		
		super().delete(*arg,**kwargs)

class OrdenIngresoFile(models.Model):
    file = models.FileField(upload_to='uploads/OrdenIngreso/',blank=True, null=True)
    #file = models.CharField(max_length=50, blank=True,default=" ")
    #propuesta = models.ManyToManyField(PropuestaCorporativo, through='PropFileKey')
    orden=models.ForeignKey(OrdenIngreso, on_delete=models.CASCADE)
