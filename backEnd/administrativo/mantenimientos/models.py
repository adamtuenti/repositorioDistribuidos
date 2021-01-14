from django.db import models
from django.db.models import Model
from datetime import datetime
from administrativo.ingreso_bienes.models import Bien, Ingreso_Bien
from financiero.orden_pago.models import Egresos

def upload_anexo(instance, filename):
    return "mantenimientos/%s/%s" %(instance.cod_mantenimiento, filename)

class Mantenimiento(models.Model):
    
    TIPO_BIEN_CHOICES=[("Activo","Activo"), ("Bien Sujeto a control administrativo","Bien Sujeto a control administrativo"),]
    STATE_CHOICES = (
        (True, u'Si'),
        (False, u'No'),
    )

    cod_mantenimiento=models.CharField(max_length=20, blank=True)
    fecha=models.DateField(default=datetime.now, blank=True)
    detalle_mantenimiento=models.CharField(max_length=500, verbose_name="Detalle mantenimiento", blank=False, null=False,default="")
    tipo_bien = models.CharField(max_length=50, choices=TIPO_BIEN_CHOICES, blank=False)
    bien = models.ForeignKey(Bien, on_delete=models.SET_NULL,null=True)
    ingreso_bien = models.ForeignKey(Ingreso_Bien, on_delete=models.SET_NULL,null=True)
    cod_orden_pago = models.CharField(max_length=20, blank=True)
    egresos = models.ForeignKey(Egresos, on_delete=models.SET_NULL,null=True, verbose_name="Partida Presupuestaria")

    es_planificado = models.BooleanField('Planificado', default= False, blank=True, null=True, choices=STATE_CHOICES)
    iva=models.BooleanField('Grava IVA', default= False, blank=True, null=True, choices=STATE_CHOICES)

    observaciones=models.CharField(max_length=500, verbose_name="Observaciones", blank=True, null=True)
    subtotal=models.FloatField(default=0)
    valor_iva=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    anexo = models.FileField(upload_to=upload_anexo, blank=True, null=True)

    def __str__(self):
        return self.cod_mantenimiento