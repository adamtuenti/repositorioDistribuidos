from django.db import models
import financiero.validaciones
from ventas.personas_naturales.models import Persona_Natural
from financiero.orden_facturacion.models import OrdenFacturacion
from academico.evento.models import Evento
# Create your models here.


class ProcesoEspecial(models.Model):
	ESTADO_CHOICES = [("EMIT","Emitido"),('SOLI','Solicitud Enviada'),("APRB","Aprobada"),("ANLD","Anulada"),]
	FORMAPAGO_CHOICES = [("TR","Transferencia"),("CH","Cheque"),]
	PROVEEDORES_CHOICES = [("Natural", "Natural"),("Jurídica", "Jurídica"),]
	COMPROBANTE_CHOICES = [("FC","Factura"),("NV","Nota de venta"),("LC","Liquidación de compra"),("CP","Comprobantes de pago"),]
	MOTIVO_CHOICES = [("DVVL","Devolución de Valores"),]
	TIPO_NOTA_CHOICES=[("Débito","Nota de Débito"),("Crédito","Nota de Crédito")]
	CATEGORIA=[("Dev","Devolución de valores"),("Part","Cambio de participantes"),("Event","Cambio de eventos"),("Grat","Cupo gratis")]

	cod_proceso = models.CharField(max_length=15, blank=True)
	motivo = models.CharField(max_length=500, blank=True, null=True)
	concepto = models.CharField(max_length=500)
	estado = models.CharField(max_length=5, default="EMIT",choices=ESTADO_CHOICES, blank=True, null=True)
	fecha_emision=models.DateField()
	fecha_aprobacion=models.DateField(blank=True, null=True)
	tipo_nota=models.CharField(max_length=10,default="Crédito",choices=TIPO_NOTA_CHOICES)
	categoria=models.CharField(max_length=10,choices=CATEGORIA)
	subtotal=models.FloatField(blank=True, null=True ,default=0.0)
	descuento_fact=models.FloatField(blank=True, null=True,default=0.0)
	descuento_total=models.FloatField(blank=True, null=True,default=0.0)
	valor_total=models.FloatField(blank=True, null=True,default=0.0)


	# documento = models.CharField(max_length=5, choices=COMPROBANTE_CHOICES, blank=True, null=True)
	# n_documento = models.CharField(max_length=20, blank=True, null=True)
	# evento = models.CharField(max_length=200, blank=True, null=True)
	# valor_evento = models.DecimalField(max_digits=10 ,decimal_places=2, blank=True, null=True, validators=[financiero.validaciones.validate_positivo])
	# descuento = models.DecimalField(max_digits=10 ,decimal_places=2, blank=True, null=True, validators=[financiero.validaciones.validate_positivo])
	# valor_pagar = models.DecimalField(max_digits=10 ,decimal_places=2, blank=True, null=True, validators=[financiero.validaciones.validate_positivo])
	# anexo = models.FileField(upload_to='uploads/nota_credito/', blank=True, null=True) 


class ProcesoParticipante(models.Model):
    participante=models.ForeignKey(Persona_Natural,on_delete=models.SET_NULL, blank=False, null=True)
    nombre_evento=models.CharField(max_length=500)
    cod_evento=models.CharField(max_length=20)
    valor_evento=models.FloatField(default=0)
    descuento=models.IntegerField(default=0)
    valor=models.FloatField(default=0)
    proceso=models.ForeignKey(ProcesoEspecial, on_delete=models.SET_NULL, blank=True, null=True)
    orden=models.ForeignKey(OrdenFacturacion, on_delete=models.SET_NULL, blank=True, null=True)


class ParticipanteIntermedio(models.Model):
    participante=models.ForeignKey(Persona_Natural,on_delete=models.SET_NULL, blank=False, null=True)
    nombre_evento=models.CharField(max_length=500)
    cod_evento=models.CharField(max_length=20)
    valor_evento=models.FloatField(default=0)
    descuento=models.IntegerField(default=0)
    valor=models.FloatField(default=0)
    orden=models.ForeignKey(OrdenFacturacion, on_delete=models.SET_NULL, blank=True, null=True)
    evento=models.ForeignKey(Evento, on_delete=models.CASCADE, blank=True, null=True)

class CambioEvento(models.Model):
	ESTADO_CHOICES = [  
		('SLCE','Solicitud Enviada'),
		('ACPF', 'Autorizada por Financiero'),
		('CNCL','Cancelada'),
		('ANLD','Anulada'),
	]
	participante=models.ForeignKey(Persona_Natural, on_delete=models.SET_NULL, blank=False, null=True)
	evento_origen=models.CharField(max_length=550)
	evento_destino=models.CharField(max_length=550)
	estado=models.CharField(max_length=30, default="SLCE", blank=True, null=True)

class ProcesoEspecialFile(models.Model):
    file = models.FileField(upload_to='uploads/proceso_especial/',blank=True, null=True)
    proceso_especial=models.ForeignKey(ProcesoEspecial, on_delete=models.CASCADE)
