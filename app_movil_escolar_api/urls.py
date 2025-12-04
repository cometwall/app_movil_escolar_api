from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.bootstrap import VersionView
from app_movil_escolar_api.views import bootstrap
from app_movil_escolar_api.views import alumnos
from app_movil_escolar_api.views import users
from app_movil_escolar_api.views import maestros
from app_movil_escolar_api.views import eventos
from app_movil_escolar_api.views import auth
# from sistema_escolar_api.views import alumnos
# from sistema_escolar_api.views import maestros

urlpatterns = [
    #Create Admin
        path('admin/', users.AdminView.as_view()),
    #Admin Data
        path('lista-admins/', users.AdminAll.as_view()),
    #Create Alumno
        path('alumno/', alumnos.AlumnoView.as_view()),
    #List Alumnos
        path('lista-alumnos/', alumnos.AlumnosAll.as_view()),
    #Edit Admin
        #path('admins-edit/', users.AdminsViewEdit.as_view())
    #Create Maestro
        path('maestro/', maestros.MaestroView.as_view()),
    #Total Users
        path('total-usuarios/', users.TotalUsers.as_view()),
    #List Maestros
        path('lista-maestros/', maestros.MaestrosAll.as_view()),
    #Create Evento
        path('evento/', eventos.EventView.as_view()),
    #List Eventos
        path('lista-eventos/', eventos.EventAll.as_view()),
    #Login
        path('login/', auth.CustomAuthToken.as_view()),
    #Logout
        path('logout/', auth.Logout.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


