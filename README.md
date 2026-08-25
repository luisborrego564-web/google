# Zplix — Login con auto-registro (Flask + MySQL)

Aplicación web mínima: una única página de login (`templates/login.html`,
HTML+CSS+JS embebidos en el mismo archivo) que autentica contra una base de
datos MySQL. Si el correo no existe, la cuenta se crea automáticamente en
el primer inicio de sesión.

## Estructura

```
app.py         # App Flask: rutas y endpoints
config.py      # Configuración (desarrollo/producción)
database.py    # Conexión MySQL (PyMySQL) y consultas SQL parametrizadas
schema.sql     # Definición de la tabla users (referencia)
templates/
  login.html   # Única página: HTML + <style> + <script> en un solo archivo
```

## Base de datos: MySQL (Aiven)

El proyecto usa un `DATABASE_URL` de un MySQL gestionado (recomendado:
[aiven.io](https://aiven.io), plan gratuito) para que los datos sobrevivan
a reinicios/redeploys, a diferencia de un archivo SQLite local en hosting
gratuito (que se pierde en cada redeploy).

1. Crea una cuenta gratis en aiven.io y un servicio **MySQL** (no Kafka).
2. En "Overview" → "Connection information", copia el "Service URI"
   (`mysql://usuario:password@host:puerto/defaultdb?ssl-mode=REQUIRED`).
3. Local: copia `.env.example` a `.env` y pega el valor en `DATABASE_URL`.
4. Producción (Render): agrégalo como variable de entorno `DATABASE_URL`
   en el dashboard del servicio (Settings → Environment).

## Puesta en marcha local

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env    # ajusta SECRET_KEY y DATABASE_URL
python app.py
```

Abre http://127.0.0.1:5000/ — escribe cualquier correo y contraseña: si el
correo no existe se crea la cuenta al momento; si ya existe, debe coincidir
la contraseña.

## Endpoints

| Método | Ruta            | Descripción                                    |
|--------|-----------------|-------------------------------------------------|
| GET    | `/`, `/login`   | Página de login (HTML/CSS/JS autocontenidos)     |
| POST   | `/api/login`    | Autentica o crea la cuenta en el primer login    |
| POST   | `/api/logout`   | Cierra la sesión                                 |

## Validación

- **Servidor** (`app.py`): exige que usuario y contraseña no estén vacíos,
  y usa consultas SQL parametrizadas (`%s`) en `database.py` para evitar
  inyección SQL.
- No hay validación de formato/longitud en el cliente (se quitó a pedido).

## Protección CSRF

`Flask-WTF` (`CSRFProtect`) protege la ruta `POST /api/login` y `/api/logout`.
El token se genera con `{{ csrf_token() }}` dentro de `login.html` y el JS
embebido lo envía en la cabecera `X-CSRFToken` en cada `fetch`.

## HTTPS, hosting y dominio (para producción)

### Opción gratuita recomendada: Render.com

El repo ya incluye `Procfile` y `render.yaml` listos para desplegar:

1. Sube el proyecto a un repositorio de GitHub (o GitLab).
2. Crea una cuenta gratuita en [render.com](https://render.com) y elige
   **New → Web Service**, conectando tu repositorio.
3. Render detecta `render.yaml` automáticamente (build: `pip install -r
   requirements.txt`, start: `gunicorn app:app`). La variable `SECRET_KEY`
   se genera sola y `FLASK_ENV=production` ya queda configurado.
4. Agrega manualmente la variable de entorno `DATABASE_URL` (tu Service URI
   de Aiven) en Render → Settings → Environment.
5. Obtienes una URL gratuita del tipo `https://zplix.onrender.com` con
   **certificado TLS válido y confiable (Let's Encrypt)**, emitido y
   renovado automáticamente por Render — sin pagar dominio ni certificado.
6. (Opcional, de pago) Si más adelante compras un dominio propio, puedes
   añadirlo en Render → Settings → Custom Domain.

### Otras opciones (todas con HTTPS automático)

- **Railway.app** / **Fly.io**: similares a Render, también gratuitos para
  proyectos pequeños y con TLS automático.
- **VPS propio** (DigitalOcean, Hetzner, etc.) + **Caddy**: Caddy obtiene y
  renueva certificados Let's Encrypt automáticamente con solo apuntar tu
  dominio; requiere comprar el dominio y el VPS.

### Variables de entorno en producción

Define `SECRET_KEY`, `FLASK_ENV=production` y `DATABASE_URL` en el entorno
del servidor (nunca los subas al repositorio; `.env` está en `.gitignore`).
Con `FLASK_ENV=production`, `SESSION_COOKIE_SECURE=True` obliga a que las
cookies de sesión solo viajen por HTTPS.

