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

class AlumnosAll(generics.CreateAPIView):
    #Aquí se valida la autenticación del usuario
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.filter(user__is_active = 1).order_by("id")
        lista = AlumnoSerializer(alumnos, many=True).data
        
        return Response(lista, 200)

class AlumnoView(generics.CreateAPIView):
    # Permisos por método (sobrescribe el comportamiento default)
    # Verifica que el usuario esté autenticado para las peticiones GET, PUT y DELETE
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación
    
    #Obtener usuario por ID
    def get(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id = request.GET.get("id"))
        alumno = AlumnoSerializer(alumno, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(alumno, 200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_ser = UserSerializer(data=request.data)

        if user_ser.is_valid():
            # Campos base de usuario
            role = request.data.get('rol')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            password = request.data.get('password')

            # Campos específicos de alumno
            matricula = request.data.get('matricula')
            curp = request.data.get('curp')

            # Validaciones de unicidad
            if User.objects.filter(email=email).exists():
                return Response({"message": f"Username {email}, is already taken"}, status=400)

            if matricula and Alumnos.objects.filter(matricula=matricula).exists():
                return Response({"message": f"Matricula {matricula} already exists"}, status=400)

            if curp and Alumnos.objects.filter(curp=curp).exists():
                return Response({"message": f"CURP {curp} already exists"}, status=400)

            # Crear usuario
            user = User.objects.create(
                username=email,
                email=email,
                first_name=first_name or '',
                last_name=last_name or '',
                is_active=1
            )
            user.set_password(password)
            user.save()

            # Asignar rol si viene
            if role:
                group, _ = Group.objects.get_or_create(name=role)
                group.user_set.add(user)

            # Crear registro de alumno
            alumno = Alumnos.objects.create(
                user=user,
                matricula=matricula,
                fecha_nacimiento=request.data.get('fecha_nacimiento'),
                curp=curp,
                rfc=(request.data.get('rfc') or '').upper(),
                edad=request.data.get('edad'),
                telefono=request.data.get('telefono'),
                ocupacion=request.data.get('ocupacion')
            )
            alumno.save()

            return Response({"alumno_created_id": alumno.id}, status=201)

        return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar datos del administrador
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        # Verificamos que el usuario esté autenticado
        permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el administrador a actualizar
        alumno = get_object_or_404(Alumnos, id=request.data["id"])
        alumno.matricula = request.data["matricula"]
        alumno.fecha_nacimiento = request.data["fecha_nacimiento"]
        alumno.curp = request.data["curp"]
        alumno.rfc = request.data["rfc"]
        alumno.edad = request.data["edad"]
        alumno.telefono = request.data["telefono"]
        alumno.ocupacion = request.data["ocupacion"]
        alumno.save()
        # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
        user = alumno.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        
        return Response({"message": "Alumno actualizado correctamente", "alumno": AlumnoSerializer(alumno).data}, 200)
        # return Response(user,200)   
        
    # Eliminar alumno con delete (Borrar realmente)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id=request.GET.get("id"))
        try:
            alumno.user.delete()
            return Response({"details":"Alumno eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)