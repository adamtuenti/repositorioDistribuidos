from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Q
from academico.participante.models import *
from academico.evento.serializers import * 
from datetime import date

class part_api(APIView):
    def post(self,request):
        ident = request.data.get('identificacion')
        #print(ident)
       	queryset=None
       	serializacion=None
        try:
        	if Participante.objects.filter(identificacion=ident).exists():
        		queryset = Participante.objects.get(identificacion=ident)
        		serializacion = ParticipanteSerializers(queryset)
        		return Response(data=serializacion.data,status=status.HTTP_200_OK)
        	else:
        		return Response(data={"error":"participante no encontrado"},status=status.HTTP_200_OK)
        except Exception as e:
        	print(e)
        	return Response(data={"error":"participante no encontrado"},status=status.HTTP_404_NOT_FOUND)

class GuardarConvalidacion(APIView):
    def post(self,request):
        tipo_convalidacion = request.data.get('conv_seleccion')
        conv_saved_h = None
        conv_saved_i = None
        try: 
        	if tipo_convalidacion == 'Convalidación interna':
        		conv_saved_i = ConvalidacionEvento.objects.create(evento_origen=Evento.objects.get(codigo_evento=request.data.get('codigo'))
        														,evento_destino=Evento.objects.get(codigo_evento=request.data.get('codigo_convalidar'))
        														,tipo_convalidacion=tipo_convalidacion
        														,motivo_convalidacion= request.data.get('motivo')
        														,fecha_convalidacion=date.today()
        														,participante_convalidado=Participante.objects.get(identificacion=request.data.get('identificacion'))
        														)
        		if conv_saved_i:
        		   print(conv_saved_i)
        		   return Response(data={"mensaje_success":"Convalidacion interna realizada con exito "},status=status.HTTP_200_OK)

        	if tipo_convalidacion == 'Convalidación historica':
        		conv_saved_h = ConvalidacionEvento.objects.create(evento_origen=Evento.objects.get(codigo_evento=request.data.get('codigo_evento_historico'))
        														,tipo_convalidacion=tipo_convalidacion
        														,motivo_convalidacion= request.data.get('motivo')
        														,fecha_convalidacion=date.today()
        														,intitucion=request.data.get('institucion_historico')
        														,participante_convalidado=Participante.objects.get(identificacion=request.data.get('identificacion'))
        														,certificado=request.data.get('archivo_historico'))
        		if conv_saved_h:
        		   print(conv_saved_h)
        		   return Response(data={"mensaje_success":"Convalidacion historica realizada con exito"},status=status.HTTP_200_OK)


        		return Response(data={"error":"Convalidación interna"},status=status.HTTP_200_OK)
        	else:
        		return Response(data={"error":"Convalidación historica"},status=status.HTTP_200_OK)
        except Exception as e:
        	print(e)
        	return Response(data={"error":"error del sistema"},status=status.HTTP_404_NOT_FOUND)
      

class part_eventos(APIView):

	def get(self,request):
		detalle = DetalleParticipante.objects.all().select_related('id_evento','id_participante')
		serial = ParticipanteDetalleSerializers(detalle,many=True)
		return Response(data=serial.data,status=status.HTTP_200_OK)

	def post(self,request):
		identificacion = request.data.get('identificacion')
		cod_evento = request.data.get('codigo')
		queryset = None
		detalle = None
		serializacion = None
		try:
			if Evento.objects.filter(codigo_evento=cod_evento).exists() and DetalleParticipante.objects.filter(id_participante__identificacion=identificacion).exists():	
				detalle = DetalleParticipante.objects.get(id_participante__identificacion=identificacion)
				queryset = Evento.objects.get(codigo_evento=cod_evento)
				if queryset.codigo_evento == detalle.id_evento.codigo_evento:
					serializacion = EventoSerializer(queryset)
					return Response(data={"modalidad":queryset.modalidad,"tipo_evento":queryset.tipo_evento,"estado":queryset.estado,"curso_codigo":queryset.get_aula().aula.codigo_aula,"nombre_curso":queryset.get_aula().aula.nombre,"codigo_diseno":queryset.get_design().codigo,"cod_programa":queryset.get_design().cod_programa,"nombre":queryset.nombre,"certificado_recibido":queryset.get_design().tipo_certificado,"fecha_inicio":queryset.fecha_inicio,"fecha_fin":queryset.fecha_fin,"duracion":queryset.duracion},status=status.HTTP_200_OK)
				else:
					return Response(data={"eventoNo":"Evento no completado"},status=status.HTTP_200_OK)
			else:
				return Response(data={"error":"Evento no encontrado"},status=status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response(data={"error":"Error"},status=status.HTTP_404_NOT_FOUND)

class eventosDestino(APIView):
	def post(self,request):
		cod_evento = request.data.get('codigo_convalidar')
		queryset = None
		serializacion = None
		try:
			if Evento.objects.filter(codigo_evento=cod_evento).exists():
				queryset = Evento.objects.get(Q(codigo_evento=cod_evento))
				serializacion = EventoSerializer(queryset)
				return Response(data={"estado":queryset.estado,"curso_codigo":queryset.get_aula().aula.codigo_aula,"nombre_curso":queryset.get_aula().aula.nombre,"codigo_diseno":queryset.get_design().codigo,"cod_programa":queryset.get_design().cod_programa,"nombre":queryset.nombre,"certificado_recibido":queryset.get_design().tipo_certificado,"fecha_inicio":queryset.fecha_inicio,"fecha_fin":queryset.fecha_fin,"duracion":queryset.duracion},status=status.HTTP_200_OK)
			else:
				return Response(data={"error":"Evento no encontrado"},status=status.HTTP_200_OK)	
		except Exception as e:
			print(e)
			return Response(data={"error":"error en el sistema"},status=status.HTTP_200_OK)



