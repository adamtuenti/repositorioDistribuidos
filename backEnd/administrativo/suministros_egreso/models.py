from django.db import models
from django.db.models import Model
from datetime import datetime
from multiselectfield import MultiSelectField
from administrativo.proveedores.models import Proveedor
from financiero.orden_pago.models import Centro_Costos
from administrativo.productos.models import Producto
from academico.evento.models import Evento

class Suministro_Egreso(models.Model):
    CONSUMO_CHOICES = [("Recursos del Evento", "Recursos del Evento"),("Consumo Interno", "Consumo Interno"),]
    AREA_CHOICES =[("Dirección","Dirección") , ("Académico","Académico") , ("Comercial","Comercial") , ("Logística","Logística") , ("Administrativo-Financiero","Administrativo-Financiero") , ("Control Académico","Control Académico") , ("Calidad","Calidad") , ("Marketing y Publicidad","Marketing y Publicidad") , ("TIC's","TIC's"),]
    
    cod_suministro_egreso=models.CharField(max_length=20, blank=True)
    fecha=models.DateField(default=datetime.now, blank=True)
    fecha_egreso=models.DateField(default=datetime.now, blank=True)
    tipo_consumo = models.CharField(max_length=50, choices=CONSUMO_CHOICES, blank=False)
    usuario=models.CharField(max_length=30)
    area = models.CharField(max_length=50, choices=AREA_CHOICES, blank=False)
    evento=models.ForeignKey(Evento,on_delete=models.SET_NULL,null=True, blank=True)
    cantidad_participantes=models.IntegerField(default=0, null=True, blank=True)
    observaciones=models.CharField(max_length=500, verbose_name="Observaciones", blank=True, null=True)



class Suministro_EgresoFile(models.Model):
    file = models.FileField(upload_to='uploads/',blank=True, null=True)
    suministro_egreso=models.ForeignKey(Suministro_Egreso, on_delete=models.CASCADE)

class ProductoSuministroEgreso(models.Model):
    suministro=models.ForeignKey(Suministro_Egreso, on_delete=models.SET_NULL, null=True)
    producto=models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad_solicitada=models.PositiveIntegerField(default=0)
    cantidad_despachada=models.PositiveIntegerField(default=0)