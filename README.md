# Zplix — Sistema de login/registro (Flask + SQLite)

Aplicación web de ejemplo que cubre: HTML/CSS, JavaScript, campos de entrada,
validación (cliente y servidor), Fetch API, endpoints, base de datos SQL,
Python/Flask, rutas, protección CSRF, y notas para HTTPS/hosting/dominio.

## Estructura

```
app.py              # Rutas y endpoints Flask
config.py           # Configuración (desarrollo/producción)
database.py         # Conexión SQLite y consultas SQL parametrizadas
schema.sql           # Definición de la tabla users
templates/           # Vistas HTML (Jinja2)
static/css/          # Estilos
static/js/           # Validación de campos y llamadas Fetch a los endpoints
```

## Puesta en marcha

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env    # ajusta SECRET_KEY
python app.py
```

Abre http://127.0.0.1:5000/register para crear un usuario y luego inicia
sesión en http://127.0.0.1:5000/login.

## Endpoints

| Método | Ruta            | Descripción                          |
|--------|-----------------|---------------------------------------|
| GET    | `/login`        | Página de inicio de sesión            |
| GET    | `/register`     | Página de registro                    |
| GET    | `/dashboard`    | Página protegida (requiere sesión)    |
| POST   | `/api/login`    | Autentica usuario (JSON)              |
| POST   | `/api/register` | Crea un usuario nuevo (JSON)          |
| POST   | `/api/logout`   | Cierra la sesión                      |

## Validación

- **Cliente**: `static/js/validation.js` valida usuario, correo y contraseña
  antes de enviar la petición, y los `input required/minlength` del HTML dan
  una primera capa de validación nativa del navegador.
- **Servidor**: `app.py` vuelve a validar todos los campos (nunca confiar
  solo en JS) y `database.py` usa consultas SQL parametrizadas (`?`) para
  evitar inyección SQL.

## Protección CSRF

`Flask-WTF` (`CSRFProtect`) protege todas las rutas `POST`. El token se
genera en `templates/base.html` (`<meta name="csrf-token">`) y el JS lo
envía en la cabecera `X-CSRFToken` en cada `fetch`.

## HTTPS, hosting y dominio (para producción)

### Opción gratuita recomendada: Render.com

El repo ya incluye `Procfile` y `render.yaml` listos para desplegar:

1. Sube el proyecto a un repositorio de GitHub (o GitLab).
2. Crea una cuenta gratuita en [render.com](https://render.com) y elige
   **New → Web Service**, conectando tu repositorio.
3. Render detecta `render.yaml` automáticamente (build: `pip install -r
   requirements.txt`, start: `gunicorn app:app`). La variable `SECRET_KEY`
   se genera sola y `FLASK_ENV=production` ya queda configurado.
4. Al terminar el despliegue obtienes una URL gratuita del tipo
   `https://zplix.onrender.com` con **certificado TLS válido y confiable
   (Let's Encrypt), emitido y renovado automáticamente por Render** — sin
   pagar dominio ni certificado.
5. (Opcional, de pago) Si más adelante compras un dominio propio, puedes
   añadirlo en Render → Settings → Custom Domain, y Render emite un
   certificado Let's Encrypt también para ese dominio.

> Nota: la base de datos SQLite (`app.db`) vive en el disco del servicio.
> En el plan gratuito de Render el disco es efímero (se reinicia con cada
> despliegue). Para persistencia real a largo plazo, usa un plan con disco
> persistente o migra a una base de datos gestionada (Render ofrece
> PostgreSQL gratuito por tiempo limitado).

### Otras opciones (todas con HTTPS automático)

- **Railway.app** / **Fly.io**: similares a Render, también gratuitos para
  proyectos pequeños y con TLS automático.
- **VPS propio** (DigitalOcean, Hetzner, etc.) + **Caddy**: Caddy obtiene y
  renueva certificados Let's Encrypt automáticamente con solo apuntar tu
  dominio; requiere comprar el dominio y el VPS.

### Variables de entorno en producción

Define `SECRET_KEY` y `FLASK_ENV=production` en el entorno del servidor
(no los subas al repositorio). Con `FLASK_ENV=production`,
`SESSION_COOKIE_SECURE=True` obliga a que las cookies de sesión solo
viajen por HTTPS.

