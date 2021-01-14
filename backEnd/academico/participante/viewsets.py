from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import *
from .serializers import *


class ParticipanteViewSet(viewsets.ModelViewSet):
    queryset = Participante.objects.all()
    serializer_class = ParticipanteSerializer

    def list(self, request, *args, **kwargs):
        queryset = Participante.objects.all()
        evento_id = request.query_params.get('evento_id', None)
        if evento_id:
            queryset = Participante.objects.filter(evento_id=evento_id)
        serializer = ParticipanteSerializer(queryset, many=True)
        return Response(serializer.data)


class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

class NotificacionesViewSet(viewsets.ModelViewSet):
    queryset = Notificaciones.objects.all()
    serializer_class = NotificacionesSerializer

class SugerenciasViewSet(viewsets.ModelViewSet):
    queryset = Sugerencias.objects.all()
    serializer_class = SugerenciasSerializer

class DetalleParticipanteViewSet(viewsets.ModelViewSet):
    queryset = DetalleParticipante.objects.all()
    serializer_class = DetalleParticipanteSerializer
