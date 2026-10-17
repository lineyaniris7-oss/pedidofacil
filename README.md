# PedidoFácil

Aplicación web para la **gestión de productos y pedidos**, desarrollada con Django y Python.
Permite iniciar sesión, administrar un catálogo de productos, registrar pedidos y consultar
la información, que se guarda en una base de datos PostgreSQL alojada en Neon y se publica en Render.

- **Aplicación publicada:** https://pedidofacil-w1d4.onrender.com/productos/
- **Repositorio:** https://github.com/lineyaniris7-oss/pedidofacil

> La aplicación está en el plan gratuito de Render: si nadie la ha visitado en un rato,
> la primera carga puede tardar cerca de un minuto.

## Tecnologías

| Parte | Herramientas |
|---|---|
| Lenguaje y framework | Python, Django |
| Interfaz | HTML5, CSS3, Bootstrap 5, JavaScript |
| Base de datos | PostgreSQL en Neon |
| Publicación | Render, Gunicorn y WhiteNoise |
| Control de versiones | Git y GitHub |

## Funcionalidades

**Acceso y seguridad**
- Inicio y cierre de sesión con el sistema de autenticación integrado de Django.
- Registro de nuevos usuarios. Las contraseñas las cifra Django; nunca se guardan en texto plano.
- Todas las páginas de productos y pedidos están protegidas: quien no ha iniciado sesión
  es enviado al formulario de login.
- Mensajes claros cuando las credenciales son incorrectas.

**Productos**
- Crear, consultar el listado, ver el detalle, editar y eliminar.
- Datos: nombre, descripción, precio, cantidad disponible y fecha de registro.
- Búsqueda por nombre del producto.

**Pedidos**
- Crear, consultar el listado, ver el detalle, editar y eliminar.
- Datos: número de pedido (único), cliente, descripción, valor total, estado, fecha de registro
  y usuario que lo registró (se asigna solo, según la sesión iniciada).
- Estados: pendiente, confirmado o cancelado, con opción para cambiarlo desde el detalle.
- Búsqueda por nombre del cliente.

**Interfaz**
- Menú de navegación, tablas, formularios y botones con Bootstrap.
- Diseño adaptable a computadores y celulares.
- Mensajes de éxito y de error, y confirmación antes de eliminar un registro.

## Validaciones

Los datos se revisan en dos niveles. Las de JavaScript avisan antes de enviar el formulario,
y las de Django siempre se aplican en el servidor, aunque se salten las del navegador.

| Campo | Regla |
|---|---|
| Producto: nombre | Obligatorio, mínimo 3 caracteres |
| Producto: precio | Número mayor que cero |
| Producto: cantidad disponible | Número entero igual o mayor que cero |
| Producto: descripción | No supera la longitud definida en el modelo (500) |
| Pedido: número | Obligatorio y único (no se permiten duplicados) |
| Pedido: cliente y descripción | Obligatorios |
| Pedido: valor total | Número mayor que cero |
| Pedido: estado | Solo pendiente, confirmado o cancelado |

- **JavaScript** (`static/js/validaciones.js`): marca en rojo el campo con error, muestra el mensaje,
  impide enviar el formulario y vuelve a validar cuando el usuario corrige.
- **Django** (formularios y modelos): vuelve a revisar todo en el servidor, y las restricciones
  importantes, como el número de pedido único, también quedan respaldadas por la base de datos.

## Modelo de datos

**Producto:** `id`, `nombre`, `descripcion`, `precio`, `cantidad_disponible`, `fecha_registro`.

**Pedido:** `id`, `numero_pedido` (único), `cliente`, `fecha_registro`, `descripcion`,
`valor_total`, `estado` y `usuario` (relación con el usuario de Django que lo registró).

Todo el acceso a la base de datos se hace con el ORM de Django.

## Estructura del proyecto

```
pedidofacil/
├── config/         Configuración del proyecto (settings, urls, wsgi)
├── usuarios/       Inicio de sesión, cierre de sesión y registro
├── productos/      Módulo de productos
├── pedidos/        Módulo de pedidos
├── templates/      Plantilla base (menú y Bootstrap)
├── static/         Archivos CSS y JavaScript
├── manage.py
├── requirements.txt
└── README.md
```

## Rutas principales

| Ruta | Qué hace |
|---|---|
| `/usuarios/login/` | Iniciar sesión |
| `/usuarios/registro/` | Crear una cuenta |
| `/productos/` | Listado de productos |
| `/productos/registrar/` | Crear un producto |
| `/pedidos/` | Listado de pedidos |
| `/pedidos/registrar/` | Crear un pedido |

## Instalación y ejecución en local

Requisitos: Python 3.12 o superior, Git y una base de datos PostgreSQL en Neon.

1. Clonar el repositorio:

```bash
git clone https://github.com/lineyaniris7-oss/pedidofacil.git
cd pedidofacil
```

2. Crear y activar el entorno virtual (Windows):

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Crear un archivo `.env` en la raíz del proyecto, al lado de `manage.py`:

```
SECRET_KEY=una-clave-secreta-larga
DEBUG=True
DATABASE_URL=postgresql://usuario:contraseña@host/basededatos?sslmode=require
```

   - `SECRET_KEY`: cualquier texto largo y difícil de adivinar.
   - `DATABASE_URL`: la cadena de conexión de Neon (en Neon, botón **Connect**).
   - Este archivo **no se sube a GitHub**: está en el `.gitignore`.

5. Crear las tablas en la base de datos:

```bash
python manage.py migrate
```

6. Ejecutar el servidor:

```bash
python manage.py runserver
```

7. Abrir en el navegador http://127.0.0.1:8000/productos/ y crear una cuenta en
   `/usuarios/registro/`, o crear un administrador con `python manage.py createsuperuser`.

## Despliegue en Render

**Enlace de la aplicación publicada:** https://pedidofacil-w1d4.onrender.com/productos/

Servicio de tipo **Web Service**, conectado al repositorio de GitHub (rama `main`):

| Campo | Valor |
|---|---|
| Build Command | `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate` |
| Start Command | `gunicorn config.wsgi` |

Variables de entorno en Render:

| Variable | Valor |
|---|---|
| `SECRET_KEY` | Una clave secreta distinta a la local |
| `DEBUG` | `False` |
| `DATABASE_URL` | La cadena de conexión de Neon |

Render define solo `RENDER_EXTERNAL_HOSTNAME`, y `settings.py` la usa para aceptar su dominio.

## Seguridad

- Las credenciales (clave secreta y conexión a la base de datos) están en variables de entorno,
  no en el código, y el archivo `.env` está excluido del repositorio.
- Las contraseñas de los usuarios se guardan cifradas por Django.
- Las acciones que cambian datos (eliminar, cambiar estado, cerrar sesión) solo funcionan por `POST`
  y llevan protección CSRF.
- En producción, `DEBUG` está en `False`.