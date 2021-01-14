from django.db import models
from django.db.models import Model 
from datetime import datetime
from multiselectfield import MultiSelectField
from financiero.orden_pago.models import Centro_Costos
from administrativo.productos.models import Producto

def upload_anexo(instance, filename):
    return "solicitudes_compra/%s/%s" %(instance.cod_solicitud, filename)

class SolicitudCompra(models.Model):
    ESTADO_CHOICES = [("Elaborado","Elaborado"), ("Aprobado","Aprobado"), ("Anulada","Anulada"),]
    PROCEDIMIENTO_SUGERIDO_CHOICES = [("Catálogo Electrónico","Catálogo Electrónico"), ("Subasta Inversa","Subasta Inversa"), ("Ínfima Cuantía","Ínfima Cuantía"),
    ("Menor Cuantía","Menor Cuantía"), ("Cotización","Cotización"), ("Licitación","Licitación"), ("Contratación Directa","Contratación Directa"),
     ("Contratación  integral por Precio Fijo","Contratación  integral por Precio Fijo"), ("Lista Corta","Lista Corta"), ("Concurso Público","Concurso Público"),]
    PERIODO_COMPRA_CHOICES = [("Diario","Diario"), ("Quincenal","Quincenal"), ("Mensual","Mensual"),
    ("Trimestral","Trimestral"), ("Cuatrimestral","Cuatrimestral"), ("Semestral","Semestral"),
    ("Anual","Anual"), ("No aplica","No aplica"),]
    TIPO_PROCESO_CHOICES = [("Bienes y Servicios Normalizados","Bienes y Servicios Normalizados"), ("Bienes y Servicios No Normalizados","Bienes y Servicios No Normalizados"),
    ("Obras","Obras"), ("Consultoría","Consultoría"),]
    TIPO_COMPRA_CHOICES = [("Bienes","Bienes"), ("Servicios","Servicios"),]
    SEDE_CHOICES = [("ESPOL, Guayaquil, Campus Las Peñas, Malecón 100 y Loja","ESPOL, Guayaquil, Campus Las Peñas, Malecón 100 y Loja"),
    ("ESPOL, Guayaquil, Campus Gustavo Galindo km 39.5 vía Perimetral","ESPOL, Guayaquil, Campus Gustavo Galindo km 39.5 vía Perimetral"),
    ("ESPOL, Quito, Av. 6 de Diciembre 3355","ESPOL, Quito, Av. 6 de Diciembre 3355")]

    # Datos principales (se muestran en vista "consultar")
    cod_solicitud = models.CharField(max_length=20, blank=True)
    fecha = models.DateField(default=datetime.now, blank=True)
    tipo_proceso = models.CharField(max_length=50, verbose_name="Periodo de Compra",blank=True, null=True, choices=TIPO_PROCESO_CHOICES)
    procedimiento_sugerido = models.CharField(max_length=50, verbose_name="Procedimiento Sugerido",blank=True, null=True, choices=PROCEDIMIENTO_SUGERIDO_CHOICES)
    tipo_compra = models.CharField(max_length=50, verbose_name="Tipo de Compra",blank=True, null=True, choices=TIPO_COMPRA_CHOICES)
    periodo_compra = models.CharField(max_length=50, verbose_name="Periodo de Compra",blank=True, null=True, choices=PERIODO_COMPRA_CHOICES)
    centro_costos = models.ForeignKey(Centro_Costos, on_delete=models.SET_NULL, blank=False, null=True)
    estado = models.CharField(max_length=50, verbose_name="Estado",blank=True, null=True, choices=ESTADO_CHOICES, default="Elaborado")
    fecha_aprobacion = models.DateField(blank=True, null=True)

    subtotal_0 = models.FloatField(default=0, verbose_name="Subtotal 0%")
    subtotal_iva = models.FloatField(default=0, verbose_name="Subtotal IVA")
    valor_iva = models.FloatField(default=0, verbose_name="IVA")
    total = models.FloatField(default=0, verbose_name="Total")

    # Informacion de ingreso (aparte de la principal)
    nombre_requirente = models.CharField(max_length=50, blank=True)
    fecha_requerimiento = models.DateField(default=datetime.now, blank=True)
    observaciones = models.CharField(max_length=500, verbose_name="Observaciones", blank=True, null=True)

    #Recepción del Bien/Servicio
    nombre_recibe = models.CharField(max_length=50, verbose_name="Nombre de quien recibe", blank=False)
    email_recibe = models.CharField(max_length=75, verbose_name="Email", blank=False)
    direccion_recibe = models.CharField(max_length=200, verbose_name="Dirección", blank=False, null=True)
    telefono_recibe = models.CharField(max_length=12, verbose_name="Teléfono", blank=True)
    celular_recibe = models.CharField(max_length=12, verbose_name="Celular", blank=True)

    #Datos Adicionales del custodio
    nombre_custodio = models.CharField(max_length=50, verbose_name="Nombre del custodio", blank=False)
    cargo_recibe = models.CharField(max_length=20, verbose_name="Cargo", blank=False)

    #Datos Adicionales del usuario responsable
    nombre_responsable = models.CharField(max_length=50, verbose_name="Nombre usuario responsable", blank=False)
    cargo_responsable = models.CharField(max_length=20, verbose_name="Cargo", blank=False)
    sede_responsable = models.CharField(max_length=150, verbose_name="Sede",blank=False, null=True, choices=SEDE_CHOICES, default="ESPOL, Guayaquil, Campus Gustavo Galindo km 39.5 vía Perimetral")

    anexo = models.FileField(upload_to=upload_anexo, blank=True, null=True)

    def __str__(self):
        return self.cod_solicitud

class ProductoSolicitud(models.Model):
    STATE_CHOICES = (
        (True, u'Si'),
        (False, u'No'),
    )

    solicitud_compra=models.ForeignKey(SolicitudCompra, on_delete=models.SET_NULL, null=True)
    producto=models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    otros=models.CharField(max_length=50, verbose_name="Otro", null=True)
    caracteristicas=models.CharField(max_length=200, verbose_name="Características", null=True)
    cantidad=models.FloatField(default=0)
    precio_referencial=models.FloatField(default=0)
    iva=models.BooleanField('Grava IVA', default= False, blank=True, null=True, choices=STATE_CHOICES)
    subtotal=models.FloatField(default=0)