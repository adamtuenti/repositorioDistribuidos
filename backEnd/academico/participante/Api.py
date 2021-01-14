from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Q
from academico.participante.models import *
from academico.participante.serializers import * 
from academico.evento.serializers import *
from academico.docente.serializers import DocenteSerializer
from academico.docente.models import Docente
from datetime import date


class login_participante(APIView):
	def post(self,request):
		try:
			correo = request.data.get('correo')
			clave = request.data.get('clave')
			participante=Participante.objects.get(correo=correo)
			if(participante.password==clave):
				return Response(data={'error':False,'id':participante.id})
			else:
				return Response(data={'error':True,'mensaje':"Credenciales incorrectas"})
		except Exception as e:
			return Response(data={'error':True,'mensaje':"Usuario no registrado"})

class existe_participante(APIView):
	def post(self,request):
		try:
			correo = request.data.get('correo')
			participante=Participante.objects.get(correo=correo)
			return Response(data={'error':False,'id':participante.id})

		except Exception as e:
			return Response(data={'error':True,'mensaje':"No se encuentra registrado"})


class notificaciones_participante(APIView):
    def post(self,request):
        id_participante = request.data.get('id')
       	queryset=None
       	serializacion=None
        try:
        	if Notificaciones.objects.filter(id_participante=id_participante,estado=True).exists():
        		queryset = Notificaciones.objects.filter(id_participante=id_participante,estado=True)
        		serializacion = NotificacionesSerializer(queryset,many=True)
        		return Response(data={"notificaciones":serializacion.data,"error":False},status=status.HTTP_200_OK)
        	else:
        		return Response(data={'error':True,'mensaje':"No tiene notificaciones"},status=status.HTTP_200_OK)
        except Exception as e:
        	return Response(data={'error':True,'mensaje':"Ocurrió un error"},status=status.HTTP_404_NOT_FOUND)

class actualizar_notificacion(APIView):
	def patch(self,request):
		try:
			id_notificacion= request.data.get('id_notificacion_participante')
			notificacion = Notificaciones.objects.get(id_notificacion_participante=id_notificacion)
			serializer = NotificacionesSerializer(notificacion,data=request.data,partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(data={"mensaje":"La notificación no se volverá a mostrar","error":False},status=status.HTTP_200_OK)
			else:
				return Response(data={'error':True,'mensaje':"No se pudo remover la notificación"},status=status.HTTP_200_OK)
		except Exception as e:
			return Response(data={'error':True,'mensaje':"Ocurrió un error"},status=status.HTTP_404_NOT_FOUND)

class cursos_participante(APIView):
	def post(self,request):
		try:
			cursos=[]
			data={}
			id_participante= request.data.get('id_participante')
			detalles = DetalleParticipante.objects.filter(id_participante=id_participante)
			serializerDetalle = DetalleParticipanteSerializer(detalles,many=True)
			for i in range(len(detalles)):	
				eventos = Evento.objects.filter(codigo_evento=serializerDetalle.data[i]['id_evento'])
				serializerEvento = EventoSerializer(eventos,many=True)
				pubEvento=PubEvento.objects.filter(evento=serializerDetalle.data[i]['id_evento'])
				serializerPub=PubEventoSerializer(pubEvento,many=True)
				data['nombre_curso']=serializerEvento.data[i]['nombre']
				data['fecha_inicio']=serializerEvento.data[i]['fecha_inicio']
				data['estado']=serializerEvento.data[i]['estado']
				data['codigo_evento']=serializerEvento.data[i]['codigo_evento']
				data['imagen']=serializerPub.data[i]['picture']
				cursos.append(data)

			return Response(data={"cursos":cursos,"error":False},status=status.HTTP_200_OK)
		except Exception as e:
			return Response(data={'error':True,'mensaje':"Ocurrió un error"},status=status.HTTP_404_NOT_FOUND)

	
class detalles_curso(APIView):
	def post(self,request):
		try:
			data={}
			codigo_evento= request.data.get('codigo_evento')
			id_participante= request.data.get('id_participante')
			detalle = DetalleParticipante.objects.get(id_participante=id_participante,id_evento=codigo_evento)
			serializerDetalle = DetalleParticipanteSerializer(detalle)
			evento = Evento.objects.get(codigo_evento=serializerDetalle.data['id_evento'])
			serializerEvento = EventoSerializer(evento)
			pubEvento=PubEvento.objects.get(evento=serializerDetalle.data['id_evento'])
			serializerPub=PubEventoSerializer(pubEvento)
			docente=Docente.objects.get(id=serializerEvento.data['docente'])
			serializerDocente=DocenteSerializer(docente)
			data['docente']=serializerDocente.data['nombres']+" "+serializerDocente.data['apellidos']
			data['nombre_curso']=serializerEvento.data['nombre']
			data['fecha_inicio']=serializerEvento.data['fecha_inicio']
			data['fecha_fin']=serializerEvento.data['fecha_fin']
			data['estado']=serializerEvento.data['estado']
			data['codigo_evento']=serializerEvento.data['codigo_evento']
			data['imagen']=serializerPub.data['picture']

			return Response(data={"detalles":data,"error":False},status=status.HTTP_200_OK)
		except Exception as e:
			return Response(data={'error':True,'mensaje':"Ocurrió un error"},status=status.HTTP_404_NOT_FOUND)


