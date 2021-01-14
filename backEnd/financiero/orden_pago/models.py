from django.db import models
from administrativo.proveedores.models import Proveedor
from academico.evento.models import Evento
from multiselectfield import MultiSelectField

# Create your models here.

class Centro_Costos(models.Model):
	nombre = models.CharField(max_length=10)
	espol=models.DecimalField(max_digits=10, decimal_places=2)
	espoltech=models.DecimalField(max_digits=10, decimal_places=2)
	ministerio=models.DecimalField(max_digits=10, decimal_places=2)
	fundaespol=models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.nombre

class Egresos(models.Model):
	codigo = models.CharField(max_length=15)
	nombre = models.CharField(max_length=200)
	centroc = models.ForeignKey(Centro_Costos, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre

ESTADO_CHOICES = [("Grabado","Grabado"),("Enviado","Enviado"),("Autorizado","Autorizado"),("Anulado","Anulado"),("Pagado","Pagado")]

class OrdenPago(models.Model):
	FORMAPAGO_CHOICES = [("Transferencia","Transferencia"),("Cheque","Cheque"),]
	PROVEEDORES_CHOICES = [("Natural", "Natural"),("Jurídica", "Jurídica"),]
	DOC_CHOICES = [("Factura Original","Factura Original"),
					("Certificado comprobantes del SRI","Certificado comprobantes del SRI"),
					("Contrato","Contrato"),
					("Orden de compra","Orden de compra"),
					("Reporte de movilización","Reporte de movilización"),
					("Informe de actividades","Informe de actividades"),
					("Ingreso de bodega","Ingreso de bodega"),
					("Registro de Asistencia","Registro de Asistencia"),
					("Acta entrega-recepción B/S","Acta entrega-recepción B/S"),
					("Garantía técnica","Garantía técnica"),
					("Tiquetes aéreos","Tiquetes aéreos"),
					("Otros","Otros"),
					]

	cod_ord_pago = models.CharField(max_length=15, blank=True)
	n_tramite = models.CharField(max_length=20, blank=True)
	fecha = models.DateField()
	fecha_tramite = models.DateField(null=True,blank=True)
	fecha_envio = models.DateField(null=True,blank=True)
	fecha_aprobacion = models.DateField(null=True,blank=True)
	fecha_pago = models.DateField(null=True,blank=True)
	fecha_anulado = models.DateField(null=True,blank=True)
	fecha_comprobante = models.DateField()
	estado = models.CharField(max_length=30, default="Grabado",choices=ESTADO_CHOICES, blank=True)
	tipo_proveedor = models.CharField(max_length=10, choices=PROVEEDORES_CHOICES, blank=False)
	proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL,null=True)
	evento=models.ForeignKey(Evento,on_delete=models.SET_NULL,null=True)
	centro_costos = models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, blank=False, null=True)
	egreso = models.ForeignKey(Egresos, on_delete=models.SET_NULL, blank=False, null=True)
	tipo_documentos=MultiSelectField(choices=DOC_CHOICES)

	n_comprobante = models.CharField(max_length=20)
	concepto = models.CharField(max_length=500)
	forma_pago = models.CharField(max_length=30, choices=FORMAPAGO_CHOICES, blank=False)
	subtotal= models.DecimalField(max_digits=10,decimal_places=2)
	iva=models.BooleanField(default=False)
	valor_iva= models.DecimalField(max_digits=10,decimal_places=2)
	otros_cargos= models.DecimalField(max_digits=10,decimal_places=2)
	total= models.DecimalField(max_digits=10,decimal_places=2)
	motivo_anular = models.CharField(max_length=500, blank=True)
	
	def __str__(self):
		return self.cod_ord_pago


class OrdenPagoFile(models.Model):
    file = models.FileField(upload_to='uploads/orden_pago/')
    orden_pago=models.ForeignKey(OrdenPago, on_delete=models.CASCADE)
    
    # def delete(self, *arg, **kwargs):
    #     self.file.delete()
    #     super().delete(*arg,**kwargs)
