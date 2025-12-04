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

class MaestrosAll(generics.CreateAPIView):
    #Obtener todos los maestros
    # Necesita permisos de autenticación de usuario para poder acceder a la petición
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        maestros = Maestros.objects.filter(user__is_active=1).order_by("id")
        lista = MaestroSerializer(maestros, many=True).data
        return Response(lista, 200)

class MaestroView(generics.CreateAPIView):
    # Permisos por método (sobrescribe el comportamiento default)
    # Verifica que el usuario esté autenticado para las peticiones GET, PUT y DELETE
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación
    
    #Obtener usuario por ID
    def get(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id = request.GET.get("id"))
        maestro = MaestroSerializer(maestro, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(maestro, 200)

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

            # Campos específicos de maestro
            id_trabajador = request.data.get('id_trabajador')

            # Validaciones de unicidad
            if User.objects.filter(email=email).exists():
                return Response({"message": f"Username {email}, is already taken"}, status=400)

            if id_trabajador and Maestros.objects.filter(id_trabajador=id_trabajador).exists():
                return Response({"message": f"id_trabajador {id_trabajador} already exists"}, status=400)

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

            # Normalizar materias_json: aceptar lista o JSON string
            materias = request.data.get('materias_json')
            materias_val = []
            try:
                if materias is None:
                    materias_val = []
                elif isinstance(materias, str):
                    import json
                    materias_val = json.loads(materias)
                else:
                    materias_val = materias
            except Exception:
                materias_val = []

            # Crear registro de maestro
            maestro = Maestros.objects.create(
                user=user,
                id_trabajador=id_trabajador,
                fecha_nacimiento=request.data.get('fecha_nacimiento'),
                telefono=request.data.get('telefono'),
                rfc=(request.data.get('rfc') or '').upper(),
                cubiculo=request.data.get('cubiculo'),
                area_investigacion=request.data.get('area_investigacion'),
                materias_json=materias_val
            )
            maestro.save()

            return Response({"maestro_created_id": maestro.id}, status=201)

        return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)  
    # Actualizar datos del maestro
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        # Verificamos que el usuario esté autenticado
        permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el maestro a actualizar
        maestro = get_object_or_404(Maestros, id=request.data["id"])
        # Actualizamos los campos del maestro
        maestro.id_trabajador = request.data.get('id_trabajador', maestro.id_trabajador)
        maestro.fecha_nacimiento = request.data.get('fecha_nacimiento', maestro.fecha_nacimiento)
        maestro.telefono = request.data.get('telefono', maestro.telefono)
        maestro.rfc = (request.data.get('rfc', maestro.rfc) or '').upper()
        maestro.cubiculo = request.data.get('cubiculo', maestro.cubiculo)
        maestro.area_investigacion = request.data.get('area_investigacion', maestro.area_investigacion)
        
        # Normalizar materias_json: aceptar lista o JSON string
        materias = request.data.get('materias_json', None)
        if materias is not None:
            materias_val = []
            try:
                if isinstance(materias, str):
                    import json
                    materias_val = json.loads(materias)
                else:
                    materias_val = materias
            except Exception:
                materias_val = []
            maestro.materias_json = materias_val

        maestro.save()
        # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
        user = maestro.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()
        return Response({"message": "Maestro actualizado correctamente", "maestro": MaestroSerializer(maestro).data}, 200)
    
    # Eliminar maestro con delete (Borrar realmente)
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.GET.get("id"))
        try:
            maestro.user.delete()
            return Response({"details":"Maestro eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)