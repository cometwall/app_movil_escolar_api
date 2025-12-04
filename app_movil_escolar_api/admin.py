from django.contrib import admin
from django.utils.html import format_html
from app_movil_escolar_api.models import *


@admin.register(Administradores)
# TODO: Aquí agregarán los otros dos

class ProfilesAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")


@admin.register(Alumnos)
class AlumnosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "matricula", "curp", "telefono", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name", "matricula", "curp")
    readonly_fields = ("creation", "update")


@admin.register(Maestros)
class MaestrosAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "id_trabajador", "telefono", "area_investigacion", "creation", "update")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name", "id_trabajador")
    readonly_fields = ("creation", "update")

@admin.register(EventosAcademicos)
class EventosAcademicosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_evento", "tipo_evento", "lugar", "publico_seleccionado", "carrera", "fecha_evento", "hora_inicio", "hora_termino", "responsable", "descripcion_evento", "cupo_maximo", "creation", "update")
    search_fields = ("nombre_evento",)
    readonly_fields = ("creation", "update")


