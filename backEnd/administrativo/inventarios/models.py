from django.db import models
from django.db.models import Model
from datetime import datetime
from financiero.orden_pago.models import Centro_Costos
from administrativo.ingreso_bienes.models import Bien

def upload_anexo(instance, filename):
    return "inventarios/%s/%s" %(instance.cod_inventario, filename)

class Inventario(models.Model):
    
    INVENTARIOS_CHOICES = [("Inicial", "Inicial"),("Final", "Final"),]
    TIPO_BIEN_CHOICES=[("Activo","Activo"), ("Bien Sujeto a control administrativo","Bien Sujeto a control administrativo"),]
    CATEGORIA_CHOICES=[("Categoria1","Categoria1"), ("Categoria2","Categoria2"),]

    #Datos generales
    cod_inventario=models.CharField(max_length=20, blank=True)
    fecha=models.DateField(default=datetime.now, blank=True)
    fecha_ultima_actualizacion=models.DateField(default=datetime.now, blank=True)
    tipo_inventario=models.CharField(max_length=10, choices=INVENTARIOS_CHOICES, blank=False)
    tipo_bienes=models.CharField(max_length=10, choices=TIPO_BIEN_CHOICES, blank=False)
    fecha_inicio=models.DateField(default=datetime.now, blank=True)
    fecha_fin=models.DateField(default=datetime.now, blank=True)
    categoria_bien=models.CharField(max_length=10, choices=CATEGORIA_CHOICES, blank=False)
    centro_costos=models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, blank=False, null=True)
    usuario_responsable=models.CharField(max_length=50, blank=True, null=True)

    #Datos Responsable CEC
    nombre_responsable_cec=models.CharField(max_length=40, blank=True, verbose_name="Nombre del responsable")
    cargo_responsable_entrega=models.CharField(max_length=40, blank=True)
    area_departamento_cec=models.CharField(max_length=30, blank=True, verbose_name="Área/Departamento")

    #Datos Responsable Unidad
    unidad_responsable=models.CharField(max_length=40, blank=True)
    nombre_responsable_unidad=models.CharField(max_length=40, blank=True)
    area_departamento_unidad=models.CharField(max_length=30, blank=True, verbose_name="Área/Departamento")
    cargo_responsable_unidad=models.CharField(max_length=40, blank=True, verbose_name="Cargo")
    mail_responsable_unidad=models.CharField(max_length=40, blank=True, verbose_name="Mail")
    telefono_responsable_unidad=models.CharField(max_length=40, blank=True, verbose_name="Teléfono")
    celular_responsable_unidad=models.CharField(max_length=40, blank=True, verbose_name="Celular")

    observaciones=models.CharField(max_length=500, verbose_name="Observaciones", blank=True, null=True)
    anexo = models.FileField(upload_to=upload_anexo, blank=True, null=True)
    
    def __str__(self):
        return self.cod_inventario    


class BienInventario(models.Model):

    SEDE_CHOICES = [("ESPOL, Guayaquil, Campus Las Peñas, Malecón 100 y Loja","ESPOL, Guayaquil, Campus Las Peñas, Malecón 100 y Loja"),
    ("ESPOL, Guayaquil, Campus Gustavo Galindo km 39.5 vía Perimetral","ESPOL, Guayaquil, Campus Gustavo Galindo km 39.5 vía Perimetral"),
    ("ESPOL, Quito, Av. 6 de Diciembre 3355","ESPOL, Quito, Av. 6 de Diciembre 3355")]
    CONSTATACIONES_CHOICES = [("Encontrado", "Encontrado"),("No encontrado", "No encontrado"),]
    ESTADO_CHOICES = [("En buen estado", "En buen estado"),("Dañado", "Dañado"),("Dado de baja", "Dado de baja"),
    ("Por reparar", "Por reparar")]

    inventario=models.ForeignKey(Inventario, on_delete=models.SET_NULL, null=True)
    bien=models.ForeignKey(Bien, on_delete=models.SET_NULL, null=True)
    fecha_inventario=models.DateField(default=datetime.now, blank=True)
    constatacion=models.CharField(max_length=20, choices=CONSTATACIONES_CHOICES, blank=False)
    observaciones=models.CharField(max_length=200, verbose_name="Observaciones", blank=True, null=True)
    usuario_responsable=models.CharField(max_length=50, blank=True, null=True)
    sede=models.CharField(max_length=200, verbose_name="Sede",blank=False, null=True, choices=SEDE_CHOICES, default="ESPOL, Guayaquil, Campus Gustavo Galindo km 39.5 vía Perimetral")
    estado=models.CharField(max_length=20, choices=ESTADO_CHOICES, blank=True, null=True)