from rest_framework import serializers
from .models import *

from academico.diseño_evento.models import Unidad
from academico.diseño_evento.models import SubUnidad
from academico.diseño_evento.models import DisenoPadreHijo
from academico.diseño_evento.models import DesignEvento as DisenoEvento
from academico.evento.models import CalendarioEvento as Sesion
from academico.evento.models import Evento

"""
    Custom APIS.
    If used for testing, the models used must have all fields with 
    null=True.
    If that is not the case. They will be used only for GET requests to retrieve 
    the fields especified. These fields are required in Plan de Trabajo flow.
"""

#Only used for testing for creation of Sesion(Calendario_Evento)
class EventoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='codigo_evento')
    class Meta:
        model = Evento
        fields = ['id','nombre','diseno','tipo_evento']

#Only used for testing for creation of Unidad, SubUnidad
class DisenoEventoSerializer(serializers.ModelSerializer):
    disenos_hijos = serializers.ReadOnlyField(source='get_hijos')
    
    class Meta:
        model = DisenoEvento
        fields = ['id','nombre','objetivo','codigo','tipo_evento','es_padre','disenos_hijos']

class DisenoHijoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisenoEvento
        fields = ['id','nombre','objetivo','codigo','tipo_evento']

class DisenoPadreHijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisenoPadreHijo
        fields = ['id','padre','hijo']
        
class UnidadSerializer(serializers.ModelSerializer):
    diseno_evento = serializers.PrimaryKeyRelatedField(source='design',queryset=DisenoEvento.objects.all())
    nombre = serializers.CharField(source='nombre_unidad')
    class Meta:
        model = Unidad
        fields = ['id','diseno_evento','nombre', 'numero']

class SubUnidadSerializer(serializers.ModelSerializer):
    diseno_evento = serializers.PrimaryKeyRelatedField(source='design',queryset=DisenoEvento.objects.all())
    nombre = serializers.CharField(source='nombre_sub')
    numero = serializers.IntegerField(source='numero_sub')
    class Meta:
        model = SubUnidad
        fields = ['id','diseno_evento','nombre', 'numero']

class SesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sesion
        fields = ['id','evento','fecha','hora_inicio','hora_fin']

"""
 Models in Plan trabajo flow
"""

class PlanTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanTrabajo
        fields = '__all__'

class ArchivoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivoActividad
        fields = '__all__'

class  ActividadPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadPlan
        fields = '__all__'

class SesionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SesionItem
        fields = '__all__'

class RecursoSesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoSesion
        fields = '__all__'

class AnexoPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnexoPlan
        fields = '__all__'

class RecursoPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoPlan
        fields = '__all__'
    
class LecturaRecomendadaPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturaRecomendadaPlan
        fields = '__all__'

class ReferenciaBibliograficaPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenciaBibliograficaPlan
        fields = '__all__'