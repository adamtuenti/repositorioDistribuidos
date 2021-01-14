from django.db import models
from ventas.reporte_contacto.models import ReporteContacto
from ventas.personas_juridicas.models import Juridica, Sector, TipoEmpresa
from multiselectfield import MultiSelectField
import ventas.validaciones
import os
from django.core.files import File
from educacion_continua import settings

# Create your models here.



class PropuestaCorporativo(models.Model):

    ESTADO_CHOICES= [
                        ('SG','Seguimiento'),
                        ('PD','Pendiente'),
                        ('ACP','Aceptada'),
                        ('NACP','No aceptada'),
                    ]

    SERVICIOS_CHOICES=  [
                            ('CBR','Coffe Break'),
                            ('ALM','Almuerzo'),
                            ('MIP','Material impreso'),
                            ('MDG','Material digital'),
                        ]

    cod_propuesta=models.CharField(max_length=20, blank=True)
    version=models.PositiveIntegerField()
    tipo_empresa=models.ForeignKey(TipoEmpresa, on_delete=models.SET_NULL, null=True, blank=True)
    reporte=models.ForeignKey(ReporteContacto, on_delete=models.CASCADE, blank=True)
    estado=models.CharField(max_length=15,
                            choices=ESTADO_CHOICES,
                            default='SG')
    ruc_ci=models.CharField(max_length=13)
    razon_nombres=models.CharField(max_length=200)
    sector=models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_solicitud=models.DateField()
    numero_participantes=models.PositiveIntegerField()
    total_horas=models.PositiveIntegerField()
    cantidad_cursos=models.PositiveIntegerField()
    monto_propuesta=models.FloatField()
    margen_contribucion=models.FloatField( max_length=3)
    utilidad_esperada=models.FloatField()
    exito=models.FloatField( max_length=4)
    lugar=models.CharField(max_length=25)
    servicios_incluidos=MultiSelectField(choices=SERVICIOS_CHOICES,
                                            blank=True,
                                            null=True)
    fecha_inicio_estimada=models.DateField()
    fecha_envio=models.DateField()
    fecha_respuesta=models.DateField()
    observacion=models.CharField(max_length=250,blank=True,null=True)

    area_capacitacion= models.CharField(max_length=50, blank=True)
    asesor=models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True, on_delete=models.SET_NULL)

    active=models.BooleanField(default = True)
    def delete(self, *arg, **kwargs):
     #   self.anexo.delete()
        super().delete(*arg,**kwargs)

class PropuestaFile(models.Model):
    file = models.FileField(upload_to='uploads/',blank=True, null=True)
    #file = models.CharField(max_length=50, blank=True,default=" ")
    #propuesta = models.ManyToManyField(PropuestaCorporativo, through='PropFileKey')
    propuesta=models.ForeignKey(PropuestaCorporativo, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     #Generate a new license file overwriting any previous version
    #     #and update file path
    #     # Using File
    #     f = open(self.file,'r')
    #     self.file.save(self.file.file, File(f))
    #     #super(PropuestaFile, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
    #     super(PropuestaFile,self).delete(*args,**kwargs)

