from django.db.models import *
from django.db import transaction
from app_movil_escolar_api.serializers import UserSerializer
from app_movil_escolar_api.serializers import *
from app_movil_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
import json
from django.shortcuts import get_object_or_404

class EventAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        evento = EventosAcademicos.objects.filter().order_by('id')
        lista = EventoAcademicoSerializer(evento, many=True).data
        #TODO: Regresar perfil del usuario
        return Response(lista, 200)
    
class EventView(generics.CreateAPIView):
        # Permisos por método (sobrescribe el comportamiento default)
    # Verifica que el usuario esté autenticado para las peticiones GET, PUT y DELETE
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación
    #Obtener evento por ID
    def get(self, request, *args, **kwargs):
        evento = get_object_or_404(EventosAcademicos, id = request.GET.get("id"))
        evento = EventoAcademicoSerializer(evento, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(evento, 200)
    
    #Registrar nuevo evento
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Serializamos los datos del evento para volverlo de nuevo JSON
        evento = EventoAcademicoSerializer(data=request.data)
        
        if evento.is_valid():
            evento = EventosAcademicos.objects.create(
                                        nombre_evento = request.data['nombre_evento'],
                                        tipo_evento = request.data['tipo_evento'],
                                        fecha_evento = request.data['fecha_evento'],
                                        hora_inicio = request.data['hora_inicio'],
                                        hora_termino = request.data['hora_termino'],
                                        lugar = request.data['lugar'],
                                        publico_seleccionado = request.data['publico_seleccionado'],
                                        carrera = request.data['carrera'],
                                        responsable = request.data['responsable'],
                                        descripcion_evento = request.data['descripcion_evento'],
                                        cupo_maximo = request.data['cupo_maximo'],
            )
            evento.save()
            return Response({"message":"Evento creado correctamente"},200)
        else:
            return Response(evento.errors,400)
        
    #Actualizar evento
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        evento = get_object_or_404(EventosAcademicos, id = request.data['id'])
        evento_serializer = EventoAcademicoSerializer(evento, data=request.data)
        
        if evento_serializer.is_valid():
            evento.nombre_evento = request.data['nombre_evento']
            evento.tipo_evento = request.data['tipo_evento']
            evento.fecha_evento = request.data['fecha_evento']
            evento.hora_inicio = request.data['hora_inicio']
            evento.hora_termino = request.data['hora_termino']
            evento.lugar = request.data['lugar']
            evento.publico_seleccionado = request.data['publico_seleccionado']
            evento.carrera = request.data['carrera']
            evento.responsable = request.data['responsable']
            evento.descripcion_evento = request.data['descripcion_evento']
            evento.cupo_maximo = request.data['cupo_maximo']
            evento.save()
            return Response({"message":"Evento actualizado correctamente"},200)
        else:
            return Response(evento_serializer.errors,400)
    #Eliminar evento
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        evento = get_object_or_404(EventosAcademicos, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"message": "Evento eliminado correctamente"}, 200)
        except Exception as e:
            return Response({"error": str(e)}, 400)