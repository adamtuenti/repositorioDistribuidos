from django.db import models
from ventas.personas_juridicas.models import Juridica, Contacto_natural
from ventas.personas_naturales.models import Persona_Natural

import ventas.validaciones as val
import financiero.validaciones as val_fin

from financiero.orden_pago.models import Centro_Costos
import ventas.validaciones

from seguridad.models import Usuario

TIPO_EVENTO=[('Abierto','Abierto'),('Corporativo','Corporativo')]

# Create your models here.
ESTADO_CHOICES = [  
        ('ACTV','Grabado'),
        ('SLCE','Solicitud Enviada'),
	    ('ACPF', 'Autorizada por Financiero'),
        ('PNDP','Pendiente de Cobro'),
        ('CNCL','Cancelada'),
        ('ANLD','Anulada'),
	]

class OrdenFacturacion(models.Model):
    class Meta:
        ordering = ['cod_orden_fact']

    TIPO_CHOICES=[('Natural','Natural'),('Jurídica','Jurídica'),]
    

    tipo_cliente=models.CharField(max_length=15, choices=TIPO_CHOICES)
    cod_orden_fact=models.CharField(max_length=15, blank=True)
    n_tramite=models.CharField(max_length=15,blank=True, null=True, default='No asignado')
    fecha_tramite=models.DateField(blank=True, null=True)
    n_factura=models.CharField(max_length=15,blank=True, null=True, default='No asignado')
    fecha_factura=models.DateField(blank=True, null=True)
    fecha=models.DateField()
    ruc_ci=models.CharField(max_length=13)
    razon_nombres=models.CharField(max_length=200)
    contacto=models.CharField(max_length=200,blank=True, null=True)
    #contacto=models.CharField(max_length=200)
    #direccion=models.CharField(max_length=200)
    #telefono=models.CharField(max_length=15)
    #asesor=models.CharField(max_length=200,blank=True, null=True)
    asesor=models.ForeignKey(Usuario, blank = True, null = True, on_delete=models.CASCADE)
    
    centro_costos = models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, blank=False, null=True)
    n_participantes=models.PositiveIntegerField(blank=True, default=0, null=True)

    observaciones=models.CharField(max_length=500,blank=True, null=True)
    
    estado = models.CharField(max_length=5,default='ACTV',choices=ESTADO_CHOICES, blank=True, null=True)
    #participantes=models.ManyToManyField(Persona_Natural)
    subtotal=models.FloatField(blank=True, null=True ,default=0.0)
    descuento_fact=models.FloatField(blank=True, null=True,default=0.0)
    descuento_total=models.FloatField(blank=True, null=True,default=0.0)

    valor_total=models.FloatField(blank=True, null=True,default=0.0)
    valor_pendiente=models.FloatField(blank=True, null=True,default=0.0)
    motivo_anular = models.CharField(max_length=500, blank=True, null=True)

    def delete(self, *arg, **kwargs):
        
        super().delete(*arg,**kwargs)
    def __str__(self):
        return self.cod_orden_fact+" - "+self.razon_nombres

class OrdenFacturacionParticipante(models.Model):
    participante=models.ForeignKey(Persona_Natural,on_delete=models.SET_NULL, blank=False, null=True)
    nombre_evento=models.CharField(max_length=500)
    cod_evento=models.CharField(max_length=20)
    valor_evento=models.FloatField(default=0)
    descuento=models.IntegerField(default=0)
    valor=models.FloatField(default=0)
    orden=models.ForeignKey(OrdenFacturacion, on_delete=models.SET_NULL, blank=True, null=True)
    




class OrdenFacturacionFile(models.Model):
    file = models.FileField(upload_to='uploads/facturas/',blank=True, null=True)
    #file = models.CharField(max_length=50, blank=True,default=" ")
    #propuesta = models.ManyToManyField(PropuestaCorporativo, through='PropFileKey')
    orden=models.ForeignKey(OrdenFacturacion, on_delete=models.CASCADE)