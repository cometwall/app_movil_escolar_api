# app_movil_escolar_api

API backend para la aplicación móvil escolar. Está desarrollado con Django y Django REST Framework, y proporciona endpoints para administrar perfiles de administradores, alumnos y maestros, así como eventos académicos y autenticación.

## Contenido

- [Tecnologías](#tecnologías)
- [Requisitos](#requisitos)
- [Instalación y configuración local](#instalación-y-configuración-local)
- [Migraciones y superusuario](#migraciones-y-superusuario)
- [Ejecución local](#ejecución-local)
- [API](#api)
- [CORS](#cors)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Despliegue](#despliegue)
- [Notas importantes](#notas-importantes)
- [Licencia](#licencia)

## Tecnologías

- Python y Django 5
- Django REST Framework, autenticación por token y `django-filter`
- PostgreSQL, configurado mediante `dj-database-url` y `psycopg2-binary`
- `django-cors-headers` para CORS
- WhiteNoise y Gunicorn para servir la aplicación en producción

Las dependencias completas y sus versiones están en [`requirements.txt`](requirements.txt).

## Requisitos

- Python 3.10 o posterior y `pip`
- PostgreSQL para la base de datos
- Git

## Instalación y configuración local

Clona el repositorio y entra en su directorio:

```bash
git clone https://github.com/cometwall/app_movil_escolar_api.git
cd app_movil_escolar_api
```

Crea y activa un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell, actívalo con:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instala las dependencias:

```bash
python -m pip install -r requirements.txt
```

La configuración de Django lee `SECRET_KEY`, `DEBUG`, `RENDER_EXTERNAL_HOSTNAME` y `DATABASE_URL` del entorno. Para desarrollo local, configura una base PostgreSQL y sus variables antes de ejecutar los comandos de Django. Por ejemplo, en Linux o macOS:

```bash
export SECRET_KEY='reemplaza-por-una-clave-local'
export DEBUG=True
export DATABASE_URL='postgresql://usuario:contraseña@localhost:5432/app_movil_escolar_db'
```

En PowerShell:

```powershell
$env:SECRET_KEY = 'reemplaza-por-una-clave-local'
$env:DEBUG = 'True'
$env:DATABASE_URL = 'postgresql://usuario:contraseña@localhost:5432/app_movil_escolar_db'
```

Sustituye los valores de ejemplo por los de tu entorno. No compartas credenciales ni uses una clave de desarrollo en producción.

## Migraciones y superusuario

Aplica las migraciones existentes para preparar la base de datos:

```bash
python manage.py migrate
```

Si modificas los modelos, genera las migraciones y después aplícalas:

```bash
python manage.py makemigrations
python manage.py migrate
```

Puedes crear un superusuario de Django desde la terminal:

```bash
python manage.py createsuperuser
```

Este comando crea una cuenta de Django; no crea por sí solo un perfil escolar ni asigna uno de los roles usados por el endpoint de inicio de sesión.

## Ejecución local

Inicia el servidor de desarrollo:

```bash
python manage.py runserver
```

La API estará disponible en `http://127.0.0.1:8000/`. La configuración local de `DEBUG=True` permite ese host. La ruta `/admin/` del proyecto es un endpoint de la API para administrar perfiles, no la interfaz de administración integrada de Django.

## API

Los endpoints están definidos en `app_movil_escolar_api/urls.py`. Las rutas listadas a continuación se usan con el host y puerto donde se ejecute el backend, por ejemplo `http://127.0.0.1:8000`.

| Ruta | Método(s) y uso |
| --- | --- |
| `/admin/` | `POST` crea un perfil de administrador; `GET` consulta un perfil por `id`; `PUT` actualiza y `DELETE` elimina el perfil. |
| `/lista-admins/` | `GET` lista administradores. Requiere autenticación. |
| `/alumno/` | `POST` crea un alumno; `GET` consulta por `id`; `PUT` actualiza y `DELETE` elimina el perfil. |
| `/lista-alumnos/` | `GET` lista alumnos. Requiere autenticación. |
| `/maestro/` | `POST` crea un maestro; `GET` consulta por `id`; `PUT` actualiza y `DELETE` elimina el perfil. |
| `/lista-maestros/` | `GET` lista maestros. Requiere autenticación. |
| `/evento/` | `POST` crea un evento; `GET` consulta por `id`; `PUT` actualiza y `DELETE` elimina el evento. |
| `/lista-eventos/` | `GET` lista eventos. Requiere autenticación. |
| `/login/` | `POST` inicia sesión y devuelve información del perfil y un token para los roles admitidos por la vista. |
| `/logout/` | `GET` cierra la sesión de token. Requiere autenticación. |
| `/total-usuarios/` | `GET` devuelve los totales de administradores, maestros y alumnos. |

Las rutas de creación aceptan los datos definidos por sus serializers y vistas. Las rutas de lista requieren autenticación; las operaciones `GET` individuales, `PUT` y `DELETE` de perfiles y eventos también requieren autenticación. Para otras rutas y detalles de validación, consulta `app_movil_escolar_api/views/`.

### Autenticación

Envía al endpoint `/login/` una solicitud `POST` con `username` y `password`:

```bash
curl -X POST http://127.0.0.1:8000/login/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"correo@ejemplo.com","password":"tu-contraseña"}'
```

Para las solicitudes autenticadas, envía el token devuelto en el encabezado `Authorization`, precedido por el prefijo `Bearer`.

## CORS

El backend permite actualmente solicitudes desde estos orígenes:

- `http://localhost:4200`
- `https://app-movil-escolar-web-beryl.vercel.app`

La configuración se encuentra en `CORS_ALLOWED_ORIGINS` dentro de `app_movil_escolar_api/settings.py`. Si conectas otro frontend, agrega su origen explícitamente. La configuración también permite credenciales.

## Estructura del proyecto

```text
.
├── app_movil_escolar_api/
│   ├── migrations/       # Migraciones de base de datos
│   ├── views/            # Vistas y endpoints de la API
│   ├── settings.py       # Configuración de Django
│   ├── urls.py           # Rutas
│   ├── models.py         # Modelos de datos
│   └── wsgi.py           # Aplicación WSGI
├── static/               # Archivos estáticos
├── build.sh              # Preparación de despliegue en Render
├── main.py               # Punto de entrada WSGI para App Engine
├── manage.py             # Utilidades de Django
└── requirements.txt      # Dependencias de Python
```

## Despliegue

El repositorio incluye `build.sh` para la preparación de un despliegue en Render. El script instala las dependencias, recopila archivos estáticos y ejecuta las migraciones. Configura en el servicio las variables `SECRET_KEY`, `DATABASE_URL` y `DEBUG=False`; configura también el hostname externo cuando corresponda. Como comando de inicio del servidor web, usa:

```bash
gunicorn app_movil_escolar_api.wsgi:application --bind 0.0.0.0:$PORT
```

`main.py` y `app.yaml` también contienen una configuración de entrada para Google App Engine. Revisa y ajusta la configuración del proveedor antes de desplegar.

## Notas importantes

- `DEBUG` es `False` de forma predeterminada; usa `DEBUG=True` solo durante el desarrollo local.
- Configura una `SECRET_KEY` propia mediante una variable de entorno y no publiques credenciales.
- Las vistas de la API usan paginación por número de página, con un tamaño predeterminado de 10 elementos.
- En producción, WhiteNoise sirve los archivos estáticos; el script de Render ejecuta `collectstatic`.

## Licencia

El repositorio no incluye una licencia explícita. Consulta al mantenedor antes de reutilizar o distribuir el código.
