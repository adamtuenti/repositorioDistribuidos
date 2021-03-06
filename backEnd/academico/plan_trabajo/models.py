from django.db import models
from django.core.validators import MinLengthValidator
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField

from academico.diseño_evento.models import Unidad
from academico.diseño_evento.models import SubUnidad
from academico.diseño_evento.models import DesignEvento as DisenoEvento
from academico.evento.models import CalendarioEvento as Sesion
from academico.evento.models import Evento

MIN_LENGTH_TEXTFIELD = 10

"""
This class is just to mimic the depedency of plantrabajo with a diseño de evento

"""
#class DisenoEvento(models.Model):
#    descripcion =  models.TextField()

"""
Clases to mimic logic from diseno evento
    TODO: match with design of Alex
"""
#class Unidad(models.Model):
#    diseno_evento = models.ForeignKey(DisenoEvento,on_delete=models.CASCADE)
#    nombre = models.TextField()
#    numero = models.IntegerField()

#class SubUnidad(models.Model):
#    diseno_evento = models.ForeignKey(DisenoEvento,on_delete=models.CASCADE)
#    nombre = models.TextField()
#    numero = models.IntegerField()

#class Sesion(models.Model):
#    diseno_evento = models.ForeignKey(DisenoEvento,on_delete=models.CASCADE)
#    numero = models.IntegerField()

"""
 Models in Plan trabajo flow
"""


class PlanTrabajo(models.Model):
    """
        estado = 'En progreso' | 'Pendiente de aprobación' | 'Por corregir'

        In instrumentos_de_evaluacion field I will save a value like :
        [
            { nombre : 'Prueba Diagnóstica'              , diagnostico : false                                        , porcentajeAsignado : 0    },
            { nombre : 'Exámenes'                                              , formativo : false , sumativo : false , porcentajeAsignado : 40   },
            ...
        ]
    """
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fecha_de_creacion = models.DateField(auto_now_add=True)
    fecha_de_modificacion = models.DateField(auto_now=True)
    fecha_de_aprobacion = models.DateField(null=True)
    estado = models.TextField(null=True)
    instrumentos_de_evaluacion = JSONField(null=True)
    motivo_de_rechazo = models.TextField(null=True)
    
    def __str__(self):
        return '{}'.format(self.id)

def upload_actividad(instance, filename):
    return "PlanTrabajo/%s/Actividades/%s/%s" %(instance.plan_trabajo, instance.nombre, filename)

class ActividadPlan(models.Model):
    plan_trabajo = models.ForeignKey(PlanTrabajo, on_delete=models.CASCADE)
    nombre = models.TextField()
    descripcion = models.TextField()
    """
        Validate if these fields are strictly neccesary. They were asked, but looking at the flow
        of plan trabajo they are not required to complete the flow succesfully.
        unidadId =
        subUnidadId =
        instrumentoId =
        tipo =

        TODO:
        adjunto =
    """
    tipo_evaluacion = models.TextField()
    instrumento = models.TextField()
    
class ArchivoActividad(models.Model):
    archivo = models.FileField(upload_to=upload_actividad, null=True)
    actividad_plan = models.ForeignKey(ActividadPlan, on_delete=models.CASCADE)

class SesionItem(models.Model):
    plan_trabajo = models.ForeignKey(PlanTrabajo, on_delete=models.CASCADE)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    sub_unidad = models.ForeignKey(SubUnidad, on_delete=models.CASCADE)
    actividad_plan = models.ForeignKey(ActividadPlan, on_delete=models.CASCADE)


class RecursoSesion(models.Model):
    """
        tipo = Didacticos | Otros
    """
    plan_trabajo = models.ForeignKey(PlanTrabajo, on_delete=models.CASCADE)
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    tipo = models.TextField()
    descripcion = models.TextField()

def upload_anexo(instance, filename):
    return "PlanTrabajo/%s/Anexos/%s/%s" %(instance.plan_trabajo, instance.nombre, filename)

class AnexoPlan(models.Model):
    plan_trabajo = models.ForeignKey(PlanTrabajo, on_delete=models.CASCADE)
    nombre = models.TextField()
    descripcion = models.TextField()
    """
        TODO: add archivo adjunto
    """
    archivo = models.FileField(upload_to=upload_anexo, null=True)
    nombre_archivo = models.TextField()

class RecursoPlan(models.Model):
    """
        tipo = Equipos | Materiales Didácticos | Software | Hardware | Aula/Laboratorio.
    """
    plan_trabajo = models.ForeignKey(PlanTrabajo, on_delete=models.CASCADE)
    tipo = models.TextField()
    descripcion = models.TextField()


class LecturaRecomendadaPlan(models.Model):
    """
        #tipo = Libro | Sitio/Documento Web
    """
    plan_trabajo = models.ForeignKey(PlanTrabajo, on_delete=models.CASCADE)
    tipo = models.TextField()
    titulo = models.TextField()
    autores = models.TextField()
    descripcion = models.TextField()

    # fields for tipo Libro
    ano_publicacion = models.IntegerField(null=True)
    editorial = models.TextField(null=True)
    pais = models.TextField(null=True)
    fecha_consulta = models.DateField(null=True)

    # fields for tipo Sitio/Documento Web
    nombre_sitio = models.TextField(null=True)
    link = models.TextField(null=True)


class ReferenciaBibliograficaPlan(models.Model):
    """
        #tipo = Libro | Sitio/Documento Web
    """
    plan_trabajo = models.ForeignKey(PlanTrabajo, on_delete=models.CASCADE)
    tipo = models.TextField()
    titulo = models.TextField()
    autores = models.TextField()
    descripcion = models.TextField()

    # fields for tipo Libro
    # None

    # fields for tipo Sitio/Documento Web
    nombre_sitio = models.TextField(null=True)
    link = models.TextField(null=True)
