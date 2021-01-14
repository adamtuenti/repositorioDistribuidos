from django.db import models
from django import forms
from django.contrib.postgres.fields import JSONField

from academico.evento.models import Evento


# Create your models here.
class Participante(models.Model):
    
    GENERO_CHOICES = [('M','Masculino'),('F','Femenino'),]

    """
        null fields are allowed for speed of development
        TODO:
            - add field 'foto'
        evento = models.ForeignKey(Evento, on_delete=models.CASCADE,related_name='participante_eventos')
    """
    
    nombres = models.CharField(null=True,blank=True,max_length=50)
    apellidos = models.CharField(null=True,blank=True,max_length=50)
    identificacion = models.CharField(null=True,blank=True,unique=True,max_length=15)
    password = models.CharField(blank=True,null=False,max_length=15)
    correo = models.EmailField(blank=True,null=True)
    correo_alternativo = models.EmailField(blank=True,null=True)
    telefono = models.CharField(null=True,blank=True,max_length=12)
    direccion = models.CharField(null=True,blank=True,max_length=50)
    genero = models.CharField(choices=GENERO_CHOICES,null=False,blank=False, max_length=50)

    def __str__(self):
        return '{} {}'.format(self.nombres, self.apellidos)

    def get_detalle(self):
        eventos = detalle_participante.objects.filter(id_participante=self.id).select_related('id_evento')
        return eventos

class Notificaciones(models.Model):
    id_notificacion_participante = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50,null=False,blank=False)
    descripcion = models.TextField()
    fecha = models.DateField()
    imagen=models.ImageField(upload_to='notificacion',null=True,blank=True)
    id_participante = models.ForeignKey(Participante,on_delete=models.CASCADE,related_name='id_participante')
    estado=models.BooleanField(default=True)

    def __str__(self):
        return '{} / {}'.format(self.titulo, self.fecha)

class Sugerencias(models.Model):
    id_sugerencia_participante = models.AutoField(primary_key=True)
    asunto = models.CharField(null=True,blank=True,max_length=50)
    mensaje = models.TextField(null=False,blank=False)
    id_participante = models.ForeignKey(Participante,on_delete=models.CASCADE,related_name='%(class)s_id_participante')
    imagen=models.ImageField(upload_to='evidencia',null=True,blank=True)

    def __str__(self):
        return '{} / {}'.format(self.asunto, self.id_participante)


class DetalleParticipante(models.Model):
    ESTADO_CHOICES = [('A','Activo'),('I','Inactivo'),]
    id_detalle_participante = models.AutoField(primary_key=True)
    id_evento = models.ForeignKey(Evento,on_delete=models.CASCADE,related_name='eventosParticipante')
    id_participante = models.ForeignKey(Participante,on_delete=models.CASCADE,related_name='detalleParticipante')
    calificaciones = JSONField(null=True)
    nota_final1 = models.FloatField(blank=True)
    nota_mej = models.FloatField(blank=True)
    aprobado = models.CharField(max_length = 2, default="No")
    rectificado = models.CharField(max_length = 2, default="No")
    fecha_registro_mej = models.DateField(null=True, blank=True)
    fecha_rectificado = models.DateField(null=True, blank=True)

class Asistencia(models.Model):
    """
        In registro field I will save a value like :
        [
            { participante_id : 'PARTICIPANTE_ID1' , is_presente : true },
            { participante_id : 'PARTICIPANTE_ID2' , is_presente : false },
            ...
        ]
    """
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha = models.DateField(null=True)
    registro = JSONField(null=True)

class ConvalidacionEvento(models.Model):
    evento_origen = models.ForeignKey(Evento, on_delete=models.CASCADE,related_name="origen_evento")
    evento_destino = models.ForeignKey(Evento,null=True,blank=True,on_delete=models.CASCADE,related_name="destino_evento")
    tipo_convalidacion = models.CharField(null=False,blank=False,max_length=50)
    motivo_convalidacion = models.CharField(null=False,blank=False,max_length=50)
    intitucion = models.CharField(null=True,blank=True,max_length=65)
    fecha_convalidacion = models.DateField(null=True,blank=True)
    participante_convalidado = models.ForeignKey('Participante',on_delete=models.CASCADE,related_name='eventosParticipante')
    certificado = models.FileField(upload_to='image_event/',null=True,blank=True)